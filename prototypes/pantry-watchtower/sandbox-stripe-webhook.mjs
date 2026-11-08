/**
 * Sandbox-only Stripe webhook verification and durable replay ledger.
 * Inert: records minimal test-mode event metadata, NEVER settles Maya orders,
 * sends messages, contacts Stripe, stores card/email payloads, or accepts money.
 * The Stripe webhook secret is supplied by an external test-only configuration;
 * a whsec_ prefix alone cannot establish the account's mode.
 */
import { createHash, createHmac, timingSafeEqual } from 'node:crypto';

const MAX_BODY = 65536;
const MAX_HEADER = 512;
const TOLERANCE_SECONDS = 300;
const TYPES = new Set([
  'checkout.session.completed', 'payment_intent.succeeded',
  'payment_intent.payment_failed', 'charge.refunded',
]);
const demand = (ok, code) => { if (!ok) throw Error(code); };
const safeId = value => typeof value === 'string' && /^[A-Za-z0-9_-]{6,180}$/.test(value);
const isRecord = value => !!value && typeof value === 'object' && !Array.isArray(value);

/** Stripe signs the *raw bytes*, not JSON reserialized by the application. */
export function verifyTestWebhook({ rawBody, signatureHeader, webhookSecret, nowSeconds = Math.floor(Date.now() / 1000) }) {
  demand(typeof webhookSecret === 'string' && /^whsec_[A-Za-z0-9_+-]{8,}$/.test(webhookSecret), 'test_webhook_secret_required');
  demand(Number.isSafeInteger(nowSeconds) && nowSeconds >= 0, 'invalid_clock');
  demand(typeof rawBody === 'string' || Buffer.isBuffer(rawBody), 'invalid_raw_body');
  const raw = Buffer.isBuffer(rawBody) ? rawBody : Buffer.from(rawBody, 'utf8');
  demand(raw.length > 0 && raw.length <= MAX_BODY, 'webhook_body_limit');
  demand(typeof signatureHeader === 'string' && signatureHeader.length > 0 &&
    signatureHeader.length <= MAX_HEADER, 'invalid_stripe_signature');
  const pieces = signatureHeader.split(',');
  demand(pieces.length <= 16, 'invalid_stripe_signature');
  const timestamps = [], digests = [];
  for (const segment of pieces) {
    const part = segment.trim();
    if (/^t=\d+$/.test(part)) timestamps.push(part.slice(2));
    else if (/^v1=[a-fA-F0-9]{64}$/.test(part)) digests.push(part.slice(3).toLowerCase());
    else if (!/^[A-Za-z0-9]+=[A-Za-z0-9]+$/.test(part)) throw Error('invalid_stripe_signature');
  }
  demand(timestamps.length === 1 && digests.length > 0, 'invalid_stripe_signature');
  const timestamp = Number(timestamps[0]);
  demand(Number.isSafeInteger(timestamp) && timestamp >= 0 &&
    Math.abs(nowSeconds - timestamp) <= TOLERANCE_SECONDS, 'webhook_timestamp_out_of_window');
  const expected = createHmac('sha256', webhookSecret)
    .update(String(timestamp)).update('.').update(raw).digest();
  const valid = digests.some(hex => {
    const provided = Buffer.from(hex, 'hex');
    return provided.length === expected.length && timingSafeEqual(provided, expected);
  });
  demand(valid, 'invalid_stripe_signature');
  let event;
  try { event = JSON.parse(raw.toString('utf8')); }
  catch { throw Error('invalid_signed_json'); }
  demand(isRecord(event) && event.livemode === false, 'test_mode_event_required');
  demand(safeId(event.id) && event.id.startsWith('evt_'), 'invalid_event_id');
  demand(TYPES.has(event.type), 'unsupported_test_event_type');
  demand(Number.isSafeInteger(event.created) && event.created >= 0, 'invalid_event_created');
  demand(isRecord(event.data) && isRecord(event.data.object), 'invalid_event_object');
  const object = event.data.object;
  demand(safeId(object.id), 'invalid_event_object');
  demand(object.livemode === undefined || object.livemode === false, 'test_mode_object_required');
  return Object.freeze({
    id: event.id, type: event.type, objectId: object.id,
    created: event.created, signatureTimestamp: timestamp,
    sha256: createHash('sha256').update(raw).digest('hex'),
    testMode: true, actionable: false,
  });
}

/** Pass a dedicated SQLite connection; this is an inert inbox, not a payment handler. */
export class SandboxStripeWebhookInbox {
  constructor(db) {
    demand(db && typeof db.exec === 'function' && typeof db.prepare === 'function', 'sqlite_connection_required');
    this.db = db;
    db.exec([
      'PRAGMA foreign_keys=ON;',
      'PRAGMA busy_timeout=5000;',
      'CREATE TABLE IF NOT EXISTS sandbox_stripe_observations (',
      'event_id TEXT PRIMARY KEY, payload_sha256 TEXT NOT NULL, event_type TEXT NOT NULL,',
      'object_id TEXT NOT NULL, provider_created INTEGER NOT NULL,',
      'first_signed_at INTEGER NOT NULL, received_at INTEGER NOT NULL);',
      "CREATE TRIGGER IF NOT EXISTS sandbox_stripe_observations_no_update BEFORE UPDATE ON sandbox_stripe_observations BEGIN SELECT RAISE(ABORT,'sandbox_event_append_only'); END;",
      "CREATE TRIGGER IF NOT EXISTS sandbox_stripe_observations_no_delete BEFORE DELETE ON sandbox_stripe_observations BEGIN SELECT RAISE(ABORT,'sandbox_event_append_only'); END;",
    ].join('\n'));
  }
  observe(args) {
    const verified = verifyTestWebhook(args);
    this.db.exec('BEGIN IMMEDIATE');
    try {
      const old = this.db.prepare(
        'SELECT payload_sha256,event_type,object_id FROM sandbox_stripe_observations WHERE event_id=?'
      ).get(verified.id);
      if (old) {
        demand(old.payload_sha256 === verified.sha256 &&
          old.event_type === verified.type && old.object_id === verified.objectId,
          'stripe_event_id_collision');
        this.db.exec('COMMIT');
        return { ...verified, duplicate: true, applied: false };
      }
      this.db.prepare(
        'INSERT INTO sandbox_stripe_observations(event_id,payload_sha256,event_type,object_id,provider_created,first_signed_at,received_at) VALUES(?,?,?,?,?,?,?)'
      ).run(verified.id, verified.sha256, verified.type, verified.objectId,
        verified.created, verified.signatureTimestamp, args.nowSeconds ?? Math.floor(Date.now() / 1000));
      this.db.exec('COMMIT');
      return { ...verified, duplicate: false, applied: false };
    } catch (e) {
      try { this.db.exec('ROLLBACK'); } catch {}
      throw e;
    }
  }
  count() {
    return this.db.prepare('SELECT COUNT(*) AS n FROM sandbox_stripe_observations').get().n;
  }
}
