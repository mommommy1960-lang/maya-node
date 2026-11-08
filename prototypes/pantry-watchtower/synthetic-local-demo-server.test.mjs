import test from 'node:test';
import http from 'node:http';
import assert from 'node:assert/strict';
import { mkdtempSync, rmSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { createLocalDemo } from './synthetic-local-demo-server.mjs';

async function withDemo(fn, opts = {}) {
  const app = createLocalDemo(opts); const url = await app.listen();
  try { return await fn(url, app); }
  finally { await app.close(); }
}
async function get(url, path = '/api/state', headers = {}) {
  const res = await fetch(url + path, { headers }); return [res.status, await res.json()];
}
async function post(url, action, extra = {}, headers = {}) {
  const res = await fetch(url + '/api/action', {method:'POST',headers:{'content-type':'application/json',...headers},body:JSON.stringify({action,...extra})});
  return [res.status,await res.json()];
}
async function approveAll(url) { for (const role of ['donor','receiver','transport']) assert.equal((await post(url,'approve',{role}))[0],200); }
async function commercialize(url) { for (const action of ['quote','accept-terms','mock-authorize']) assert.equal((await post(url,action))[0],200); }

test('new local demo serves explicitly fictional, empty state and loopback HTML', async () => withDemo(async url => {
  const [status, state] = await get(url);
  assert.equal(status,200); assert.equal(state.synthetic,true); assert.equal(state.live,false);
  assert.equal(state.order,null); assert.deepEqual(state.capacity,{food:12,cold:12,truck:12});
  const response = await fetch(url);
  const html=await response.text();
  assert.match(html,/SYNTHETIC DEMONSTRATION ONLY/);
  assert.match(html,/aria-live="polite"/);
  assert.match(html,/data-action="start"/);
  assert.equal(response.headers.get('x-frame-options'),'DENY');
}));

test('full order, approvals, pickup, receipt consumes food and returns reusable slots',async()=>withDemo(async url=>{
  let [status,state]=await post(url,'start'); assert.equal(status,200); assert.equal(state.order.state,'reserved');
  assert.deepEqual(state.capacity,{food:4,cold:4,truck:4});
  await approveAll(url);
  assert.equal((await get(url))[1].order.state,'approved');
  assert.equal((await post(url,'pickup'))[0],409);
  await commercialize(url);
  assert.equal((await post(url,'pickup'))[1].order.state,'picked_up');
  [status,state]=await post(url,'deliver',{mode:'full'});
  assert.equal(status,200); assert.equal(state.order.state,'reconciled');
  assert.equal(state.receipt.received,8); assert.equal(state.receipt.missing,0);
  assert.deepEqual(state.capacity,{food:4,cold:12,truck:12});
  assert.deepEqual(state.order.events.map(e=>e.kind).slice(-3),['picked_up','delivered','reconciled']);
}));

test('partial delivery stays exception until disposition and missing food is never restocked',async()=>withDemo(async url=>{
  await post(url,'start');await approveAll(url);await commercialize(url);await post(url,'pickup');
  const [,state]=await post(url,'deliver',{mode:'partial'});
  assert.equal(state.order.state,'exception');
  assert.equal(state.receipt.received,6);assert.equal(state.receipt.rejected,1);assert.equal(state.receipt.missing,1);
  assert.deepEqual(state.capacity,{food:4,cold:12,truck:12});
  const [,resolved]=await post(url,'document-exception');
  assert.equal(resolved.order.state,'reconciled');assert.equal(resolved.receipt.disposition.code,'exception_documented');
  assert.equal(resolved.capacity.food,4);
}));

test('reject pickup before all three fictional approvals',async()=>withDemo(async url=>{
  await post(url,'start'); await post(url,'approve',{role:'donor'});
  const [status] = await post(url,'pickup');assert.equal(status,409);
  const [,state]=await get(url);assert.equal(state.order.state,'reserved');assert.equal(state.order.approvals.length,1);
}));

test('refuse duplicate order, repeat approval is idempotent, no extra allocation',async()=>withDemo(async url=>{
  await post(url,'start');
  assert.equal((await post(url,'start'))[0],409);
  await post(url,'approve',{role:'donor'});
  const [,state]=await post(url,'approve',{role:'donor'});
  assert.equal(state.order.approvals.length,1); assert.deepEqual(state.capacity,{food:4,cold:4,truck:4});
}));

test('cancel before pickup returns all three resources',async()=>withDemo(async url=>{
  await post(url,'start');const [,state]=await post(url,'cancel');
  assert.equal(state.order.state,'canceled');assert.deepEqual(state.capacity,{food:12,cold:12,truck:12});
}));

test('cannot cancel after pickup or overwrite a previously recorded receipt',async()=>withDemo(async url=>{
  await post(url,'start');await approveAll(url);await commercialize(url);await post(url,'pickup');
  assert.equal((await post(url,'cancel'))[0],409);
  await post(url,'deliver',{mode:'full'});
  assert.notEqual((await post(url,'deliver',{mode:'partial'}))[0],200);
  const [,state]=await get(url);assert.equal(state.receipt.received,8);assert.equal(state.order.state,'reconciled');
}));

test('reject unknown role, invalid delivery mode and unrecognized actions',async()=>withDemo(async url=>{
  await post(url,'start');
  assert.equal((await post(url,'approve',{role:'admin'}))[0],409);
  assert.equal((await post(url,'deliver',{mode:'real'}))[0],409);
  assert.equal((await post(url,'send-notification'))[0],409);
  assert.equal((await get(url))[1].order.state,'reserved');
}));

test('block cross-origin and cross-site operations before state mutation',async()=>withDemo(async url=>{
  assert.equal((await post(url,'start',{}, {origin:'https://attacker.example'}))[0],403);
  assert.equal((await post(url,'start',{}, {'sec-fetch-site':'cross-site'}))[0],403);
  assert.equal((await get(url))[1].order,null);
}));

test('reject malformed body, wrong content type, missing path and untrusted Host',async()=>withDemo(async url=>{
  let r=await fetch(url+'/api/action',{method:'POST',headers:{'content-type':'text/plain'},body:'{}'});assert.equal(r.status,415);
  r=await fetch(url+'/api/action',{method:'POST',headers:{'content-type':'application/json'},body:'nonsense'});assert.equal(r.status,409);
  r=await fetch(url+'/../../.git/config');assert.equal(r.status,404);
  const badHostStatus = await new Promise((resolve, reject) => {
    const req = http.request({hostname:'127.0.0.1',port:Number(new URL(url).port),
      path:'/api/state',headers:{Host:'evil.example:8000'}}, res => {
        res.resume(); res.on('end',()=>resolve(res.statusCode));
      });
    req.on('error',reject);req.end();
  });
  assert.equal(badHostStatus,403);
}));

test('SQLite file recovers fictional receipt and order across app restart',async()=>{
  const dir=mkdtempSync(join(tmpdir(),'maya-syn-'));
  const filename=join(dir,'synthetic.sqlite');
  try {
    await withDemo(async url=>{
      await post(url,'start');await approveAll(url);await commercialize(url);await post(url,'pickup');
      await post(url,'deliver',{mode:'partial'});
    },{filename});
    await withDemo(async url=>{
      const [,state]=await get(url);
      assert.equal(state.order.state,'exception');assert.equal(state.receipt.missing,1);
      assert.deepEqual(state.capacity,{food:4,cold:12,truck:12});
      const [,after]=await post(url,'document-exception');assert.equal(after.order.state,'reconciled');
    },{filename});
  } finally {rmSync(dir,{recursive:true,force:true});}
});

test('expired fictional reservation blocks late approval', async()=>{
  let now=1_000_000;
  await withDemo(async url=>{
    await post(url,'start');now+=900_001;
    const [status]=await post(url,'approve',{role:'donor'});assert.equal(status,409);
    assert.equal((await get(url))[1].order.state,'reserved');
  },{clock:()=>now});
});

test('local HTTP fictional quote, agreement, declined auth, retry, capture and refund',async()=>withDemo(async url=>{
  await post(url,'start'); await approveAll(url);
  assert.equal((await post(url,'mock-authorize'))[0],409);
  assert.equal((await post(url,'mock-capture'))[0],409);
  assert.equal((await post(url,'quote'))[1].commercial.sponsorFeeCents,250);
  assert.equal((await post(url,'accept-terms'))[1].commercial.receiverFeeCents,0);
  const declined=await post(url,'mock-decline');assert.equal(declined[0],200);
  assert.equal(declined[1].commercial.state,'accepted');
  const authorized=await post(url,'mock-authorize'); assert.equal(authorized[1].commercial.state,'authorized');
  assert.equal(authorized[1].commercial.provider,'LOCAL_SIMULATOR_ONLY_NOT_STRIPE');
  await post(url,'pickup');await post(url,'deliver',{mode:'full'});
  const capture=await post(url,'mock-capture');assert.equal(capture[1].commercial.simulatedNetCents,250);
  const refunded=await post(url,'mock-refund');assert.equal(refunded[1].commercial.simulatedNetCents,0);
  assert.equal((await post(url,'mock-refund'))[1].commercial.events.length,6);
  assert.equal((await get(url))[1].capacity.food,4);
}));
test('cancel order after fictional authorization atomically voids mock authorization',async()=>withDemo(async url=>{
  await post(url,'start');await approveAll(url);await commercialize(url);
  const [,state]=await post(url,'cancel');
  assert.equal(state.order.state,'canceled');
  assert.equal(state.commercial.state,'voided');
  assert.equal(state.commercial.events.at(-1).kind,'authorization_voided');
  assert.equal((await post(url,'pickup'))[0],409);
}));
