import test from "node:test";
import assert from "node:assert/strict";
import {assessKnowledgeSource,assessOperationalObservation} from "./knowledge-gates.mjs";
const now=new Date("2026-11-07T22:00:00Z");
test("licensed public research is background, never live inventory",()=>{
 const r=assessKnowledgeSource({id:"public-guide",title:"Fictional food rescue guide",url:"https://example.org/guide",publisher:"fictional",retrievedAt:"2026-11-07T21:00:00Z",kind:"research",licenseStatus:"verified"},now);
 assert.equal(r.usableForBackground,true);assert.equal(r.usableForLiveInventory,false);
});
test("unverified source rights block research ingestion",()=>assert.equal(assessKnowledgeSource({id:"x",title:"x",url:"x",publisher:"x",retrievedAt:"2026-11-07T21:00:00Z",kind:"research",licenseStatus:"unknown"},now).usableForBackground,false));
test("fresh authorized confirmed inventory can be considered",()=>assert.equal(assessOperationalObservation({organizationId:"fictional-A",resourceId:"freezer",sourceId:"fictional-authorized-api",authorized:true,status:"confirmed",observedAt:"2026-11-07T21:59:00Z",quantity:20},now).usableForMatching,true));
test("stale or unauthorized inventory blocked",()=>{
 const r=assessOperationalObservation({organizationId:"fictional-A",resourceId:"freezer",sourceId:"unapproved",authorized:false,status:"confirmed",observedAt:"2026-11-07T20:00:00Z",quantity:20},now);
 assert.equal(r.usableForMatching,false);assert.ok(r.reasons.includes("authorization_missing"));
});
