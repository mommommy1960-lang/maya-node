import test from "node:test";
import assert from "node:assert/strict";
import { evaluateTransfer, recordEvent } from "./matching.mjs";
const now = new Date("2026-11-07T22:00:00Z");
const stamp = "2026-11-07T21:59:00Z";
const offer = { observedAt: stamp, status: "confirmed", foodType: "produce", handling: "chilled", quantity: 20, expiresAt: "2026-11-08T22:00:00Z" };
const need = { observedAt: stamp, status: "confirmed", foodType: "produce", quantity: 10, receivingUntil: "2026-11-08T00:00:00Z" };
const receiver = { observedAt: stamp, status: "confirmed", handling: "chilled", freeCapacity: 12 };
const vehicle = { observedAt: stamp, status: "confirmed", handling: "chilled", capacity: 15, available: true };
test("safe candidate is a proposal, never a dispatch", () => {
  assert.deepEqual(evaluateTransfer(offer,need,receiver,vehicle,now), {
    eligible:true, quantity:10, reasons:[], state:"proposal_only",
    requires:["donor_approval","receiver_approval","transport_confirmation"]
  });
});
test("stale freezer capacity blocks", () => {
  const result=evaluateTransfer(offer,need,{...receiver,observedAt:"2026-11-07T20:00:00Z"},vehicle,now);
  assert.equal(result.eligible,false); assert.ok(result.reasons.includes("unverified_or_stale"));
});
test("full freezer blocks", () => assert.equal(evaluateTransfer(offer,need,{...receiver,freeCapacity:0},vehicle,now).eligible,false));
test("driver unavailable blocks", () => assert.equal(evaluateTransfer(offer,need,receiver,{...vehicle,available:false},now).eligible,false));
test("spoiled lot blocks", () => assert.equal(evaluateTransfer({...offer,expiresAt:"2026-11-07T21:00:00Z"},need,receiver,vehicle,now).eligible,false));
test("incompatible cold chain blocks", () => assert.equal(evaluateTransfer(offer,need,receiver,{...vehicle,handling:"ambient"},now).eligible,false));
test("duplicate event ignored", () => {
  const e={id:"synthetic-1",type:"offer",observedAt:stamp,source:"fictional-pantry"};
  assert.equal(recordEvent(recordEvent([],e),e).length,1);
});
