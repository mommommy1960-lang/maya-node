/**
 * Loopback-only, fictional Maya pantry order journey.
 * No production/hosted integration, real identities, records, dispatch, notifications, or billing.
 * Start: node prototypes/pantry-watchtower/synthetic-local-demo-server.mjs
 */
import http from 'node:http';
import { AsyncLocalStorage } from 'node:async_hooks';
import { readFile } from 'node:fs/promises';
import { fileURLToPath } from 'node:url';
import { dirname, join } from 'node:path';
import { ReservationLedger } from './reservation-ledger.mjs';
import { SyntheticOrderStore } from './synthetic-order-store.mjs';
import { SyntheticDeliverySettlement } from './synthetic-delivery-settlement.mjs';
import { SyntheticCommercialRehearsal } from './synthetic-commercial-rehearsal.mjs';
import { SyntheticTenantOrderGate } from './synthetic-tenant-order-gate.mjs';

const here = dirname(fileURLToPath(import.meta.url));
const HOST = '127.0.0.1';
const ORDER = 'SYN-DEMO-ORDER';
const ROLES = Object.freeze({ donor: 'fictional-donor', receiver: 'fictional-receiver', transport: 'fictional-transporter' });
const RESOURCE = Object.freeze({ food: 'SYN-FOOD', cold: 'SYN-COLD', truck: 'SYN-TRUCK' });
const ACTIONS = new Set(['start', 'approve', 'quote', 'accept-terms', 'mock-decline', 'mock-authorize', 'pickup', 'deliver', 'document-exception', 'mock-capture', 'mock-refund', 'cancel']);
const FILES = Object.freeze({
  '/': ['synthetic-journey.html', 'text/html; charset=utf-8'],
  '/synthetic-journey-client.mjs': ['synthetic-journey-client.mjs', 'text/javascript; charset=utf-8'],
});
const HEADERS = Object.freeze({
  'Cache-Control': 'no-store', 'X-Content-Type-Options': 'nosniff',
  'Referrer-Policy': 'no-referrer', 'X-Frame-Options': 'DENY',
  'Content-Security-Policy': "default-src 'none'; script-src 'self'; style-src 'unsafe-inline'; connect-src 'self'; base-uri 'none'; frame-ancestors 'none'; form-action 'none'",
});
function json(res, status, value) {
  const body = JSON.stringify(value);
  res.writeHead(status, { ...HEADERS, 'Content-Type': 'application/json; charset=utf-8', 'Content-Length': Buffer.byteLength(body) });
  res.end(body);
}
function readJson(req) {
  return new Promise((resolve, reject) => {
    let body = '';
    req.on('data', chunk => {
      body += chunk;
      if (body.length > 2048) { reject(Error('request_too_large')); req.destroy(); }
    });
    req.on('end', () => {
      try { const data = JSON.parse(body); if (!data || typeof data !== 'object' || Array.isArray(data)) throw Error(); resolve(data); }
      catch { reject(Error('invalid_json')); }
    });
    req.on('error', reject);
  });
}

export function createLocalDemo({ filename = ':memory:', clock = () => Date.now(), resolveServerPrincipal = null } = {}) {
  // This resolver is a TEST HARNESS injection, not user authentication.
  // Neither browser-supplied identity fields nor role selectors are credentials.
  if (resolveServerPrincipal !== null && typeof resolveServerPrincipal !== 'function')
    throw Error('invalid_test_principal_resolver');
  const ledger = new ReservationLedger(filename);
  const orders = new SyntheticOrderStore(ledger);
  const delivery = new SyntheticDeliverySettlement(orders);
  const commercial = new SyntheticCommercialRehearsal(orders);
  // AsyncLocalStorage keeps independent concurrent HTTP test principals isolated.
  // No browser route can register/provision its own tenant. Provisioning is local
  // test-fixture code only, and this separate route must never be deployed as auth.
  const requestPrincipal = new AsyncLocalStorage();
  const tenantGate = new SyntheticTenantOrderGate(orders, () => requestPrincipal.getStore());
  const guardedErrors = new Set(['tenant_route_unavailable', 'verified_principal_required',
    'tenant_scope_denied', 'role_denied', 'actor_scope_denied',
    'client_identity_claim_denied', 'unknown_tenant_action']);
  for (const id of Object.values(RESOURCE)) ledger.seedResource(id, 12);
  const snapshot = () => {
    const order = orders.get(ORDER);
    return { synthetic: true, live: false, dataLabel: 'FICTIONAL ONLY', order,
      receipt: delivery.getReceipt(ORDER),
      commercial: commercial.get(ORDER),
      capacity: Object.fromEntries(Object.entries(RESOURCE).map(([name, id]) => [name, ledger.available(id)])),
      permissions: 'Demo buttons impersonate fictional actors; payment states are local fake ledger entries, NOT a Stripe sandbox or any real financial transaction.',
    };
  };
  function act(input) {
    if (!ACTIONS.has(input.action)) throw Error('unknown_action');
    const now = clock();
    if (!Number.isSafeInteger(now) || now < 0) throw Error('invalid_demo_clock');
    if (input.action === 'start') {
      if (orders.get(ORDER)) throw Error('demo_already_started');
      orders.createReserved({ id: ORDER, offerId: 'SYN-OFFER', needId: 'SYN-NEED', quantity: 8,
        parties: ROLES, at: now,
        bundle: { id: 'SYN-DEMO-BUNDLE', expiresAt: now + 900_000,
          items: Object.values(RESOURCE).map(resourceId => ({ resourceId, quantity: 8 })) }
      }, now);
    } else if (input.action === 'approve') {
      if (!Object.hasOwn(ROLES, input.role)) throw Error('invalid_demo_role');
      orders.approve({ id: ORDER, role: input.role, actorId: ROLES[input.role], evidenceRef: 'SYN-' + input.role + '-approval', at: now });
     } else if (input.action === 'quote') {
      commercial.quote({ orderId: ORDER, at: now });
    } else if (input.action === 'accept-terms') {
      commercial.accept({ orderId: ORDER, actorId: 'fictional-sponsor', termsVersion: 'SYN-TERMS-2026-11-07-v1', at: now });
    } else if (input.action === 'mock-decline') {
      commercial.authorize({ orderId: ORDER, actorId: 'fictional-sponsor', attemptId: 'SYN-AUTH-declined', mode: 'decline', at: now });
    } else if (input.action === 'mock-authorize') {
      commercial.authorize({ orderId: ORDER, actorId: 'fictional-sponsor', attemptId: 'SYN-AUTH-success', mode: 'approve', at: now });
    } else if (input.action === 'pickup') {
      if (orders.get(ORDER)?.state !== 'approved') throw Error('pickup_requires_approvals');
      if (commercial.get(ORDER)?.state !== 'authorized') throw Error('mock_authorization_required');
      orders.pickup({ id: ORDER, actorId: ROLES.transport, evidenceRef: 'SYN-pickup', at: now });
    } else if (input.action === 'deliver') {
      if (input.mode !== 'full' && input.mode !== 'partial') throw Error('invalid_demo_receipt_mode');
      delivery.recordReceipt({ id: ORDER, receiptId: 'SYN-DEMO-RECEIPT', actorId: ROLES.receiver,
        evidenceRef: 'SYN-receiver-receipt-' + input.mode, foodResourceId: RESOURCE.food,
        received: input.mode === 'full' ? 8 : 6, rejected: input.mode === 'full' ? 0 : 1,
        damaged: 0, at: now });
    } else if (input.action === 'document-exception') {
      delivery.recordDisposition({ id: ORDER, actorId: ROLES.receiver, evidenceRef: 'SYN-exception-review',
        resolutionCode: 'exception_documented', explanation: 'Fictional discrepancy reviewed; not evidence of recovered stock.', at: now });
     } else if (input.action === 'mock-capture') {
      commercial.capture({ orderId: ORDER, actorId: 'fictional-sponsor', at: now });
    } else if (input.action === 'mock-refund') {
      commercial.refund({ orderId: ORDER, actorId: 'fictional-sponsor', at: now });
    } else if (input.action === 'cancel') {
      orders.cancel({ id: ORDER, actorId: ROLES.donor, evidenceRef: 'SYN-cancellation', at: now });
    }
    return snapshot();
  }
  async function tenantHttpRoute(req, res) {
    // The public demo API remains intentionally untrusted and fictional. This
    // NEW, opt-in endpoint exercises the tenant gate over real HTTP without
    // treating a header, body, or selector as proof of a genuine login.
    if (!resolveServerPrincipal) throw Error('tenant_route_unavailable');
    const verified = resolveServerPrincipal(req);
    return requestPrincipal.run(verified, async () => {
      if (req.method === 'GET') {
        return json(res, 200, { synthetic: true, authenticatedTestOnly: true,
          order: tenantGate.read(ORDER) });
      }
      const input = await readJson(req);
      if (['actorId', 'tenantId', 'role', 'authenticated'].some(k => Object.hasOwn(input, k)))
        throw Error('client_identity_claim_denied');
      const now = clock();
      if (!Number.isSafeInteger(now) || now < 0) throw Error('invalid_demo_clock');
      // All four operations use the *server-resolved* actor; supplied actor IDs
      // and tenant IDs never decide the effective principal.
      const role = requestPrincipal.getStore()?.role;
      if (input.action === 'approve')
        tenantGate.approve({ id: ORDER, role, evidenceRef: 'SYN-HTTP-' + role + '-approval', at: now });
      else if (input.action === 'pickup') {
        if (commercial.get(ORDER)?.state !== 'authorized') throw Error('mock_authorization_required');
        tenantGate.pickup({ id: ORDER, evidenceRef: 'SYN-HTTP-pickup', at: now });
      } else if (input.action === 'cancel')
        tenantGate.cancel({ id: ORDER, evidenceRef: 'SYN-HTTP-cancel', at: now });
      else throw Error('unknown_tenant_action');
      return json(res, 200, { synthetic: true, authenticatedTestOnly: true,
        order: tenantGate.read(ORDER) });
    });
  }
  const server = http.createServer(async (req, res) => {
    try {
      const host = req.headers.host ?? '';
      if (!/^((127\.0\.0\.1)|(localhost)):\d{1,5}$/.test(host)) return json(res, 403, { error: 'loopback_host_required' });
      if (req.headers.origin && req.headers.origin !== 'http://' + host) return json(res, 403, { error: 'cross_origin_denied' });
      if (req.headers['sec-fetch-site'] && !['same-origin', 'none'].includes(req.headers['sec-fetch-site']))
        return json(res, 403, { error: 'cross_site_denied' });
      if (req.url === '/api/tenant-order' && ['GET','POST'].includes(req.method)) {
        if (req.method === 'POST' && !(req.headers['content-type'] || '').startsWith('application/json'))
          return json(res, 415, { error: 'json_required' });
        return await tenantHttpRoute(req, res);
      }
      if (req.method === 'GET' && req.url === '/api/state') return json(res, 200, snapshot());
      if (req.method === 'POST' && req.url === '/api/action') {
        if (!(req.headers['content-type'] || '').startsWith('application/json')) return json(res, 415, { error: 'json_required' });
        return json(res, 200, act(await readJson(req)));
      }
      if (req.method === 'GET' && Object.hasOwn(FILES, req.url)) {
        const [file, type] = FILES[req.url];
        const body = await readFile(join(here, file));
        res.writeHead(200, { ...HEADERS, 'Content-Type': type, 'Content-Length': body.length });
        return res.end(body);
      }
      json(res, 404, { error: 'not_found' });
    } catch (err) {
      const known = new Set(['invalid_json', 'request_too_large', 'unknown_action', 'invalid_demo_role', 'invalid_demo_receipt_mode', 'demo_already_started', 'unknown_order', 'invalid_order_state', 'pickup_requires_approvals', 'delivery_requires_pickup', 'disposition_requires_exception', 'cancellation_requires_pre_pickup', 'reservation_expired', 'unauthorized_party', 'quote_requires_fictional_approvals', 'missing_fictional_quote', 'fictional_agreement_mismatch', 'agreement_requires_approved_order', 'authorization_requires_fictional_agreement', 'authorization_requires_approved_order', 'invalid_commercial_state', 'mock_authorization_required', 'capture_requires_reconciled_delivery', 'capture_requires_mock_authorization', 'refund_requires_mock_capture', 'unauthorized_fictional_sponsor', 'invalid_mock_authorization_mode', 'invalid_mock_attempt', 'out_of_order_commercial_event']);
      const denial = guardedErrors.has(err?.message);
      json(res, denial ? 403 : known.has(err?.message) ? 409 : 500,
        { error: denial || known.has(err?.message) ? err.message : 'synthetic_demo_action_failed' });
    }
  });
  return { server, ledger, orders, delivery, commercial, tenantGate, snapshot, act,
    async listen(port = 0) {
      await new Promise((resolve, reject) => { server.once('error', reject); server.listen(port, HOST, resolve); });
      return 'http://' + HOST + ':' + server.address().port;
    },
    async close() { await new Promise((resolve, reject) => server.close(err => err ? reject(err) : resolve())); ledger.close(); },
  };
}

if (process.argv[1] && fileURLToPath(import.meta.url) === process.argv[1]) {
  const app = createLocalDemo();
  const port = Number(process.env.MAYA_SYNTHETIC_PORT || 8789);
  app.listen(port).then(url => console.log('Synthetic-only loopback demonstration: ' + url)).catch(err => { console.error(err); process.exitCode = 1; });
}
