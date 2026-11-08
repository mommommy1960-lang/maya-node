import test from 'node:test';
import assert from 'node:assert/strict';
import { createHmac } from 'node:crypto';
import { DatabaseSync } from 'node:sqlite';
import { mkdtempSync, rmSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { verifyTestWebhook, SandboxStripeWebhookInbox } from './sandbox-stripe-webhook.mjs';

const SECRET = 'whsec_syntheticsecret12345', NOW = 1_700_000_000;
function fixture(overrides = {}, timestamp = NOW) {
  const event = {
    id: 'evt_sandbox_000001', type: 'payment_intent.succeeded',
    livemode: false, created: NOW - 30,
    data: { object: { id: 'pi_sandbox_000001', livemode: false,
      receipt_email: 'never-persist@example.invalid' } },
    ...overrides,
  };
  const rawBody = JSON.stringify(event);
  const digest = createHmac('sha256', SECRET)
    .update(String(timestamp)).update('.').update(rawBody).digest('hex');
  return { rawBody, signatureHeader: 't=' + timestamp + ',v1=' + digest,
    webhookSecret: SECRET, nowSeconds: NOW };
}
function inbox() {
  const db = new DatabaseSync(':memory:');
  return { db, i: new SandboxStripeWebhookInbox(db), close: () => db.close() };
}

test('correctly signed, test-only raw payload yields metadata, not a payment action', () => {
  const verified = verifyTestWebhook(fixture());
  assert.equal(verified.id, 'evt_sandbox_000001');
  assert.equal(verified.type, 'payment_intent.succeeded');
  assert.equal(verified.objectId, 'pi_sandbox_000001');
  assert.equal(verified.testMode, true);
  assert.equal(verified.actionable, false);
  assert.match(verified.sha256, /^[a-f0-9]{64}$/);
  assert.doesNotMatch(JSON.stringify(verified), /never-persist/);
});

test('rejects tampering, malformed signatures and missing signing secret', () => {
  const ok = fixture();
  assert.throws(() => verifyTestWebhook({ ...ok, rawBody: ok.rawBody + ' ' }), /invalid_stripe_signature/);
  assert.throws(() => verifyTestWebhook({ ...ok, signatureHeader: 't=' + NOW + ',v1=' + '0'.repeat(64) }), /invalid_stripe_signature/);
  assert.throws(() => verifyTestWebhook({ ...ok, signatureHeader: 'v1=' + '0'.repeat(64) }), /invalid_stripe_signature/);
  assert.throws(() => verifyTestWebhook({ ...ok, signatureHeader: ok.signatureHeader + ',t=2' }), /invalid_stripe_signature/);
  assert.throws(() => verifyTestWebhook({ ...ok, webhookSecret: undefined }), /test_webhook_secret_required/);
});

test('rejects stale and future signatures, accepting exact edge only', () => {
  assert.throws(() => verifyTestWebhook(fixture({}, NOW - 301)), /webhook_timestamp_out_of_window/);
  assert.throws(() => verifyTestWebhook(fixture({}, NOW + 301)), /webhook_timestamp_out_of_window/);
  assert.equal(verifyTestWebhook(fixture({}, NOW - 300)).testMode, true);
  assert.equal(verifyTestWebhook(fixture({}, NOW + 300)).testMode, true);
  assert.throws(() => verifyTestWebhook({ ...fixture(), nowSeconds: -1 }), /invalid_clock/);
});

test('rejects signed live-mode envelopes and live-mode objects', () => {
  assert.throws(() => verifyTestWebhook(fixture({ livemode: true })), /test_mode_event_required/);
  assert.throws(() => verifyTestWebhook(fixture({
    data: { object: { id: 'pi_sandbox_000001', livemode: true } },
  })), /test_mode_object_required/);
});

test('rejects signed unsupported event shapes and event types', () => {
  assert.throws(() => verifyTestWebhook(fixture({ type: 'customer.created' })), /unsupported_test_event_type/);
  assert.throws(() => verifyTestWebhook(fixture({ id: 'id' })), /invalid_event_id/);
  assert.throws(() => verifyTestWebhook(fixture({ created: -8 })), /invalid_event_created/);
  assert.throws(() => verifyTestWebhook(fixture({ data: null })), /invalid_event_object/);
  assert.throws(() => verifyTestWebhook(fixture({ data: { object: { id: '../bad' } } })), /invalid_event_object/);
});

test('rejects oversized bodies before parsing or writing anything', () => {
  const f = fixture();
  assert.throws(() => verifyTestWebhook({ ...f, rawBody: 'x'.repeat(65537) }), /webhook_body_limit/);
  assert.throws(() => verifyTestWebhook({ ...f, rawBody: '' }), /webhook_body_limit/);
});

test('records one test observation; retries are inert with no financial effects', () => {
  const a = inbox();
  try {
    const first = a.i.observe(fixture());
    assert.equal(first.duplicate, false);
    assert.equal(first.applied, false);
    assert.equal(a.i.count(), 1);
    const again = a.i.observe(fixture());
    assert.equal(again.duplicate, true);
    assert.equal(again.applied, false);
    assert.equal(a.i.count(), 1);
    assert.doesNotMatch(JSON.stringify(a.db.prepare('SELECT * FROM sandbox_stripe_observations').all()),
      /never-persist|receipt_email/);
  } finally { a.close(); }
});

test('freshly signed retry is deduplicated even if Stripe retries with a new signature timestamp', () => {
  const a = inbox();
  try {
    assert.equal(a.i.observe(fixture({}, NOW - 20)).duplicate, false);
    assert.equal(a.i.observe(fixture({}, NOW + 20)).duplicate, true);
    assert.equal(a.i.count(), 1);
  } finally { a.close(); }
});

test('same event ID with changed signed payload is rejected rather than overwritten', () => {
  const a = inbox();
  try {
    a.i.observe(fixture());
    assert.throws(() => a.i.observe(fixture({
      data: { object: { id: 'pi_sandbox_changed', livemode: false } },
    })), /stripe_event_id_collision/);
    assert.equal(a.i.count(), 1);
    assert.equal(a.db.prepare('SELECT object_id FROM sandbox_stripe_observations').get().object_id,
      'pi_sandbox_000001');
  } finally { a.close(); }
});

test('inbox observations are append-only even with direct SQL statements', () => {
  const a = inbox();
  try {
    a.i.observe(fixture());
    assert.throws(() => a.db.exec("UPDATE sandbox_stripe_observations SET event_type='other'"),
      /sandbox_event_append_only/);
    assert.throws(() => a.db.exec('DELETE FROM sandbox_stripe_observations'),
      /sandbox_event_append_only/);
    assert.equal(a.i.count(), 1);
  } finally { a.close(); }
});

test('cross-connection retries and database restart preserve the replay barrier', () => {
  const dir = mkdtempSync(join(tmpdir(), 'maya-sandbox-stripe-'));
  const file = join(dir, 'stripe-test-observations.sqlite');
  try {
    const a = new DatabaseSync(file);
    const b = new DatabaseSync(file);
    try {
      const first = new SandboxStripeWebhookInbox(a);
      const second = new SandboxStripeWebhookInbox(b);
      assert.equal(first.observe(fixture()).duplicate, false);
      assert.equal(second.observe(fixture()).duplicate, true);
      assert.equal(second.count(), 1);
    } finally { a.close(); b.close(); }
    const reopened = new DatabaseSync(file);
    try {
      const restored = new SandboxStripeWebhookInbox(reopened);
      assert.equal(restored.observe(fixture()).duplicate, true);
      assert.equal(restored.count(), 1);
    } finally { reopened.close(); }
  } finally { rmSync(dir, { recursive: true, force: true }); }
});

test('distinct allowed payment lifecycle observations remain unlinked to any Maya order', () => {
  const a = inbox();
  try {
    const types = ['checkout.session.completed', 'payment_intent.payment_failed', 'charge.refunded'];
    for (const [n, type] of types.entries()) {
      const result = a.i.observe(fixture({
        id: 'evt_test_' + (1000 + n), type,
        data: { object: { id: 'ch_test_' + (1000 + n), livemode: false } },
      }));
      assert.equal(result.applied, false);
    }
    assert.equal(a.i.count(), 3);
    assert.equal(a.db.prepare("SELECT COUNT(*) AS n FROM sqlite_master WHERE name='synthetic_orders'").get().n, 0);
  } finally { a.close(); }
});
