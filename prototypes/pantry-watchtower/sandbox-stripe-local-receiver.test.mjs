import test from 'node:test';
import assert from 'node:assert/strict';
import { createHmac } from 'node:crypto';
import { mkdtempSync, rmSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import http from 'node:http';
import { createSandboxLocalReceiver } from './sandbox-stripe-local-receiver.mjs';

const SECRET = 'whsec_test_http_fixture_1234';
const NOW = 1_700_000_000;
function signed({ type = 'checkout.session.completed', id = 'evt_test_http_0001', livemode = false,
  objectMode = false, email = 'do-not-store@example.invalid' } = {}, at = NOW) {
  const raw = JSON.stringify({
    id, type, livemode, created: NOW - 20,
    data: { object: { id: 'cs_test_http_0001', livemode: objectMode, customer_email: email } },
  });
  const digest = createHmac('sha256', SECRET).update(String(at)).update('.').update(raw).digest('hex');
  return { raw, signature: 't=' + at + ',v1=' + digest };
}
async function withReceiver(action, settings = {}) {
  const app = createSandboxLocalReceiver({
    webhookSecret: SECRET, accountMode: 'confirmed-test', clock: () => NOW, ...settings,
  });
  const base = await app.listen();
  try { await action(base, app); }
  finally { await app.close(); }
}
async function post(base, fixture, options = {}) {
  const res = await fetch(base + '/sandbox/stripe/webhook', {
    method: 'POST',
    headers: {
      'content-type': 'application/json',
      'stripe-signature': fixture.signature,
      ...options.headers,
    },
    body: fixture.raw,
  });
  return { status: res.status, body: await res.json() };
}
test('refuses startup unless caller explicitly confirms TEST account mode and provides secret', () => {
  assert.throws(() => createSandboxLocalReceiver({ webhookSecret: SECRET }), /confirmed_test_account_required/);
  assert.throws(() => createSandboxLocalReceiver({ webhookSecret: SECRET, accountMode: 'live' }), /confirmed_test_account_required/);
  assert.throws(() => createSandboxLocalReceiver({ accountMode: 'confirmed-test', webhookSecret: '' }), /test_webhook_secret_required/);
});
test('signed test event reaches SQLite over real loopback HTTP, retry returns 200 with no side effects', async () =>
  withReceiver(async (base, app) => {
    const f = signed();
    assert.deepEqual(await post(base, f), { status: 200,
      body: { received: true, duplicate: false, applied: false, testMode: true } });
    assert.equal(app.inbox.count(), 1);
    assert.deepEqual(await post(base, f), { status: 200,
      body: { received: true, duplicate: true, applied: false, testMode: true } });
    assert.equal(app.inbox.count(), 1);
    assert.doesNotMatch(JSON.stringify(app.inbox.db.prepare('SELECT * FROM sandbox_stripe_observations').all()),
      /do-not-store|customer_email/);
    assert.equal(app.inbox.db.prepare("SELECT COUNT(*) AS n FROM sqlite_master WHERE name='synthetic_orders'").get().n, 0);
  }));
test('bad signature, signed live events, future timestamps and payload changes do not enter inbox', async () =>
  withReceiver(async (base, app) => {
    const f = signed();
    assert.equal((await post(base, { ...f, raw: f.raw + ' ' })).status, 400);
    assert.equal((await post(base, signed({ livemode: true }))).status, 400);
    assert.equal((await post(base, signed({ objectMode: true }))).status, 400);
    assert.equal((await post(base, signed({}, NOW + 400))).status, 400);
    assert.equal(app.inbox.count(), 0);
  }));
test('event ID reuse with different verified payload fails without overwriting first', async () =>
  withReceiver(async (base, app) => {
    assert.equal((await post(base, signed())).status, 200);
    assert.equal((await post(base, signed({ email: 'different@example.invalid' }))).status, 409);
    assert.equal(app.inbox.count(), 1);
  }));
test('rejects wrong paths, methods, content type, Host spoof and oversized raw bodies', async () =>
  withReceiver(async (base, app) => {
    assert.equal((await fetch(base + '/sandbox/stripe/webhook')).status, 404);
    assert.equal((await fetch(base + '/other', { method: 'POST' })).status, 404);
    assert.equal((await post(base, signed(), { headers: { 'content-type': 'text/plain' } })).status, 415);
    const huge = signed();
    huge.raw = 'x'.repeat(65537);
    assert.equal((await post(base, huge)).status, 413);
    const hostResult = await new Promise((resolve, reject) => {
      const url = new URL(base);
      const req = http.request({ hostname: '127.0.0.1', port: url.port,
        path: '/sandbox/stripe/webhook', method: 'POST', headers: { Host: 'evil.example:88' } }, res => {
        res.resume(); res.on('end', () => resolve(res.statusCode));
      });
      req.on('error', reject); req.end();
    });
    assert.equal(hostResult, 403);
    assert.equal(app.inbox.count(), 0);
  }));
test('loopback signed event deduplication persists after SQLite application restart', async () => {
  const dir = mkdtempSync(join(tmpdir(), 'maya-http-sandbox-'));
  const filename = join(dir, 'observations.sqlite');
  try {
    await withReceiver(async (base, app) => {
      assert.equal((await post(base, signed())).status, 200);
      assert.equal(app.inbox.count(), 1);
    }, { filename });
    await withReceiver(async (base, app) => {
      const replay = await post(base, signed());
      assert.equal(replay.status, 200);
      assert.equal(replay.body.duplicate, true);
      assert.equal(app.inbox.count(), 1);
    }, { filename });
  } finally { rmSync(dir, { recursive: true, force: true }); }
});
