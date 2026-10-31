import { test } from 'node:test';
import assert from 'node:assert/strict';
import { OWNER_ID, OWNER_EMAIL, hasAccess, snapshot, subscriptionId, verifySignature, webhook, processEvent, ownerBilling, D1Store } from '../payments.mjs';
const now = Math.floor(Date.now()/1000);
const env = { STRIPE_SECRET_KEY: 'rk_test_example', STRIPE_PRICE_ID: 'price_example', STRIPE_WEBHOOK_SECRET: 'whsec_example' };
function sub(overrides = {}) { return { id: 'sub_example', livemode:false, customer:'cus_example', status:'active', cancel_at_period_end:false,
  items:{data:[{quantity:1,current_period_end:now+3600,price:{id:'price_example',livemode:false,currency:'usd',unit_amount:1000,recurring:{interval:'month',interval_count:1}}}]},
  latest_invoice:{livemode:false,customer:'cus_example',parent:{subscription_details:{subscription:'sub_example'}},status:'paid',currency:'usd',amount_paid:1000,amount_remaining:0}, ...overrides }; }
function event(type='checkout.session.completed', object={}, id='evt_example') { return {id,livemode:false,type,data:{object:{id:'cs_test_example',livemode:false,customer:'cus_example',subscription:'sub_example',client_reference_id:OWNER_ID,mode:'subscription',payment_status:'paid',...object}}}; }
function store() { return {state:{revision:0},events:new Set(),checkouts:new Set(['cs_test_example']),
  async seen(id){return this.events.has(id)}, async read(){return {...this.state}}, async hasCheckout(id){return this.checkouts.has(id)},
  async commit(id,rev,next){if(this.state.revision!==rev)return false; this.state={...next,revision:rev+1};this.events.add(id);return true} }; }
const sendSub = value => async()=>Response.json(value);
async function signature(payload,t=now,secret=env.STRIPE_WEBHOOK_SECRET) {
  const e=new TextEncoder();const k=await crypto.subtle.importKey('raw',e.encode(secret),{name:'HMAC',hash:'SHA-256'},false,['sign']);
  const a=await crypto.subtle.sign('HMAC',k,e.encode(`${t}.${payload}`));return `t=${t},v1=${Array.from(new Uint8Array(a),b=>b.toString(16).padStart(2,'0')).join('')}`;
}
test('real verifier accepts signature and rotation headers; rejects tamper, stale and future timestamps',async()=>{
  const p=JSON.stringify(event()),h=await signature(p);
  assert.equal(await verifySignature(p,h,env.STRIPE_WEBHOOK_SECRET),true);
  assert.equal(await verifySignature(p,h+',v1='+'0'.repeat(64),env.STRIPE_WEBHOOK_SECRET),true);
  assert.equal(await verifySignature(p+'x',h,env.STRIPE_WEBHOOK_SECRET),false);
  for(const t of [now-601,now+601])assert.equal(await verifySignature(p,await signature(p,t),env.STRIPE_WEBHOOK_SECRET),false);
  assert.equal(await verifySignature(p,'t=no,v1=bad',env.STRIPE_WEBHOOK_SECRET),false);
});
test('actual webhook route rejects invalid signature without touching state',async()=>{
  const s=store();const r=await webhook(new Request('https://example/api/stripe/webhook',{method:'POST',body:'{}'}),env,s);
  assert.equal(r.status,400);assert.equal(s.events.size,0);
});
test('actual webhook route processes signed paid checkout',async()=>{
  const s=store(),payload=JSON.stringify(event());
  const r=await webhook(new Request('https://example/api/stripe/webhook',{method:'POST',body:payload,headers:{'Stripe-Signature':await signature(payload)}}),env,s,sendSub(sub()));
  assert.equal(r.status,200);assert.equal(hasAccess(s.state),true);
});
test('unpaid checkout never grants access or calls Stripe',async()=>{
  const s=store();const r=await processEvent(event(undefined,{payment_status:'unpaid'}),env,s,()=>{throw Error('must not fetch')});
  assert.equal(r.pending_payment,true);assert.equal(hasAccess(s.state),false);
});
test('unrecognized checkout and forged owner reference cannot link',async()=>{
  for(const o of [{id:'cs_unrecognized'},{client_reference_id:'someone-else'}]){
    const s=store();assert.equal((await processEvent(event(undefined,o),env,s)).ignored,true);assert.equal(s.events.size,0);
  }
});
test('rejects live events and live subscriptions',async()=>{
  const s=store();await assert.rejects(processEvent({...event(),livemode:true},env,s),/sandbox event/);
  await assert.rejects(processEvent(event(),env,s,sendSub(sub({livemode:true}))),/Live Stripe/);
});
test('live API key rejected before outbound call',async()=>{
  await assert.rejects(processEvent(event(),{...env,STRIPE_SECRET_KEY:'sk_live_example'},store(),()=>{throw Error('must not fetch')}),/Sandbox test key/);
});
test('requires matching price and paid invoice; handles item-level billing period',()=>{
  const good=snapshot(sub(),env);assert.equal(hasAccess(good),true);
  assert.equal(hasAccess({...good,period_end:null}),false);assert.equal(hasAccess({...good,period_end:now},now),false);
  assert.equal(hasAccess({...good,status:'canceled'}),false);
  assert.throws(()=>snapshot(sub(),{...env,STRIPE_PRICE_ID:'price_other'}),/Unexpected practice price/);
  assert.throws(()=>snapshot(sub({items:{data:[{...sub().items.data[0],current_period_end:null}]}}),env),/Missing billing period/);
  assert.equal(hasAccess(snapshot(sub({latest_invoice:{...sub().latest_invoice,status:'open',amount_paid:0}}),env)),false);
  assert.throws(()=>snapshot(sub({latest_invoice:{...sub().latest_invoice,customer:'cus_other'}}),env),/ownership mismatch/);
});
test('duplicate event has one state commit',async()=>{
  const s=store();await processEvent(event(),env,s,sendSub(sub()));
  assert.equal((await processEvent(event(),env,s,()=>{throw Error('must not fetch')})).duplicate,true);assert.equal(s.state.revision,1);
});
test('Stripe failure leaves event retryable',async()=>{
  const s=store();await assert.rejects(processEvent(event(),env,s,async()=>Response.json({}, {status:500})),/Stripe request failed/);
  assert.equal(s.events.size,0);await processEvent(event(),env,s,sendSub(sub()));assert.equal(hasAccess(s.state),true);
});
test('database commit failure leaves event retryable',async()=>{
  const s=store(),commit=s.commit;s.commit=async()=>{throw Error('DB failed')};
  await assert.rejects(processEvent(event(),env,s,sendSub(sub())),/DB failed/);assert.equal(s.events.size,0);
  s.commit=commit;await processEvent(event(),env,s,sendSub(sub()));assert.equal(s.events.size,1);
});
test('older event reads canonical canceled state rather than restoring access',async()=>{
  const s=store();await processEvent(event(),env,s,sendSub(sub()));
  await processEvent(event('customer.subscription.updated',{id:'sub_example',subscription:undefined,status:'active'},'evt_old'),env,s,sendSub(sub({status:'canceled'})));
  assert.equal(hasAccess(s.state),false);
});
test('overlapping stale fetch loses revision check and remains retryable',async()=>{
  const s=store();const delayed=async()=>{s.state.revision++;return Response.json(sub())};
  await assert.rejects(processEvent(event(),env,s,delayed),/Concurrent update/);assert.equal(s.events.size,0);
});
test('invoice before linkage is retried; nested invoice subscription resolved',async()=>{
  const e=event('invoice.paid',{id:'in_example',subscription:undefined,parent:{subscription_details:{subscription:'sub_example'}}});
  assert.equal(subscriptionId(e),'sub_example');await assert.rejects(processEvent(e,env,store()),/not linked yet/);
});
test('different subscription cannot replace existing linked subscription',async()=>{
  const s=store();s.state.subscription='sub_other';await assert.rejects(processEvent(event(),env,s),/already linked/);
});
test('scheduled cancellation retains paid access, immediate cancellation revokes',async()=>{
  const s=store();await processEvent(event(),env,s,sendSub(sub({cancel_at_period_end:true})));
  assert.equal(s.state.cancel_at_period_end,true);assert.equal(hasAccess(s.state),true);
  await processEvent(event('customer.subscription.deleted',{id:'sub_example',subscription:undefined},'evt_deleted'),env,s,sendSub(sub({status:'canceled'})));
  assert.equal(hasAccess(s.state),false);
});
test('owner route rejects a different authenticated identity',async()=>{
  const r=await ownerBilling(new Request('https://example/api/stripe/cancel',{method:'POST'}),env,{email:'other@example.com'});
  assert.equal(r.status,403);
});
test('read-only owner discovery verifies one exact-price paid sandbox subscription with GET requests only',async()=>{
  const calls=[];
  const send=async(url,options={})=>{
    calls.push({url,method:options.method||'GET'});
    if(url.includes('/v1/customers?'))return Response.json({data:[{id:'cus_example',email:OWNER_EMAIL}],has_more:false});
    if(url.includes('/v1/subscriptions?'))return Response.json({data:[sub()],has_more:false});
    if(url.includes('/v1/subscriptions/sub_example?expand'))return Response.json(sub());
    throw Error('Unexpected Stripe request '+url);
  };
  const r=await ownerBilling(new Request('https://example/api/stripe/discover'),env,{email:OWNER_EMAIL},send);
  const d=await r.json();
  assert.equal(r.status,200);assert.equal(d.found,true);assert.equal(d.subscription_id,'sub_example');
  assert.equal(d.billing_access,true);assert.equal(d.paid,true);
  assert.equal(calls.length,3);assert.ok(calls.every(c=>c.method==='GET'));
  assert.ok(calls[0].url.includes(encodeURIComponent(OWNER_EMAIL)));
});
test('read-only discovery returns no match without importing or writing',async()=>{
  const calls=[];
  const send=async(url,options={})=>{calls.push([url,options.method||'GET']);return Response.json({data:url.includes('/customers?')?[{id:'cus_example',email:OWNER_EMAIL}]:[],has_more:false});};
  const r=await ownerBilling(new Request('https://example/api/stripe/discover'),env,{email:OWNER_EMAIL},send);
  assert.equal(r.status,200);assert.equal((await r.json()).found,false);
  assert.ok(calls.every(([,method])=>method==='GET'));
});
test('read-only discovery refuses ambiguous customer or subscription matches',async()=>{
  const customerSend=async()=>Response.json({data:[{id:'cus_one',email:OWNER_EMAIL},{id:'cus_two',email:OWNER_EMAIL}],has_more:false});
  const a=await ownerBilling(new Request('https://example/api/stripe/discover'),env,{email:OWNER_EMAIL},customerSend);
  assert.equal(a.status,409);
  const second=sub();
  second.id='sub_second';
  second.latest_invoice.parent.subscription_details.subscription='sub_second';
  const subSend=async(url)=>{
    if(url.includes('/customers?'))return Response.json({data:[{id:'cus_example',email:OWNER_EMAIL}],has_more:false});
    return Response.json({data:[sub(),second],has_more:false});
  };
  const b=await ownerBilling(new Request('https://example/api/stripe/discover'),env,{email:OWNER_EMAIL},subSend);
  assert.equal(b.status,409);
});
test('read-only discovery fails closed on incomplete customer pagination and live API keys',async()=>{
  const incomplete=await ownerBilling(new Request('https://example/api/stripe/discover'),env,{email:OWNER_EMAIL},async()=>Response.json({data:[],has_more:true}));
  assert.equal(incomplete.status,409);
  let called=false;
  const live=await ownerBilling(new Request('https://example/api/stripe/discover'),{...env,STRIPE_SECRET_KEY:'sk_live_example'},{email:OWNER_EMAIL},async()=>{called=true;});
  assert.equal(live.status,403);assert.equal(called,false);
});
test('actual owner cancellation uses POST period-end, never DELETE',async()=>{
  const value=snapshot(sub(),env);const db={prepare(){return{bind(){return this},async first(){return{revision:1,snapshot:JSON.stringify(value)}}}}};
  const calls=[];const send=async(url,opts)=>{calls.push([url,opts]);return Response.json(opts.method==='POST'?sub({cancel_at_period_end:true}):sub())};
  const r=await ownerBilling(new Request('https://example/api/stripe/cancel',{method:'POST'}),{...env,DB:db},{email:OWNER_EMAIL},send);
  assert.equal(r.status,200);assert.equal(calls[1][1].method,'POST');assert.equal(calls[1][1].body,'cancel_at_period_end=true');
});
test('D1 commit uses a single transactional batch with revision and event guards',async()=>{
  let batch;const db={prepare(sql){return{sql,bind(...v){this.values=v;return this}}},async batch(statements){batch=statements;return[{meta:{changes:1}},{meta:{changes:1}}]}};
  assert.equal(await new D1Store(db).commit('evt_one',2,{status:'active'}),true);
  assert.equal(batch.length,2);assert.match(batch[0].sql,/revision=\?/);assert.match(batch[1].sql,/EXISTS/);
});
