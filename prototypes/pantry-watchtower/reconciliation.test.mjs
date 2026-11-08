import test from "node:test";
import assert from "node:assert/strict";
import { reconcileShipment } from "./reconciliation.mjs";
const base={id:"fictional-shipment",loaded:200,receipts:[{id:"proof-1",confirmedBy:"fictional-pantry",recordedAt:"2026-11-07T22:00:00Z",received:180,rejected:0,damaged:0}]};
test("200 loaded and 180 received flags 20 for review without blame",()=>{
 const r=reconcileShipment(base);
 assert.equal(r.difference,20);
 assert.equal(r.status,"discrepancy_requires_review");
 assert.equal(r.automatedAccusation,false);
});
test("complete verified receipt reconciles",()=>{
 const r=reconcileShipment({...base,receipts:[{...base.receipts[0],received:200}]});
 assert.equal(r.difference,0);assert.equal(r.status,"reconciled");
});
test("missing proof requires review",()=>{
 const r=reconcileShipment({...base,receipts:[{...base.receipts[0],confirmedBy:null}]});
 assert.equal(r.status,"needs_record_review");
});
test("duplicate proof cannot double count",()=>{
 const r=reconcileShipment({...base,receipts:[base.receipts[0],base.receipts[0]]});
 assert.equal(r.status,"needs_record_review");assert.equal(r.received,180);
});
