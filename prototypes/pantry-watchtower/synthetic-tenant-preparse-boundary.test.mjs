/**
 * Guarded local HTTP must authorize its server-injected fictional principal
 * BEFORE content-type and JSON validation. These header fixtures are
 * deliberately SPOOFABLE; they are NOT real sessions or deployable auth.
 */
import test from 'node:test';
import assert from 'node:assert/strict';
import { createLocalDemo } from './synthetic-local-demo-server.mjs';

const fixtures = {
  donor: { authenticated: true, tenantId: 'SYN-A', actorId: 'fictional-donor', role: 'donor' },
  receiver: { authenticated: true, tenantId: 'SYN-A', actorId: 'fictional-receiver', role: 'receiver' },
  otherTenant: { authenticated: true, tenantId: 'SYN-B', actorId: 'fictional-donor', role: 'donor' },
  wrongActor: { authenticated: true, tenantId: 'SYN-A', actorId: 'SYN-impostor', role: 'donor' },
};
const resolveServerPrincipal = req => fixtures[req.headers['x-syn-session']] ?? null;
async function post(url, who, body, contentType = 'application/json') {
  const response = await fetch(url + '/api/tenant-order', {
    method: 'POST',
    headers: { ...(who ? { 'x-syn-session': who } : {}), 'content-type': contentType },
    body,
  });
  return [response.status, await response.json()];
}

test('guarded POST denies missing or mismatched principal BEFORE malformed body or content type', async () => {
  const app = createLocalDemo({ tenantGuardedOnly: true, resolveServerPrincipal, clock: () => 1000 });
  const url = await app.listen();
  try {
    // Provisioning happens only in the local test fixture, never over HTTP.
    app.act({ action: 'start' });
    app.tenantGate.provisionForSyntheticTest('SYN-DEMO-ORDER', 'SYN-A', 1000);
    const before = app.snapshot();
    const requests = [
      [null, '{"action":', 'application/json', 'verified_principal_required'],
      ['otherTenant', '{"action":"approve"}', 'text/plain', 'tenant_scope_denied'],
      ['wrongActor', '{"action":', 'application/json', 'actor_scope_denied'],
      [null, '{"action":"approve"}', 'text/plain', 'verified_principal_required'],
    ];
    const results = await Promise.all(requests.map(async ([who,body,type,code]) => {
      const [status, response] = await post(url, who, body, type);
      assert.equal(status, 403);
      assert.equal(response.error, code);
      assert.equal(Object.hasOwn(response, 'order'), false);
    }));
    assert.equal(results.length, 4);
    assert.deepEqual(app.snapshot(), before);
  } finally { await app.close(); }
});

test('authorized fictional participant receives ordinary payload errors and can still approve', async () => {
  const app = createLocalDemo({ tenantGuardedOnly: true, resolveServerPrincipal, clock: () => 1000 });
  const url = await app.listen();
  try {
    app.act({ action: 'start' });
    app.tenantGate.provisionForSyntheticTest('SYN-DEMO-ORDER', 'SYN-A', 1000);
    const before = app.snapshot();
    assert.deepEqual(await post(url, 'donor', '{"action":"approve"}', 'text/plain'),
      [415, {error:'json_required'}]);
    assert.deepEqual(await post(url, 'donor', '{"action":'),
      [409, {error:'invalid_json'}]);
    assert.deepEqual(app.snapshot(), before);
    const [status, response] = await post(url, 'donor', '{"action":"approve"}');
    assert.equal(status, 200);
    assert.equal(response.order.approvals.length, 1);
    assert.equal(response.order.approvals[0].actorId, 'fictional-donor');
  } finally { await app.close(); }
});
