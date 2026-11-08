/** Synthetic-only tenant/actor scope regression. Identity objects are TEST DOUBLES, not real sessions. */
import test from 'node:test';
import assert from 'node:assert/strict';
import { mkdtempSync, rmSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { ReservationLedger } from './reservation-ledger.mjs';
import { SyntheticOrderStore } from './synthetic-order-store.mjs';
import { SyntheticTenantOrderGate } from './synthetic-tenant-order-gate.mjs';

const parties = Object.freeze({ donor:'SYN-alice', receiver:'SYN-bob', transport:'SYN-carl' });
const principal = (role, tenantId='SYN-coalition-A', actorId=parties[role]) =>
  ({ authenticated:true, tenantId, role, actorId });
const order = () => ({
  id:'SYN-order', offerId:'SYN-offer', needId:'SYN-need', quantity:3, parties, at:100,
  bundle:{ id:'SYN-bundle', expiresAt:600,
    items:[{resourceId:'SYN-food',quantity:3},{resourceId:'SYN-storage',quantity:3},{resourceId:'SYN-vehicle',quantity:1}] }
});
function setup(file=':memory:') {
  const ledger=new ReservationLedger(file);
  for(const [id,n] of [['SYN-food',10],['SYN-storage',10],['SYN-vehicle',1]])
    ledger.seedResource(id,n);
  const store=new SyntheticOrderStore(ledger);
  let identity=null;
  const gate=new SyntheticTenantOrderGate(store,()=>identity);
  return { ledger, store, gate, become:p=>{identity=p;} };
}

test('unbound order and missing actual server principal both refuse access',()=>{
  const x=setup();
  try {
    x.store.createReserved(order());
    assert.throws(()=>x.gate.read('SYN-order'),/verified_principal_required/);
    x.become(principal('donor'));
    assert.throws(()=>x.gate.read('SYN-order'),/tenant_scope_denied/);
    assert.equal(x.store.get('SYN-order').events.length,2);
  } finally { x.ledger.close(); }
});
test('wrong tenant, even with correct fictional actor, cannot read or approve',()=>{
  const x=setup();
  try {
    x.store.createReserved(order());x.gate.provisionForSyntheticTest('SYN-order','SYN-coalition-A',105);
    x.become(principal('donor','SYN-coalition-B'));
    assert.throws(()=>x.gate.read('SYN-order'),/tenant_scope_denied/);
    assert.throws(()=>x.gate.approve({id:'SYN-order',role:'donor',evidenceRef:'SYN-proof',at:110}),/tenant_scope_denied/);
    assert.equal(x.store.get('SYN-order').approvals.length,0);
  } finally { x.ledger.close(); }
});
test('same tenant but wrong actor, and mismatched role, are denied before effects',()=>{
  const x=setup();
  try {
    x.store.createReserved(order());x.gate.provisionForSyntheticTest('SYN-order','SYN-coalition-A',105);
    x.become(principal('donor','SYN-coalition-A','SYN-other'));
    assert.throws(()=>x.gate.read('SYN-order'),/actor_scope_denied/);
    x.become(principal('receiver'));
    assert.throws(()=>x.gate.approve({id:'SYN-order',role:'donor',evidenceRef:'SYN-forged',at:110}),/role_denied/);
    assert.throws(()=>x.gate.pickup({id:'SYN-order',evidenceRef:'SYN-forged',at:111}),/role_denied/);
    assert.equal(x.store.get('SYN-order').approvals.length,0);
  } finally { x.ledger.close(); }
});
test('spoofed actorId supplied in action input is ignored; resolver identity wins',()=>{
  const x=setup();
  try {
    x.store.createReserved(order());x.gate.provisionForSyntheticTest('SYN-order','SYN-coalition-A',105);
    x.become(principal('donor'));
    const result=x.gate.approve({id:'SYN-order',role:'donor',actorId:'SYN-attacker',evidenceRef:'SYN-consent',at:110});
    assert.equal(result.approvals[0].actorId,parties.donor);
    assert.equal(result.approvals.length,1);
  } finally { x.ledger.close(); }
});
test('valid isolated role sequence approves and authorizes pickup but only for transporter',()=>{
  const x=setup();
  try {
    x.store.createReserved(order());x.gate.provisionForSyntheticTest('SYN-order','SYN-coalition-A',105);
    for(const [i,role] of ['donor','receiver','transport'].entries()) {
      x.become(principal(role));
      x.gate.approve({id:'SYN-order',role,evidenceRef:'SYN-'+role+'-proof',at:110+i});
    }
    x.become(principal('donor'));
    assert.throws(()=>x.gate.pickup({id:'SYN-order',at:115,evidenceRef:'SYN-pickup'}),/role_denied/);
    x.become(principal('transport'));
    assert.equal(x.gate.pickup({id:'SYN-order',at:116,evidenceRef:'SYN-pickup'}).state,'picked_up');
    assert.equal(x.ledger.available('SYN-vehicle'),0);
  } finally { x.ledger.close(); }
});
test('tenant binding is immutable and cannot be reassigned with conflicting provision',()=>{
  const x=setup();
  try {
    x.store.createReserved(order());
    x.gate.provisionForSyntheticTest('SYN-order','SYN-coalition-A',105);
    x.gate.provisionForSyntheticTest('SYN-order','SYN-coalition-A',105);
    assert.throws(()=>x.gate.provisionForSyntheticTest('SYN-order','SYN-coalition-B',106),/tenant_binding_conflict/);
    assert.throws(()=>x.ledger.db.exec("UPDATE synthetic_order_tenants SET tenant_id='SYN-coalition-B'"),/immutable_tenant_binding/);
    assert.throws(()=>x.ledger.db.exec('DELETE FROM synthetic_order_tenants'),/immutable_tenant_binding/);
    assert.throws(()=>x.gate.provisionForSyntheticTest('SYN-unknown','SYN-coalition-A',100),/unknown_order/);
  } finally { x.ledger.close(); }
});
test('tenant scope and approval denial persist after SQLite close and restart',()=>{
  const dir=mkdtempSync(join(tmpdir(),'maya-tenant-gate-'));
  const file=join(dir,'synthetic.sqlite');
  try {
    let x=setup(file);
    x.store.createReserved(order());x.gate.provisionForSyntheticTest('SYN-order','SYN-coalition-A',105);
    x.ledger.close();
    x=setup(file);
    try {
      x.become(principal('receiver','SYN-coalition-B'));
      assert.throws(()=>x.gate.read('SYN-order'),/tenant_scope_denied/);
      x.become(principal('receiver'));
      assert.equal(x.gate.read('SYN-order').id,'SYN-order');
      assert.equal(x.gate.cancel({id:'SYN-order',evidenceRef:'SYN-cancel',at:140}).state,'canceled');
      assert.equal(x.ledger.available('SYN-vehicle'),1);
    } finally { x.ledger.close(); }
  } finally { rmSync(dir,{recursive:true,force:true}); }
});
test('malformed or unauthenticated principal cannot masquerade as an operator',()=>{
  const x=setup();
  try {
    x.store.createReserved(order());x.gate.provisionForSyntheticTest('SYN-order','SYN-coalition-A',105);
    for(const p of [
      {tenantId:'SYN-coalition-A',actorId:'SYN-operator',role:'operator'},
      {authenticated:true,tenantId:'SYN-coalition-A',role:'operator'},
      {authenticated:true,tenantId:'SYN-coalition-A',actorId:'SYN-operator',role:'administrator'},
      {authenticated:'true',tenantId:'SYN-coalition-A',actorId:'SYN-operator',role:'operator'}
    ]) {
      x.become(p); assert.throws(()=>x.gate.read('SYN-order'),/verified_principal_required/);
    }
    x.become(principal('operator','SYN-coalition-A','SYN-operator'));
    assert.equal(x.gate.read('SYN-order').id,'SYN-order');
    assert.throws(()=>x.gate.approve({id:'SYN-order',role:'donor',evidenceRef:'SYN-fake',at:120}),/role_denied/);
  } finally { x.ledger.close(); }
});
