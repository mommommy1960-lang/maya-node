import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import vm from 'node:vm';
const html=fs.readFileSync(new URL('../demos/offline_workflow_lab.html',import.meta.url),'utf8');
function lab(){
 const nodes=new Map();const element=()=>({textContent:'',disabled:false,attrs:{},children:[],setAttribute(k,v){this.attrs[k]=v;},replaceChildren(){this.children=[];},append(x){this.children.push(x);}});
 const document={getElementById(id){if(!nodes.has(id))nodes.set(id,element());return nodes.get(id);},createElement:element};
 const context=vm.createContext({document,URLSearchParams,location:{search:''}});
 vm.runInContext(html.match(/<script>([\s\S]*?)<\/script>/)[1],context);
 return {context,nodes,run:code=>vm.runInContext(code,context)};
}
for(const sector of ['housing','foodbank','accounts','subscriptions','school','bank','nonprofit','support']){
 test(`${sector}: approved, export, revocation and correction boundaries`,()=>{
  const x=lab();x.run(`reset('${sector}')`);
  assert.equal(x.run('request(state,sectors[state.sector].action).allowed'),true);
  assert.equal(x.run("request(state,'bulk_export').allowed"),false);
  x.run('revoke(state)');assert.equal(x.run('request(state,sectors[state.sector].action).allowed'),false);
  assert.equal(x.run('correct(state)'),true);
  assert.equal(x.run('request(state,sectors[state.sector].action).allowed'),false,'correction cannot restore permission');
 });
 test(`${sector}: execution checks expiry, purpose and owner coverage`,()=>{
  const x=lab();x.run(`reset('${sector}');state.now=119`);
  assert.equal(x.run('request(state,sectors[state.sector].action).allowed'),true);
  x.run('state.now=120');assert.equal(x.run('request(state,sectors[state.sector].action).reason'),'expired');
  x.run(`reset('${sector}')`);assert.equal(x.run("request(state,sectors[state.sector].action,{purpose:'marketing'}).allowed"),false);
  x.run('state.ownerAvailable=false');assert.equal(x.run('request(state,sectors[state.sector].action).reason'),'no_owner_coverage');
 });
}
test('payment amount cap rejects excess, negative and nonfinite values',()=>{
 const x=lab();x.run("reset('subscriptions')");
 for(const amount of ['6','-1','0','NaN','Infinity'])assert.equal(x.run(`request(state,'charge_once',{amount:${amount}}).reason`),'over_budget');
 assert.equal(x.run("request(state,'charge_once',{amount:5}).allowed"),true);
 assert.equal(x.run("request(state,'charge_recurring').allowed"),false);
});
test('offline edition has no external runtime dependencies or network calls',()=>{
 assert.equal(/\bfetch\s*\(|XMLHttpRequest|sendBeacon|<script[^>]+src=|<link[^>]+stylesheet/.test(html),false);
 assert.match(html,/identifier stays private/);assert.match(html,/not the paid Maya AI runtime/);
 assert.equal(/\b\d{2}-\d{7}\b/.test(html),false,'no taxpayer identifier in export');
});
test('visible controls execute fixture paths and reset restores independent state',()=>{
 const x=lab();x.nodes.get('subscriptions').onclick();x.nodes.get('budget').onclick();
 assert.match(x.nodes.get('decision').textContent,/BLOCKED/);
 x.nodes.get('reset').onclick();x.nodes.get('allowed').onclick();assert.match(x.nodes.get('decision').textContent,/ALLOWED/);
 x.nodes.get('expired').onclick();assert.match(x.nodes.get('decision').textContent,/expired/);
 x.nodes.get('reset').onclick();assert.equal(x.run('state.events.length'),0);
 x.nodes.get('foodbank').onclick();assert.equal(x.nodes.get('budget').disabled,true);
});
test('queued request is rechecked after permission changes',()=>{
 const x=lab();x.run("reset('accounts');var queuedAction=sectors.accounts.action;state.now=121");
 assert.equal(x.run('request(state,queuedAction).allowed'),false);
});

test('person-facing receipt excludes case payload and explains blocked review',()=>{
 const x=lab();x.nodes.get('scope').onclick();const receipt=x.nodes.get('receipt').textContent;
 assert.match(receipt,/Blocked in this fictional example/);assert.match(receipt,/outside scope/);
 assert.match(receipt,/Review required; no real notification sent/);assert.doesNotMatch(receipt,/missing-month review/);
 assert.match(receipt,/External licenses and identity have not been verified/);
});
test('receipt separates completed correction from restored permission',()=>{
 const x=lab();x.nodes.get('revoked').onclick();x.nodes.get('correct').onclick();
 assert.match(x.nodes.get('receipt').textContent,/Permission now: Revoked/);
 assert.match(x.nodes.get('receipt').textContent,/permission is not restored/);
 x.nodes.get('reset').onclick();assert.equal(x.nodes.get('receipt').textContent,'Run an action to see its receipt.');
});
test('receipt shows current expiry when a previously permitted request ages',()=>{
 const x=lab();x.nodes.get('allowed').onclick();x.run('state.now=120;render()');
 assert.match(x.nodes.get('receipt').textContent,/Outcome: Allowed in this fictional example/);
 assert.match(x.nodes.get('receipt').textContent,/Permission now: Expired/);
});
