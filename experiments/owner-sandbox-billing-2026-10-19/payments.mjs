// Review candidate: owner sandbox billing only. Does not alter owner chat access.
export const OWNER_ID = 'maya-owner-demo';
export const OWNER_EMAIL = 'commons.initiative@proton.me';
const supported = new Set(['checkout.session.completed', 'checkout.session.async_payment_succeeded',
  'invoice.paid', 'invoice.payment_failed', 'customer.subscription.updated', 'customer.subscription.deleted']);
const idOf = x => typeof x === 'string' ? x : x?.id;
const fail = (message, status = 503) => { throw Object.assign(new Error(message), { status }); };
export function testKey(env) {
  if (!/^(sk|rk)_test_[A-Za-z0-9]+$/.test(env.STRIPE_SECRET_KEY || '')) fail('Sandbox test key required', 403);
}
export async function stripe(env, path, options = {}, send = fetch) {
  testKey(env);
  const response = await send('https://api.stripe.com' + path, {
    ...options, headers: { Authorization: 'Bearer ' + env.STRIPE_SECRET_KEY,
      'Content-Type': 'application/x-www-form-urlencoded', ...options.headers }
  });
  const data = await response.json();
  if (!response.ok) fail('Stripe request failed; review restricted-key permissions and Stripe logs', 502);
  if (data.livemode === true) fail('Live Stripe object rejected', 403);
  return data;
}
export async function verifySignature(payload, header, secret, now = Date.now()) {
  if (!secret || !header) return false;
  const fields = header.split(',').map(p => p.trim().split('='));
  const stamps = fields.filter(([k]) => k === 't');
  if (stamps.length !== 1 || !/^\d+$/.test(stamps[0][1])) return false;
  const t = Number(stamps[0][1]);
  if (!Number.isSafeInteger(t) || Math.abs(now / 1000 - t) > 300) return false;
  const enc = new TextEncoder();
  const key = await crypto.subtle.importKey('raw', enc.encode(secret), { name: 'HMAC', hash: 'SHA-256' }, false, ['verify']);
  for (const [kind, value] of fields) {
    if (kind !== 'v1' || !/^[a-fA-F0-9]{64}$/.test(value || '')) continue;
    const bytes = Uint8Array.from(value.match(/../g), b => parseInt(b, 16));
    if (await crypto.subtle.verify('HMAC', key, bytes, enc.encode(`${t}.${payload}`))) return true;
  }
  return false;
}
export function subscriptionId(event) {
  const o = event.data?.object;
  if (event.type.startsWith('customer.subscription.')) return idOf(o);
  return idOf(o?.subscription) || idOf(o?.parent?.subscription_details?.subscription);
}
export function snapshot(sub, env) {
  if (sub.livemode !== false || !/^sub_[A-Za-z0-9]+$/.test(sub.id || '')) fail('Invalid sandbox subscription', 403);
  const items = sub.items?.data;
  if (!Array.isArray(items) || items.length !== 1 || items[0].quantity !== 1) fail('Unexpected subscription items', 403);
  const item = items[0], price = item.price;
  if (price?.livemode !== false || price.id !== env.STRIPE_PRICE_ID || price.currency !== 'usd' ||
      price.unit_amount !== 1000 || price.recurring?.interval !== 'month' || price.recurring?.interval_count !== 1) {
    fail('Unexpected practice price', 403);
  }
  const end = item.current_period_end ?? sub.current_period_end;
  if (!Number.isSafeInteger(end) || end <= 0) fail('Missing billing period; access remains disabled');
  const invoice = sub.latest_invoice;
  if (!invoice || typeof invoice !== 'object' || invoice.livemode !== false) fail('Expanded sandbox invoice required');
  const invoiceSub = idOf(invoice.subscription) || idOf(invoice.parent?.subscription_details?.subscription);
  const customer = idOf(sub.customer);
  if (!/^cus_[A-Za-z0-9]+$/.test(customer || '') || idOf(invoice.customer) !== customer || invoiceSub !== sub.id) {
    fail('Invoice ownership mismatch', 403);
  }
  const paid = invoice.status === 'paid' && invoice.currency === 'usd' &&
    invoice.amount_paid === 1000 && invoice.amount_remaining === 0;
  return { customer, subscription: sub.id, status: sub.status,
    period_end: end, paid, cancel_at_period_end: sub.cancel_at_period_end === true };
}
export function hasAccess(s, now = Math.floor(Date.now() / 1000)) {
  return Boolean(s && s.status === 'active' && s.paid && Number.isSafeInteger(s.period_end) && s.period_end > now);
}
export async function currentSnapshot(env, id, send) {
  if (!/^sub_[A-Za-z0-9]+$/.test(id || '')) fail('Invalid subscription ID', 400);
  const sub = await stripe(env, '/v1/subscriptions/' + id + '?expand[]=latest_invoice', {}, send);
  return snapshot(sub, env);
}
export async function processEvent(event, env, store, send) {
  if (!/^evt_[A-Za-z0-9]+$/.test(event.id || '') || event.livemode !== false) fail('Invalid sandbox event', 400);
  if (!supported.has(event.type)) return { ignored: true };
  if (await store.seen(event.id)) return { duplicate: true };
  const obj = event.data?.object;
  if (obj?.livemode !== false) fail('Invalid sandbox object', 400);
  const id = subscriptionId(event);
  if (!id) fail('Missing subscription ID', 400);
  const state = await store.read();
  if (!state) fail('Apply additive billing migration first');
  // Initial linkage must come from a checkout actually created by this owner session.
  if (event.type.startsWith('checkout.session.')) {
    if (obj.mode !== 'subscription' || obj.client_reference_id !== OWNER_ID ||
        !(await store.hasCheckout(obj.id))) return { ignored: true };
    if (obj.payment_status !== 'paid') return { ignored: true, pending_payment: true };
  } else if (state.subscription !== id) {
    // May arrive before checkout completion. Retry so the event is not lost.
    fail('Subscription not linked yet; retry after checkout completion');
  }
  if (state.subscription && state.subscription !== id) fail('Different owner subscription already linked', 409);
  const next = await currentSnapshot(env, id, send);
  if (idOf(obj.customer) !== next.customer) fail('Event customer mismatch', 403);
  // Fetch current canonical state rather than trusting the possibly old event payload.
  // Revision CAS ensures an overlapping stale fetch cannot overwrite a committed update.
  if (!(await store.commit(event.id, state.revision, next))) fail('Concurrent update; retry event');
  return { received: true };
}
export class D1Store {
  constructor(db) { this.db = db; }
  async read() {
    const row = await this.db.prepare('SELECT revision,snapshot FROM owner_sandbox_billing WHERE owner_id=?').bind(OWNER_ID).first();
    return row ? { ...JSON.parse(row.snapshot), revision: row.revision } : null;
  }
  async seen(id) { return Boolean(await this.db.prepare('SELECT event_id FROM owner_sandbox_events WHERE event_id=?').bind(id).first()); }
  async hasCheckout(id) { return Boolean(await this.db.prepare('SELECT checkout_id FROM owner_sandbox_checkouts WHERE checkout_id=? AND owner_id=?').bind(id, OWNER_ID).first()); }
  async commit(id, revision, next) {
    try {
      const results = await this.db.batch([
        this.db.prepare('INSERT INTO owner_sandbox_events(event_id) SELECT ? WHERE EXISTS (SELECT 1 FROM owner_sandbox_billing WHERE owner_id=? AND revision=?)').bind(id, OWNER_ID, revision),
        this.db.prepare('UPDATE owner_sandbox_billing SET snapshot=?,revision=revision+1 WHERE owner_id=? AND revision=? AND EXISTS (SELECT 1 FROM owner_sandbox_events WHERE event_id=?)').bind(JSON.stringify(next), OWNER_ID, revision, id)
      ]);
      return results[0].meta.changes === 1 && results[1].meta.changes === 1;
    } catch (error) {
      // A competing duplicate can win the unique constraint. Never swallow other failures.
      if (await this.seen(id)) return true;
      throw error;
    }
  }
}
export async function webhook(request, env, store = new D1Store(env.DB), send) {
  if (request.method !== 'POST') return new Response('Method not allowed', { status: 405 });
  if (!env.STRIPE_WEBHOOK_SECRET) return new Response('Webhook not configured', { status: 503 });
  try {
    const declared = Number(request.headers.get('content-length') || 0);
    if (declared > 262144) return new Response('Too large', { status: 413 });
    // Bound actual streamed bytes, even when Content-Length is absent or false.
    const reader = request.body?.getReader();
    const chunks = []; let size = 0;
    if (reader) {
      while (true) {
        const { value, done } = await reader.read(); if (done) break;
        size += value.byteLength;
        if (size > 262144) { await reader.cancel(); return new Response('Too large', { status: 413 }); }
        chunks.push(value);
      }
    }
    const bytes = new Uint8Array(size); let offset = 0;
    for (const chunk of chunks) { bytes.set(chunk, offset); offset += chunk.length; }
    const payload = new TextDecoder('utf-8', { fatal: true }).decode(bytes);
    if (!(await verifySignature(payload, request.headers.get('Stripe-Signature'), env.STRIPE_WEBHOOK_SECRET))) {
      return new Response('Invalid signature', { status: 400 });
    }
    let event; try { event = JSON.parse(payload); } catch { return new Response('Invalid JSON', { status: 400 }); }
    return Response.json(await processEvent(event, env, store, send));
  } catch (error) {
    return Response.json({ error: error.status ? error.message : 'Billing temporarily unavailable' }, { status: error.status || 503 });
  }
}
export async function discoverOwnerSubscription(env, send = fetch) {
  testKey(env);
  const customersResult = await stripe(env, '/v1/customers?email=' + encodeURIComponent(OWNER_EMAIL) + '&limit=100', {}, send);
  if (!Array.isArray(customersResult.data)) fail('Stripe customer lookup returned an invalid response');
  if (customersResult.has_more) fail('Customer lookup is incomplete; no subscription was selected', 409);
  const customers = customersResult.data.filter(c => c && c.email === OWNER_EMAIL && /^cus_[A-Za-z0-9]+$/.test(c.id || ''));
  if (customers.length > 1) fail('Multiple matching Stripe customers found; manual review required', 409);
  if (!customers.length) return { found: false, message: 'No matching sandbox customer was found.' };

  const customer = customers[0];
  const subscriptions = [];
  let startingAfter = '';
  for (let page = 0; page < 5; page++) {
    const query = new URLSearchParams({ customer: customer.id, status: 'all', limit: '100' });
    if (startingAfter) query.set('starting_after', startingAfter);
    const result = await stripe(env, '/v1/subscriptions?' + query.toString(), {}, send);
    if (!Array.isArray(result.data)) fail('Stripe subscription lookup returned an invalid response');
    subscriptions.push(...result.data);
    if (!result.has_more) break;
    if (page === 4) fail('Subscription lookup exceeded the safe page limit; no subscription was selected', 409);
    const last = result.data[result.data.length - 1];
    if (!last?.id) fail('Stripe pagination was incomplete; no subscription was selected', 409);
    startingAfter = last.id;
  }

  const matches = subscriptions.filter(s => s && s.livemode === false &&
    Array.isArray(s.items?.data) && s.items.data.some(item => item?.price?.id === env.STRIPE_PRICE_ID));
  if (!matches.length) return { found: false, message: 'No subscription matched the configured sandbox practice price.' };
  if (matches.length > 1) fail('Multiple subscriptions match the configured practice price; manual review required', 409);

  const verified = await currentSnapshot(env, matches[0].id, send);
  if (verified.customer !== customer.id) fail('Subscription customer does not match the owner account', 403);
  if (!hasAccess(verified)) fail('A matching subscription exists, but it is not currently paid and active; no link was made', 409);
  return { found: true, subscription_id: verified.subscription, status: verified.status,
    paid: verified.paid, period_end: verified.period_end, billing_access: true };
}

export async function ownerBilling(request, env, session, send = fetch) {
  if (session?.email !== OWNER_EMAIL) return Response.json({ error: 'Owner session required' }, { status: 403 });
  const path = new URL(request.url).pathname;
  if (!['/api/stripe/access-status','/api/stripe/portal','/api/stripe/cancel','/api/stripe/import','/api/stripe/discover'].includes(path)) return null;
  if (request.method !== (path.endsWith('access-status') || path.endsWith('discover') ? 'GET' : 'POST')) return new Response('Method not allowed', { status: 405 });
  try {
    if (path.endsWith('discover')) return Response.json(await discoverOwnerSubscription(env, send), { headers: { 'Cache-Control': 'no-store' } });
    const s = await new D1Store(env.DB).read();
    if (path.endsWith('import')) {
      if (!s) fail('Apply additive billing migration first');
      const body = await request.json();
      if (body.confirmOwnerImport !== true) fail('Explicit owner import confirmation required', 400);
      const next = await currentSnapshot(env, body.subscriptionId, send);
      if (s.subscription && s.subscription !== next.subscription) fail('Another subscription already linked', 409);
      if (!(await new D1Store(env.DB).commit('owner_import_' + crypto.randomUUID(), s.revision, next))) fail('Concurrent import; retry');
      return Response.json({ imported: true, scope: 'owner_sandbox_only', billing_access: hasAccess(next) });
    }
    if (path.endsWith('access-status')) return Response.json({ scope: 'owner_sandbox_only', billing_access: hasAccess(s), subscription: s, owner_demo_access: true }, { headers: { 'Cache-Control': 'no-store' } });
    if (!s?.subscription) fail('Owner practice subscription is not linked', 409);
    const canonical = await currentSnapshot(env, s.subscription, send);
    if (canonical.customer !== s.customer) fail('Customer mismatch', 403);
    if (path.endsWith('portal')) {
      const data = await stripe(env, '/v1/billing_portal/sessions', { method: 'POST', body: new URLSearchParams({ customer: s.customer, return_url: new URL(request.url).origin }).toString() }, send);
      if (!/^https:\/\/billing\.stripe\.com\//.test(data.url || '')) fail('Invalid portal URL', 502);
      return Response.json({ url: data.url });
    }
    const data = await stripe(env, '/v1/subscriptions/' + s.subscription, { method: 'POST',
      body: new URLSearchParams({ cancel_at_period_end: 'true' }).toString() }, send);
    if (data.livemode !== false || data.id !== s.subscription || data.cancel_at_period_end !== true) fail('Cancellation not confirmed', 502);
    return Response.json({ message: 'Cancellation scheduled at period end. Verified webhook updates billing access.', cancel_at_period_end: true });
  } catch (error) {
    return Response.json({ error: error.status ? error.message : 'Billing temporarily unavailable' }, { status: error.status || 503 });
  }
}
