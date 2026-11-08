/**
 * LOCAL, opt-in sandbox Stripe webhook HTTP receiver. No customer or production deployment.
 * Records only test-mode event metadata; DOES NOT fulfill Maya orders or change balances.
 * Never place live Stripe credentials in this process. Confirm test-mode in Stripe first.
 */
import http from 'node:http';
import { DatabaseSync } from 'node:sqlite';
import { SandboxStripeWebhookInbox } from './sandbox-stripe-webhook.mjs';

const HOST = '127.0.0.1';
const ROUTE = '/sandbox/stripe/webhook';
const MAX_BODY = 65536;
const HEADERS = Object.freeze({
  'Cache-Control': 'no-store',
  'X-Content-Type-Options': 'nosniff',
  'Referrer-Policy': 'no-referrer',
});
function respond(res, status, value) {
  const body = JSON.stringify(value);
  res.writeHead(status, { ...HEADERS, 'Content-Type': 'application/json; charset=utf-8', 'Content-Length': Buffer.byteLength(body) });
  res.end(body);
}
async function rawBytes(req) {
  const parts = [];
  let bytes = 0;
  for await (const part of req) {
    bytes += part.length;
    if (bytes > MAX_BODY) throw Error('webhook_body_limit');
    parts.push(part);
  }
  if (bytes === 0) throw Error('webhook_body_limit');
  return Buffer.concat(parts);
}
/**
 * Explicit test-mode acknowledgement is required; whsec_ alone does not
 * distinguish a test webhook secret from a live one.
 */
export function createSandboxLocalReceiver({
  filename = ':memory:', webhookSecret, accountMode, clock = () => Math.floor(Date.now() / 1000),
} = {}) {
  if (accountMode !== 'confirmed-test') throw Error('confirmed_test_account_required');
  if (typeof webhookSecret !== 'string' || !/^whsec_[A-Za-z0-9_+-]{8,}$/.test(webhookSecret))
    throw Error('test_webhook_secret_required');
  const db = new DatabaseSync(filename);
  if (filename !== ':memory:') db.exec('PRAGMA journal_mode=WAL;');
  const inbox = new SandboxStripeWebhookInbox(db);
  const server = http.createServer(async (req, res) => {
    try {
      const host = req.headers.host ?? '';
      if (!/^127\\.0\\.0\\.1:\\d{1,5}$/.test(host)) return respond(res, 403, { error: 'loopback_host_required' });
      if (req.method !== 'POST' || req.url !== ROUTE) return respond(res, 404, { error: 'not_found' });
      if (!/^application\\/json(?:\\s*;|$)/i.test(req.headers['content-type'] ?? ''))
        return respond(res, 415, { error: 'json_required' });
      const bytes = await rawBytes(req);
      const observed = inbox.observe({
        rawBody: bytes,
        signatureHeader: req.headers['stripe-signature'],
        webhookSecret,
        nowSeconds: clock(),
      });
      respond(res, 200, { received: true, duplicate: observed.duplicate, applied: false, testMode: true });
    } catch (err) {
      const code = err?.message;
      const rejected = new Set([
        'invalid_stripe_signature', 'webhook_timestamp_out_of_window', 'invalid_signed_json',
        'test_mode_event_required', 'test_mode_object_required', 'invalid_event_id',
        'invalid_event_object', 'invalid_event_created', 'unsupported_test_event_type',
        'invalid_raw_body', 'invalid_clock', 'webhook_body_limit',
      ]);
      if (code === 'webhook_body_limit') return respond(res, 413, { error: code });
      if (code === 'stripe_event_id_collision') return respond(res, 409, { error: code });
      if (rejected.has(code)) return respond(res, 400, { error: code });
      // Do not reflect SQLite internals or provider data.
      respond(res, 503, { error: 'sandbox_observation_unavailable' });
    }
  });
  return {
    server, inbox,
    async listen(port = 0) {
      await new Promise((resolve, reject) => {
        server.once('error', reject);
        server.listen(port, HOST, resolve);
      });
      return 'http://' + HOST + ':' + server.address().port;
    },
    async close() {
      if (server.listening) await new Promise((resolve, reject) =>
        server.close(error => error ? reject(error) : resolve()));
      db.close();
    },
  };
}
if (process.argv[1] && import.meta.url === new URL('file://' + process.argv[1]).href) {
  if (process.env.MAYA_STRIPE_TEST_MODE_CONFIRMED !== 'yes') {
    console.error('Refusing receiver startup without explicit Stripe TEST-mode acknowledgement.');
    process.exitCode = 1;
  } else {
    try {
      const app = createSandboxLocalReceiver({
        filename: process.env.MAYA_STRIPE_SANDBOX_SQLITE || ':memory:',
        webhookSecret: process.env.MAYA_STRIPE_TEST_WEBHOOK_SECRET,
        accountMode: 'confirmed-test',
      });
      app.listen(Number(process.env.MAYA_SANDBOX_WEBHOOK_PORT || 8790))
        .then(url => console.log('Inert TEST-mode Stripe webhook receiver at ' + url))
        .catch(() => { console.error('Unable to start sandbox receiver.'); process.exitCode = 1; });
    } catch {
      console.error('Missing or invalid sandbox webhook configuration.');
      process.exitCode = 1;
    }
  }
}
