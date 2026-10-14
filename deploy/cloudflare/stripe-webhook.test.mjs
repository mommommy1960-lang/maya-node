import {test} from 'node:test';
import assert from 'node:assert/strict';
import {DatabaseSync} from 'node:sqlite';
import {readFileSync} from 'node:fs';
import worker,{verifyStripeSignature,reviewMessages,fulfillStripeEvent} from './worker.mjs';
function database(){
  const raw=new DatabaseSync(':memory:');
  raw.exec(readFileSync(new URL('./schema.sql',import.meta.url),'utf8'));
  return {raw,prepare(sql){
    return {bind(...args){
      const s=raw.prepare(sql);
      return {async first(){return s.get(...args)||null},async run(){const r=s.run(...args);return {meta:{changes:r.changes}}}};
    }};
  }};
}
const event=()=>({livemode:true,type:'checkout.session.completed',data:{object:{id:'cs_live_TestOrder123',livemode:true,mode:'payment',payment_status:'paid',payment_link:'plink_1UFNOZJYOy8NtnKHK8eCz4BP',currency:'usd',amount_total:2500,customer_details:{email:'buyer@example.invalid'}}}});
async function sign(body,t){const key=await crypto.subtle.importKey('raw',new TextEncoder().encode('test-only-signing-key'),{name:'HMAC',hash:'SHA-256'},false,['sign']);const bytes=new Uint8Array(await crypto.subtle.sign('HMAC',key,new TextEncoder().encode(`${t}.${body}`)));return `t=${t},v1=${Array.from(bytes,b=>b.toString(16).padStart(2,'0')).join('')}`;}
test('signature rejects tampering, missing signatures and expired/future timestamps',async()=>{const body=JSON.stringify(event()),t=1000;const h=await sign(body,t);assert.equal(await verifyStripeSignature(body,h,'test-only-signing-key',t),true);assert.equal(await verifyStripeSignature(body+' ',h,'test-only-signing-key',t),false);assert.equal(await verifyStripeSignature(body,h,'test-only-signing-key',t+301),false);assert.equal(await verifyStripeSignature(body,h,'test-only-signing-key',t-301),false);assert.equal(await verifyStripeSignature(body,null,'test-only-signing-key',t),false);});
test('unpaid, wrong amount, other link, other account and testmode never deliver',()=>{for(const mutate of [e=>e.data.object.payment_status='unpaid',e=>e.data.object.amount_total=3500,e=>e.data.object.payment_link='other',e=>e.account='acct_other',e=>e.livemode=false]){const e=event();mutate(e);assert.equal(reviewMessages(e),null);}});
test('delayed payment succeeds only after paid event',()=>{const e=event();e.type='checkout.session.async_payment_succeeded';assert.equal(reviewMessages(e).messages.length,2);e.type='checkout.session.async_payment_failed';assert.equal(reviewMessages(e),null);});
test('duplicate paid events send one buyer email and one owner email',async()=>{const db=database();let calls=0;const env={DB:db,SEND_ENABLED:'true'};const factory=async()=>async()=>({id:`receipt${++calls}`});await fulfillStripeEvent(event(),env,factory);await fulfillStripeEvent(event(),env,factory);assert.equal(calls,2);assert.equal(db.raw.prepare("SELECT COUNT(*) AS n FROM jobs WHERE state='sent'").get().n,2);});
test('OAuth failure leaves durable queued messages and retry sends once',async()=>{const db=database(),env={DB:db,SEND_ENABLED:'true'};await assert.rejects(fulfillStripeEvent(event(),env,async()=>{throw Error('oauth')}));assert.equal(db.raw.prepare("SELECT COUNT(*) AS n FROM jobs WHERE state='queued'").get().n,2);let calls=0;await fulfillStripeEvent(event(),env,async()=>async()=>({id:`r${++calls}`}));assert.equal(calls,2);});
test('ambiguous submission is never automatically resent',async()=>{const db=database(),env={DB:db,SEND_ENABLED:'true'};let calls=0;const factory=async()=>async()=>{calls++;throw Error('timeout')};await assert.rejects(fulfillStripeEvent(event(),env,factory));await assert.rejects(fulfillStripeEvent(event(),env,factory));assert.equal(calls,1);});
test('mail disabled and malicious email headers cannot enqueue',async()=>{const db=database();await assert.rejects(fulfillStripeEvent(event(),{DB:db,SEND_ENABLED:'false'},()=>assert.fail()));const e=event();e.data.object.customer_details.email='a@example.invalid,b@example.invalid';assert.throws(()=>reviewMessages(e));assert.equal(db.raw.prepare('SELECT COUNT(*) AS n FROM jobs').get().n,0);});
test('public webhook fails closed without secret; controller stays protected',async()=>{assert.equal((await worker.fetch(new Request('https://worker.test/stripe/webhook',{method:'POST',body:'{}'}),{})).status,503);assert.equal((await worker.fetch(new Request('https://worker.test/status'),{})).status,401);assert.equal((await worker.fetch(new Request('https://worker.test/stripe/webhook',{method:'POST',body:'{}'}),{DB:{},STRIPE_WEBHOOK_SECRET:'test'})).status,400);});
