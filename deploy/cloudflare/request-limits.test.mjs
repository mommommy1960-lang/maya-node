import test from 'node:test';
import assert from 'node:assert/strict';
import {boundedRequestText, stripeWebhook} from './worker.mjs';
function request(chunks, headers={}) {
  let canceled=false;
  let pulls=0;
  const body=new ReadableStream({
    pull(controller) { pulls++; if(chunks.length) controller.enqueue(chunks.shift()); else controller.close(); },
    cancel(){canceled=true}
  });
  return {request:new Request('https://example.com/stripe/webhook',{method:'POST',headers,body,duplex:'half'}), canceled:()=>canceled,pulls:()=>pulls};
}
test('exact byte boundary and split Unicode retain raw signature input',async()=>{
 const data=new TextEncoder().encode('a€');
 const r=request([data.slice(0,2),data.slice(2)]);
 assert.equal(await boundedRequestText(r.request,4),'a€');
});
test('chunked oversized request stops early and cancels remaining body',async()=>{
 const r=request([new Uint8Array(8),new Uint8Array(8),new Uint8Array(8),new Uint8Array(8)]);
 await assert.rejects(boundedRequestText(r.request,10),e=>e.status===413);
 assert.equal(r.canceled(),true); assert.ok(r.pulls()<5);
});
test('declared size cannot bypass measured byte limit',async()=>{
 const r=request([new Uint8Array(11)],{'content-length':'1'});
 await assert.rejects(boundedRequestText(r.request,10),e=>e.status===413);
});
test('invalid or excessive declared length rejected without reading',async()=>{
 for(const value of ['-1','garbage','9007199254740992','11']) {
  const req={headers:new Headers({'content-length':value}),get body(){throw new Error('body accessed');}};
  await assert.rejects(boundedRequestText(req,10),e=>e.status===(value==='11'?413:400));
 }
});
test('malformed UTF-8 is rejected without changing signature payload',async()=>{
 const r=request([new Uint8Array([0xc3])]);
 await assert.rejects(boundedRequestText(r.request,10),e=>e.status===400);
});
test('public webhook rejects chunked oversize before signature or database work',async()=>{
 const r=request([new Uint8Array(262145)]);
 const response=await stripeWebhook(r.request,{STRIPE_WEBHOOK_SECRET:'test',DB:{}});
 assert.equal(response.status,413);assert.equal(r.canceled(),true);
});
