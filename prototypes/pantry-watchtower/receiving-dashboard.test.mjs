import test from 'node:test';
import assert from 'node:assert/strict';
import { createLocalDemo } from './synthetic-local-demo-server.mjs';
import { createReceivingDashboard } from './receiving-dashboard.mjs';

test('receiving changes are shared over HTTP and duplicate receipts do not count twice', async () => {
  const demo = createLocalDemo();
  const url = await demo.listen();
  try {
    const state = () => fetch(url + '/api/receiving').then(r => r.json());
    const act = action => fetch(url + '/api/receiving/fixture', {
      method: 'POST', headers: { 'content-type': 'application/json' }, body: JSON.stringify({ action })
    }).then(r => r.json());
    assert.equal((await state()).capacity.chilled.available, 25);
    await act('outage');
    const held = await state();
    assert.equal(held.capacity.chilled.available, 0);
    assert.equal(held.capacity.chilled.reserved, 15);
    assert.equal(held.summary.held, 1);
    await act('cancel');
    assert.equal((await state()).capacity.ambient.available, 25);
    const receipt = await act('short');
    assert.equal(receipt.summary.received, 12);
    assert.equal(receipt.summary.short, 3);
    assert.equal(receipt.capacity.ambient.occupied, 72);
    assert.equal(receipt.capacity.ambient.reserved, 0);
    assert.equal(receipt.capacity.ambient.available, 28);
    const duplicate = await act('duplicate');
    assert.equal(duplicate.outcome, 'duplicate');
    assert.equal(duplicate.revision, receipt.revision);
    assert.deepEqual(duplicate.summary, receipt.summary);
    const sponsor = await fetch(url + '/api/receiving/sponsor').then(r => r.json());
    assert.deepEqual(Object.keys(sponsor).sort(), ['revision', 'summary', 'synthetic', 'updatedAt']);
    assert.deepEqual(sponsor.summary, receipt.summary);
    assert.equal((await fetch(url + '/receiving')).status, 200);
    const blocked = await fetch(url + '/api/receiving/fixture', { method: 'POST', headers: { origin: 'https://outside.invalid' } });
    assert.equal(blocked.status, 403);
  } finally { await demo.close(); }
});

test('accept reserves space, decline closes, and a pending hold reserves nothing', () => {
  for (const [action, state, remaining] of [
    ['accept', 'accepted', 10], ['decline', 'declined', 15], ['hold', 'held', 15]
  ]) {
    const dashboard = createReceivingDashboard(() => 1);
    const after = dashboard.applyFixture(action);
    assert.equal(after.shipments.find(s => s.id === 'SYN-GRAINS').state, state);
    assert.equal(after.capacity.ambient.available, remaining);
  }
});
