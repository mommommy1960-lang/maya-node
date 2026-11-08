/** Real independent Node processes compete for one synthetic file-backed SQLite.
 * No customers, real inventory, actual transport, external calls or billing.
 */
import test from 'node:test';
import assert from 'node:assert/strict';
import { spawn } from 'node:child_process';
import { mkdtempSync, rmSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { fileURLToPath } from 'node:url';
import { ReservationLedger } from './reservation-ledger.mjs';
import { SyntheticOrderStore } from './synthetic-order-store.mjs';

const worker = fileURLToPath(new URL('./reservation-race-worker.mjs', import.meta.url));
const resources = ['food', 'freezer', 'truck'];
const quantities = [5, 5, 1];
const items = resources.map((resourceId, i) => ({ resourceId, quantity: quantities[i] }));
const parties = { donor: 'donor', receiver: 'receiver', transport: 'transport' };
const bundle = id => ({ id, items, expiresAt: 400 });
function startDb(file) {
  const ledger = new ReservationLedger(file);
  resources.forEach((id, i) => ledger.seedResource(id, quantities[i]));
  return { ledger, orders: new SyntheticOrderStore(ledger) };
}
function run(file, operation, identifier = 'unused') {
  return new Promise((resolve, reject) => {
    const p = spawn(process.execPath, [worker, file, operation, identifier],
      { stdio: ['ignore', 'pipe', 'pipe'] });
    let out = '', err = '';
    p.stdout.on('data', chunk => { out += chunk; });
    p.stderr.on('data', chunk => { err += chunk; });
    p.on('error', reject);
    p.on('close', code => {
      if (code !== 0) return reject(Error('worker_failed: ' + err + out));
      try { resolve(JSON.parse(out.trim())); }
      catch { reject(Error('worker_invalid_result: ' + out + err)); }
    });
  });
}
async function isolated(name, fn) {
  const dir = mkdtempSync(join(tmpdir(), name));
  try { await fn(join(dir, 'shared.sqlite')); }
  finally { rmSync(dir, { recursive: true, force: true }); }
}
const capacities = ledger => resources.map(id => ledger.available(id));
function assertNoInfrastructureErrors(results) {
  const unexpected = results.filter(x => !x.ok && !['insufficient_capacity'].includes(x.error));
  assert.deepEqual(unexpected, [], 'no SQLite busy, corruption, or other unexpected errors');
}

test('six independent processes cannot double-claim food, freezer or truck after bundle expiry', async () =>
  isolated('maya-expiry-claim-', async file => {
    const { ledger } = startDb(file);
    assert.equal(ledger.reserveBundle({ id: 'old', items, expiresAt: 200 }, 100), true);
    ledger.close();
    const results = await Promise.all(Array.from({ length: 6 }, (_, i) => run(file, 'claim', 'new-' + i)));
    assertNoInfrastructureErrors(results);
    assert.equal(results.filter(x => x.value === true).length, 1, 'one and only one new bundle wins');
    const { ledger: check } = startDb(file);
    try {
      assert.deepEqual(capacities(check), [0, 0, 0]);
      assert.equal(check.db.prepare("SELECT state FROM bundles WHERE id='old'").get().state, 'released');
      assert.equal(check.db.prepare("SELECT COUNT(*) AS n FROM bundles WHERE state='active'").get().n, 1);
      assert.equal(check.reserveBundle({ id: 'old', items, expiresAt: 200 }, 100), false,
        'old idempotency key cannot resurrect after restart');
    } finally { check.close(); }
  }));

test('simultaneous order-expiry sweepers and cross-process claims conserve all capacities and receipts', async () =>
  isolated('maya-order-expiry-race-', async file => {
    const { ledger, orders } = startDb(file);
    orders.createReserved({ id: 'race-order', offerId: 'synthetic-offer',
      needId: 'synthetic-need', quantity: 5, parties, at: 100,
      bundle: { id: 'owned-old', items, expiresAt: 200 } });
    ledger.close();
    const [sweeper1, sweeper2, ...claims] = await Promise.all([
      run(file, 'expire-order'), run(file, 'expire-order'),
      ...Array.from({ length: 4 }, (_, i) => run(file, 'claim', 'reclaimed-' + i))
    ]);
    assert.deepEqual([sweeper1, sweeper2].filter(x => !x.ok), []);
    assert.equal(sweeper1.value + sweeper2.value, 1, 'one audited expiry even with two sweepers');
    assertNoInfrastructureErrors(claims);
    let winners = claims.filter(x => x.value === true).length;
    assert.ok(winners <= 1);
    const { ledger: check, orders: finalOrders } = startDb(file);
    try {
      if (!winners) {
        assert.equal(check.reserveBundle(bundle('after-sweep'), 201), true,
          'a later retry succeeds if all initial claimers lost race to the sweeper');
        winners = 1;
      }
      assert.equal(winners, 1);
      assert.deepEqual(capacities(check), [0, 0, 0]);
      assert.equal(finalOrders.get('race-order').state, 'expired');
      assert.equal(finalOrders.get('race-order').events.filter(x => x.kind === 'expired').length, 1);
      assert.equal(check.db.prepare("SELECT state FROM bundles WHERE id='owned-old'").get().state, 'released');
    } finally { check.close(); }
  }));

test('concurrent separate-process pickup versus cancellation has exactly one terminal winner', async () =>
  isolated('maya-cancel-pickup-race-', async file => {
    const { ledger, orders } = startDb(file);
    orders.createReserved({ id: 'race-order', offerId: 'synthetic-offer',
      needId: 'synthetic-need', quantity: 5, parties, at: 100,
      bundle: { id: 'held-trip', items, expiresAt: 300 } });
    for (const [role, actorId] of Object.entries(parties))
      orders.approve({ id: 'race-order', role, actorId, evidenceRef: 'SYN-' + role, at: 120 });
    ledger.close();
    const [pickup, cancel] = await Promise.all([run(file, 'pickup'), run(file, 'cancel')]);
    assert.equal([pickup, cancel].filter(x => x.ok).length, 1, 'exactly one successful terminal action');
    for (const result of [pickup, cancel]) {
      if (!result.ok) assert.ok(['pickup_requires_approvals', 'cancellation_requires_pre_pickup'].includes(result.error),
        'losing action fails because of state, not SQLite locking: ' + result.error);
    }
    const { ledger: check, orders: finalOrders } = startDb(file);
    try {
      const order = finalOrders.get('race-order');
      assert.equal(order.state, pickup.ok ? 'picked_up' : 'canceled');
      assert.equal(order.events.filter(x => ['picked_up', 'canceled'].includes(x.kind)).length, 1);
      assert.deepEqual(capacities(check), pickup.ok ? [0, 0, 0] : [5, 5, 1]);
      assert.equal(finalOrders.expireDue(301), 0, 'terminal order cannot later double-release');
      assert.deepEqual(capacities(check), pickup.ok ? [0, 0, 0] : [5, 5, 1]);
    } finally { check.close(); }
  }));
