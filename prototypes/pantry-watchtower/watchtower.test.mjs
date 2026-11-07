import test from "node:test";
import assert from "node:assert/strict";
import { buildWatchtower } from "./watchtower.mjs";
const now=new Date("2026-11-07T22:00:00Z");
const observedAt="2026-11-07T21:59:00Z";
const sample={
 offers:[{id:"lot-1",pantryId:"fictional-A",observedAt,status:"confirmed",foodType:"produce",handling:"chilled",quantity:20,expiresAt:"2026-11-08T22:00:00Z"}],
 needs:[{id:"need-1",pantryId:"fictional-B",observedAt,status:"confirmed",foodType:"produce",quantity:10,receivingUntil:"2026-11-08T00:00:00Z"}],
 receivers:[{pantryId:"fictional-B",observedAt,status:"confirmed",handling:"chilled",freeCapacity:15}],
 vehicles:[{id:"truck-1",observedAt,status:"confirmed",handling:"chilled",capacity:12,available:true}],
 contacts:[{id:"fictional-manager",consent:true,active:true,role:"authorized",priority:1}],now
};
test("watchtower produces a proposal and a non-sending alert plan",()=>{
 const view=buildWatchtower(sample);
 assert.equal(view.proposals.length,1);
 assert.equal(view.proposals[0].quantity,10);
 assert.equal(view.notifications.length,1);
 assert.equal(view.notifications[0].send,false);
 assert.equal(view.liveDispatchEnabled,false);
 assert.equal(view.paymentEnabled,false);
});
test("freezer full blocks match",()=>{
 const view=buildWatchtower({...sample,receivers:[{...sample.receivers[0],freeCapacity:0}]});
 assert.equal(view.proposals.length,0);
 assert.equal(view.blocked.length,1);
 assert.equal(view.notifications.length,0);
});
test("unverified vehicle blocks match",()=>{
 const view=buildWatchtower({...sample,vehicles:[{...sample.vehicles[0],status:"estimated"}]});
 assert.equal(view.proposals.length,0);
});
