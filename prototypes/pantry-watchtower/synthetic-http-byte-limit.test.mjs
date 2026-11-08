/**
 * Strict byte-size and error-response tests for the isolated fictional HTTP
 * server. The header-based principal resolver is SPOOFABLE and test-only.
 * Passing these checks does not establish a hosted authenticated pilot.
 */
import test from 'node:test';
import assert from 'node:assert/strict';
import { createLocalDemo } from './synthetic-local-demo-server.mjs';

const principals = {
  donor: { authenticated: true, tenantId: 'SYN-A', role: 'donor', actorId: 'fictional-donor' },
};
const resolver = req => principals[req.headers['x-syn-session']] ?? null;
const endpoint = '/api/tenant-order';
async function withGuardedDemo(fn) {
  const app = createLocalDemo({
    tenantGuardedOnly: true, resolveServerPrincipal: resolver, clock: () => 1000,
  });
  const url = await app.listen();
  try {
    app.act({ action: 'start' }); // only local test fixture may provision
    app.tenantGate.provisionForSyntheticTest('SYN-DEMO-ORDER', 'SYN-A', 1000);
    return await fn(url, app);
  } finally { await app.close(); }
}
async function send(url, body, who = 'donor', path = endpoint) {
  const response = await fetch(url + path, {
    method: 'POST', headers: { 'content-type': 'application/json',
      ...(who ? { 'x-syn-session': who } : {}) },
    body,
  });
  return [response.status, await response.json()];
}

test('oversized ASCII JSON returns stable HTTP 413 without changing the fictional order', async () => withGuardedDemo(async (url, app) => {
  const before = app.snapshot();
  const tooLarge = JSON.stringify({ action: 'approve', padding: 'x'.repeat(3000) });
  assert.ok(Buffer.byteLength(tooLarge) > 2048);
  const [status, payload] = await send(url, tooLarge);
  assert.equal(status, 413);
  assert.deepEqual(payload, { error: 'request_too_large' });
  assert.deepEqual(app.snapshot(), before);
  // The server must remain available after rejecting the oversized body.
  assert.equal((await send(url, JSON.stringify({ action: 'approve' })))[0], 200);
  assert.equal(app.orders.get('SYN-DEMO-ORDER').approvals.length, 1);
}));

test('size limit measures UTF-8 bytes, not JS characters, and exactly 2048 bytes is accepted', async () => withGuardedDemo(async (url, app) => {
  const before = app.snapshot();
  const multibyte = JSON.stringify({ action: 'approve', padding: '🍏'.repeat(600) });
  assert.ok(multibyte.length < 2048);
  assert.ok(Buffer.byteLength(multibyte) > 2048);
  assert.deepEqual(await send(url, multibyte), [413, { error: 'request_too_large' }]);
  assert.deepEqual(app.snapshot(), before);

  const template = JSON.stringify({ action: 'approve', padding: '' });
  const exact = JSON.stringify({ action: 'approve', padding: 'x'.repeat(2048 - Buffer.byteLength(template)) });
  assert.equal(Buffer.byteLength(exact), 2048);
  const [status, payload] = await send(url, exact);
  assert.equal(status, 200);
  assert.equal(payload.order.approvals.length, 1);
}));

test('unauthenticated oversized payload is denied before body validation and leaks no order', async () => withGuardedDemo(async (url, app) => {
  const before = app.snapshot();
  const [status, payload] = await send(url, JSON.stringify({ action: 'approve', padding: 'x'.repeat(3000) }), null);
  assert.equal(status, 403);
  assert.equal(payload.error, 'verified_principal_required');
  assert.equal(Object.hasOwn(payload, 'order'), false);
  assert.deepEqual(app.snapshot(), before);
}));

test('legacy demo endpoints remain closed even when sent oversized JSON in guarded-only mode', async () => withGuardedDemo(async (url, app) => {
  const before = app.snapshot();
  const [status, payload] = await send(url, JSON.stringify({ action: 'start', padding: 'x'.repeat(3000) }), 'donor', '/api/action');
  assert.equal(status, 403);
  assert.deepEqual(payload, { error: 'untrusted_demo_routes_disabled' });
  assert.deepEqual(app.snapshot(), before);
}));
