import test from "node:test";
import assert from "node:assert/strict";
import { buildWatchtower } from "./watchtower.mjs";
import { reconcileShipment } from "./reconciliation.mjs";
const now=new Date("2026-11-07T22:00:00Z"),observedAt="2026-11-07T21:59:00Z";
const offer={id:"fictional-lot",pantryId:"A",observedAt,status:"confirmed",foodType:"produce",handling:"chilled",quantity:20,expiresAt:"2026-11-08T00:00:00Z"};
const need=id=>({id,pantryId:"B",observedAt,status:"confirmed",foodType:"produce",quantity:10,receivingUntil:"2026-11-07T23:00:00Z"});
const receiver={pantryId:"B",observedAt,status:"confirmed",handling:"chilled",freeCapacity:20};
const truck={id:"fictional-truck",observedAt,status:"confirmed",handling:"chilled",capacity:20,available:true};
test("one offer and one truck cannot be double-booked by two needs",()=>{
 const r=buildWatchtower({offers:[offer],needs:[need("one"),need("two")],receivers:[receiver],vehicles:[truck],now});
 assert.equal(r.proposals.length,1);assert.equal(r.proposals[0].quantity,10);
});
test("two offers cannot share one truck in a snapshot",()=>{
 const r=buildWatchtower({offers:[offer,{...offer,id:"second"}],needs:[need("one"),need("two")],receivers:[receiver],vehicles:[truck],now});
 assert.equal(r.proposals.length,1);
});
test("invalid receipt does not suppress a subsequent valid receipt",()=>{
 const r=reconcileShipment({id:"fictional",loaded:200,receipts:[
 {id:"bad",confirmedBy:null,recordedAt:now.toISOString(),received:50},
 {id:"good",confirmedBy:"receiver",recordedAt:now.toISOString(),received:180}
 ]});
 assert.equal(r.received,180);assert.equal(r.difference,20);assert.equal(r.status,"needs_record_review");
});
