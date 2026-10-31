import {test} from 'node:test';
import assert from 'node:assert/strict';
import {mkdtempSync,readFileSync,rmSync} from 'node:fs';
import {tmpdir} from 'node:os';
import {join} from 'node:path';
import {spawnSync} from 'node:child_process';
import vm from 'node:vm';
import worker from '../dist/worker.mjs';
import {HTML} from '../ui.mjs';
import {D1Store,OWNER_ID,OWNER_EMAIL} from '../payments.mjs';
function db(path){
  function run(commands){const r=spawnSync('python',['test/sqlite_bridge.py',path],{input:JSON.stringify(commands),encoding:'utf8'});if(r.status!==0)throw Error(JSON.parse(r.stdout).error);return JSON.parse(r.stdout);}
  return{prepare(sql){return{sql,values:[],bind(...values){this.values=values;return this},async run(){return run([this])[0]},async first(){return run([this])[0].results[0]||null},async all(){return run([this])[0]}}},async batch(commands){return run(commands)}};
}
async function setup(t){const dir=mkdtempSync(join(tmpdir(),'maya-test-'));t.after(()=>rmSync(dir,{recursive:true,force:true}));
  const DB=db(join(dir,'test.db')),env={DB,STAGING_ACCESS_SECRET:'example_owner_secret',STRIPE_SECRET_KEY:'rk_test_example',STRIPE_PRICE_ID:'price_example',AI:{async run(){return{response:'Pineapple.'}}}};
  const request=(path,body,token)=>new Request('https://maya.example'+path,{method:body===undefined?'GET':'POST',headers:{'Content-Type':'application/json',...(token?{'Authorization':'Bearer '+token}:{})},body:body===undefined?undefined:JSON.stringify(body)});
  const login=await worker.fetch(request('/api/signin',{email:OWNER_EMAIL,accessSecret:env.STAGING_ACCESS_SECRET}),env);
  const token=(await login.json()).token;
  return{DB,env,token,request};
}
test('HTML and embedded browser script parse; billing controls and original local-storage keys exist',()=>{
  const script=HTML.match(/<script>([\s\S]*?)<\/script>/)[1];new vm.Script(script);
  for(const id of ['billing-refresh','subscription-id','portal','cancel','signin','send','discover-subscription','discovery-status','link-discovered'])assert.ok(HTML.includes('id="'+id+'"'));
  assert.ok(HTML.includes('maya_owner_token'));assert.ok(!script.includes('.innerHTML'));
});
test('original bearer login and owner chat persist in real SQLite without a paid subscription',async t=>{
  const {env,token,request}=await setup(t);assert.match(token,/^[a-f0-9]{64}$/);
  const r=await worker.fetch(request('/api/chat',{content:'Reply pineapple'},token),env);assert.equal(r.status,200);assert.equal((await r.json()).reply,'Pineapple.');
  const history=await worker.fetch(request('/api/messages',undefined,token),env);assert.equal((await history.json()).messages.length,2);
});
test('invalid credentials and unknown bearer rejected',async t=>{
  const {env,request}=await setup(t);
  assert.equal((await worker.fetch(request('/api/signin',{email:'other@example.com',accessSecret:env.STAGING_ACCESS_SECRET}),env)).status,403);
  assert.equal((await worker.fetch(request('/api/chat',{content:'x'},'0'.repeat(64)),env)).status,401);
});
test('session expiry retains conversation history for the next owner session',async t=>{
  const {env,DB,token,request}=await setup(t);
  await worker.fetch(request('/api/chat',{content:'Remember history'},token),env);
  await DB.prepare('UPDATE recovery_sessions SET created_at=? WHERE token=?').bind(new Date(Date.now()-7300000).toISOString(),token).run();
  assert.equal((await worker.fetch(request('/api/messages',undefined,token),env)).status,401);
  assert.equal((await DB.prepare('SELECT COUNT(*) AS n FROM recovery_messages').first()).n,2);
});
test('malformed session timestamp fails closed',async t=>{
  const {env,DB,token,request}=await setup(t);
  await DB.prepare('UPDATE recovery_sessions SET created_at=? WHERE token=?').bind('not-a-date',token).run();
  assert.equal((await worker.fetch(request('/api/messages',undefined,token),env)).status,401);
});
test('webhook route precedes bearer middleware and rejects missing signature',async t=>{
  const {env,request}=await setup(t);env.STRIPE_WEBHOOK_SECRET='whsec_example';
  assert.equal((await worker.fetch(request('/api/stripe/webhook',{}),env)).status,400);
});
test('subscription discovery requires an authenticated owner session',async t=>{
  const {env,request}=await setup(t);
  const r=await worker.fetch(request('/api/stripe/discover'),env);
  assert.equal(r.status,401);
});
test('success query alone grants no billing status',async t=>{
  const {env,DB,token,request}=await setup(t);await migrate(DB);
  assert.equal((await worker.fetch(request('/?checkout=success'),env)).status,200);
  const r=await worker.fetch(request('/api/stripe/access-status',undefined,token),env);
  const d=await r.json();assert.equal(d.billing_access,false);assert.equal(d.owner_demo_access,true);
});
async function migrate(DB){for(const sql of readFileSync('migration.sql','utf8').replace(/--[^\n]*/g,'').split(';').filter(s=>s.trim()))await DB.prepare(sql).run();}
test('actual D1Store SQL commits once; stale version and duplicates cannot overwrite snapshot',async t=>{
  const {DB}=await setup(t);await migrate(DB);const s=new D1Store(DB);
  assert.equal(await s.commit('evt_first',0,{subscription:'sub_one',status:'active'}),true);
  assert.equal(await s.commit('evt_stale',0,{subscription:'sub_stale'}),false);
  assert.equal((await s.read()).subscription,'sub_one');assert.equal(await s.seen('evt_stale'),false);
  assert.equal(await s.commit('evt_first',1,{subscription:'sub_duplicate'}),true);
  assert.equal((await s.read()).subscription,'sub_one');assert.equal((await s.read()).revision,1);
});
test('billing mutation without owner authentication is denied before Stripe',async t=>{
  const {env,request}=await setup(t);
  assert.equal((await worker.fetch(request('/api/stripe/cancel',{}),env)).status,401);
  assert.equal((await worker.fetch(request('/api/stripe/import',{subscriptionId:'sub_example'}),env)).status,401);
});
test('live key connectivity fails before network',async t=>{
  const {env,token,request}=await setup(t);env.STRIPE_SECRET_KEY='sk_live_example';
  assert.equal((await worker.fetch(request('/api/stripe/test',undefined,token),env)).status,403);
});
function stripeSubscription(){return{id:'sub_existing',livemode:false,customer:'cus_existing',status:'active',cancel_at_period_end:false,
  items:{data:[{quantity:1,current_period_end:Math.floor(Date.now()/1000)+3600,price:{id:'price_example',livemode:false,currency:'usd',unit_amount:1000,recurring:{interval:'month',interval_count:1}}}]},
  latest_invoice:{livemode:false,customer:'cus_existing',parent:{subscription_details:{subscription:'sub_existing'}},status:'paid',currency:'usd',amount_paid:1000,amount_remaining:0}};}
test('existing paid subscription import uses explicit ID, persists to SQLite and never searches email',async t=>{
  const {env,DB,token,request}=await setup(t);await migrate(DB);
  const prior=globalThis.fetch,calls=[];t.after(()=>globalThis.fetch=prior);
  globalThis.fetch=async(url,options)=>{calls.push([url,options]);return Response.json(stripeSubscription())};
  const r=await worker.fetch(request('/api/stripe/import',{subscriptionId:'sub_existing',confirmOwnerImport:true},token),env);
  assert.equal(r.status,200);assert.equal((await r.json()).billing_access,true);
  assert.match(calls[0][0],/\/subscriptions\/sub_existing\?expand/);assert.equal(calls.length,1);
  assert.equal((await new D1Store(DB).read()).subscription,'sub_existing');
});
test('checkout retains test safeguards and records owner linkage without exposing bearer token',async t=>{
  const {env,DB,token,request}=await setup(t);await migrate(DB);
  const prior=globalThis.fetch;let outbound;t.after(()=>globalThis.fetch=prior);
  globalThis.fetch=async(url,options)=>{outbound=options.body;return Response.json({id:'cs_test_example',livemode:false,url:'https://checkout.stripe.com/c/pay/cs_test_example'})};
  const r=await worker.fetch(request('/api/stripe/checkout',{},token),env);
  assert.equal(r.status,200);assert.equal((await r.json()).livemode,false);
  assert.equal(new URLSearchParams(outbound).get('client_reference_id'),OWNER_ID);assert.ok(!outbound.includes(token));
  assert.equal((await DB.prepare('SELECT owner_id FROM owner_sandbox_checkouts WHERE checkout_id=?').bind('cs_test_example').first()).owner_id,OWNER_ID);
});
test('signout invalidates bearer token without deleting chat history',async t=>{
  const {env,DB,token,request}=await setup(t);await worker.fetch(request('/api/chat',{content:'hello'},token),env);
  assert.equal((await worker.fetch(request('/api/signout',{},token),env)).status,200);
  assert.equal((await worker.fetch(request('/api/messages',undefined,token),env)).status,401);
  assert.equal((await DB.prepare('SELECT COUNT(*) AS n FROM recovery_messages').first()).n,2);
});
