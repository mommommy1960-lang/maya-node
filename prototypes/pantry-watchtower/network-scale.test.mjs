import test from "node:test";
import assert from "node:assert/strict";
import { buildWatchtower } from "./watchtower.mjs";
import { reconcileShipment } from "./reconciliation.mjs";
/** Synthetic empire stress harness: many fictional pantry/vehicle/offer combinations. */
const now=new Date("2026-11-07T22:00:00Z"),observedAt="2026-11-07T21:59:00Z";
const pantryCount=30,offerCount=300,vehicleCount=40;
const pantries=Array.from({length:pantryCount},(_,i)=>"fictional-pantry-"+i);
const offers=Array.from({length:offerCount},(_,i)=>({id:"offer-"+i,pantryId:pantries[i%pantryCount],foodType:"produce",handling:"chilled",quantity:5,observedAt,status:"confirmed",expiresAt:"2026-11-08T22:00:00Z"}));
const needs=Array.from({length:offerCount},(_,i)=>({id:"need-"+i,pantryId:pantries[(i+1)%pantryCount],foodType:"produce",quantity:5,observedAt,status:"confirmed",receivingUntil:"2026-11-08T00:00:00Z"}));
const receivers=pantries.map(pantryId=>({pantryId,observedAt,status:"confirmed",handling:"chilled",freeCapacity:20}));
const vehicles=Array.from({length:vehicleCount},(_,i)=>({id:"truck-"+i,observedAt,status:"confirmed",handling:"chilled",capacity:5,available:true}));
test("300 offers cannot overbook 40 trucks or 30 pantry freezers",()=>{
 const r=buildWatchtower({offers,needs,receivers,vehicles,now});
 assert.ok(r.proposals.length<=vehicleCount);
 assert.equal(new Set(r.proposals.map(p=>p.vehicleId)).size,r.proposals.length);
 assert.equal(new Set(r.proposals.map(p=>p.offerId)).size,r.proposals.length);
 assert.equal(new Set(r.proposals.map(p=>p.needId)).size,r.proposals.length);
 for(const pantryId of pantries) assert.ok(r.proposals.filter(p=>p.to===pantryId).reduce((n,p)=>n+p.quantity,0)<=20);
 assert.equal(r.liveDispatchEnabled,false);
 assert.equal(r.paymentEnabled,false);
});
test("100 synthetic shipment reconciliations preserve discrepancy counts",()=>{
 for(let i=0;i<100;i++){
  const received=i%2?180:200;
  const r=reconcileShipment({id:"shipment-"+i,loaded:200,receipts:[{id:"receipt-"+i,confirmedBy:"fictional-receiver",recordedAt:observedAt,received}]});
  assert.equal(r.difference,200-received);
  assert.equal(r.automatedAccusation,false);
 }
});
