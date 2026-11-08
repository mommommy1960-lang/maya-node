import test from "node:test";
import assert from "node:assert/strict";
import {createOrder,transitionOrder} from "./order-lifecycle.mjs";
const at="2026-11-07T22:00:00Z",base=()=>createOrder({id:"fictional-order",offerId:"lot",needId:"need",quantity:10,createdAt:at});
test("synthetic order begins proposed without dispatch or payment",()=>{
 const o=base();assert.equal(o.state,"proposed");assert.equal(o.dispatchEnabled,false);assert.equal(o.paymentEnabled,false);
});
test("order cannot skip reservation",()=>assert.throws(()=>transitionOrder(base(),{to:"picked_up",at,actor:"fictional"}),/invalid_transition/));
test("order requires donor receiver and transport approval",()=>{
 const reserved=transitionOrder(base(),{to:"reserved",at,actor:"fictional"});
 assert.throws(()=>transitionOrder(reserved,{to:"approved",at,actor:"fictional",approvalEvidence:{donor:true}}),/missing_approvals/);
 const approved=transitionOrder(reserved,{to:"approved",at,actor:"fictional",approvalEvidence:{donor:true,receiver:true,transport:true}});
 assert.equal(approved.state,"approved");assert.equal(approved.events.length,3);
});
test("canceled order cannot restart",()=>{
 const canceled=transitionOrder(base(),{to:"canceled",at,actor:"fictional"});
 assert.throws(()=>transitionOrder(canceled,{to:"reserved",at,actor:"fictional"}),/invalid_transition/);
});
test("events cannot be backdated",()=>{
 const reserved=transitionOrder(base(),{to:"reserved",at:"2026-11-07T22:01:00Z",actor:"fictional"});
 assert.throws(()=>transitionOrder(reserved,{to:"canceled",at,actor:"fictional"}),/out_of_order_event/);
});
