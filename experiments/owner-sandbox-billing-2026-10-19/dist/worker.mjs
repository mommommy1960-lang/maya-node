// Source: payments.mjs
// Review candidate: owner sandbox billing only. Does not alter owner chat access.
const OWNER_ID = 'maya-owner-demo';
const OWNER_EMAIL = 'commons.initiative@proton.me';
const supported = new Set(['checkout.session.completed', 'checkout.session.async_payment_succeeded',
  'invoice.paid', 'invoice.payment_failed', 'customer.subscription.updated', 'customer.subscription.deleted']);
const idOf = x => typeof x === 'string' ? x : x?.id;
const fail = (message, status = 503) => { throw Object.assign(new Error(message), { status }); };
function testKey(env) {
  if (!/^(sk|rk)_test_[A-Za-z0-9]+$/.test(env.STRIPE_SECRET_KEY || '')) fail('Sandbox test key required', 403);
}
async function stripe(env, path, options = {}, send = fetch) {
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
async function verifySignature(payload, header, secret, now = Date.now()) {
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
function subscriptionId(event) {
  const o = event.data?.object;
  if (event.type.startsWith('customer.subscription.')) return idOf(o);
  return idOf(o?.subscription) || idOf(o?.parent?.subscription_details?.subscription);
}
function snapshot(sub, env) {
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
function hasAccess(s, now = Math.floor(Date.now() / 1000)) {
  return Boolean(s && s.status === 'active' && s.paid && Number.isSafeInteger(s.period_end) && s.period_end > now);
}
async function currentSnapshot(env, id, send) {
  if (!/^sub_[A-Za-z0-9]+$/.test(id || '')) fail('Invalid subscription ID', 400);
  const sub = await stripe(env, '/v1/subscriptions/' + id + '?expand[]=latest_invoice', {}, send);
  return snapshot(sub, env);
}
async function processEvent(event, env, store, send) {
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
class D1Store {
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
async function webhook(request, env, store = new D1Store(env.DB), send) {
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
async function ownerBilling(request, env, session, send = fetch) {
  if (session?.email !== OWNER_EMAIL) return Response.json({ error: 'Owner session required' }, { status: 403 });
  const path = new URL(request.url).pathname;
  if (!['/api/stripe/access-status','/api/stripe/portal','/api/stripe/cancel','/api/stripe/import'].includes(path)) return null;
  if (request.method !== (path.endsWith('access-status') ? 'GET' : 'POST')) return new Response('Method not allowed', { status: 405 });
  try {
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


// Source: ui.mjs
const HTML = `<!DOCTYPE html>
<html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Maya Recovery Staging - Owner Secure Access & Payments</title>
<style>
body{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif;max-width:650px;margin:40px auto;padding:20px;background:#0f172a;color:#f8fafc}
.card{background:#1e293b;padding:24px;border-radius:12px;box-shadow:0 4px 12px #0005;margin-bottom:20px}
input,button,textarea{width:100%;padding:12px;margin-top:8px;margin-bottom:16px;border-radius:6px;border:1px solid #475569;background:#0f172a;color:#f8fafc;box-sizing:border-box}
button{background:#3b82f6;border:none;font-weight:bold;cursor:pointer}button:hover{background:#2563eb}button:disabled{opacity:.5;cursor:wait}
.chat-box{height:260px;overflow-y:auto;background:#0f172a;padding:12px;border-radius:6px;border:1px solid #334155;margin-bottom:16px}
.msg{margin-bottom:10px;padding:8px 12px;border-radius:6px}.msg.user{background:#1e3a8a;text-align:right}.msg.assistant{background:#334155}.msg.error{background:#7f1d1d;color:#fecaca}
.badge{display:inline-block;background:#059669;padding:4px 8px;border-radius:4px;font-size:12px;margin-bottom:12px}.stripe-box{background:#0f172a;padding:16px;border-radius:8px;border:1px solid #334155;margin-top:16px}.muted{font-size:14px;color:#cbd5e1}
</style></head><body><div class="card">
<div class="badge">Owner Staging Environment • Stripe Sandbox Practice</div><h1>Maya Secure Staging & Payments</h1>
<div id="auth-section"><h3>Owner Sign-In</h3>
<input type="email" id="email-input" aria-label="Owner email" value="commons.initiative@proton.me" readonly>
<input type="password" id="secret-input" aria-label="Owner access secret" placeholder="Enter STAGING_ACCESS_SECRET" autocomplete="current-password">
<button id="signin">Authenticate Owner Session</button><p id="login-error" role="alert"></p></div>
<div id="app-section" style="display:none">
<div style="display:flex;justify-content:space-between;align-items:center"><span>Owner: <strong id="user-email"></strong></span><button id="logout" style="width:auto;background:#ef4444">Sign Out</button></div>
<h3>Secure Conversation History</h3><div id="chat-box" class="chat-box" aria-live="polite"></div>
<textarea id="prompt-input" rows="2" aria-label="Message to Maya" placeholder="Enter test prompt (e.g. pineapple)..."></textarea><button id="send">Send Message</button>
<div class="stripe-box"><h4>Stripe Sandbox Integration Status</h4><p id="stripe-status" class="muted" role="status"></p>
<button id="test-stripe" style="background:#6366f1">Test Stripe Connectivity (Prices Read)</button><div id="checkout-section"><button id="checkout" hidden style="background:#059669">Start Sandbox Test Checkout</button></div>
<h4>Owner Practice Subscription</h4><p class="muted">Sandbox billing status only. Your owner chat remains available. No real charges.</p>
<p id="billing-status" role="status"></p><button id="billing-refresh">Refresh Subscription Status</button>
<details><summary>Link the existing paid practice subscription</summary><p class="muted">Copy the subscription ID beginning sub_ from your Stripe Sandbox subscription. This links it to this owner demo only.</p>
<input id="subscription-id" aria-label="Existing sandbox subscription ID" placeholder="sub_…"><button id="import">Link Existing Practice Subscription</button></details>
<button id="portal" hidden>Manage Subscription in Stripe</button><button id="cancel" hidden style="background:#b45309">Cancel Renewal at Period End</button>
<p id="action-status" role="status"></p></div></div></div>
<script>
let sessionToken=localStorage.getItem('maya_owner_token')||'';
let userEmail=localStorage.getItem('maya_owner_email')||'';
const el=id=>document.getElementById(id);
function logout(){localStorage.removeItem('maya_owner_token');localStorage.removeItem('maya_owner_email');sessionToken='';location.reload();}
async function api(path,body){const r=await fetch(path,{method:body===undefined?'GET':'POST',headers:{'Authorization':'Bearer '+sessionToken,'Content-Type':'application/json'},body:body===undefined?undefined:JSON.stringify(body)});const d=await r.json();if(r.status===401){logout();throw Error('Owner session expired. Please sign in again.')}if(!r.ok)throw Error(d.error||'Request failed');return d;}
function addMessage(role,content){const div=document.createElement('div');div.className='msg '+(role==='user'?'user':role==='assistant'?'assistant':'error');div.textContent=content;el('chat-box').appendChild(div);el('chat-box').scrollTop=el('chat-box').scrollHeight;}
async function loadHistory(){const d=await api('/api/messages');el('chat-box').replaceChildren();for(const m of d.messages||[])addMessage(m.role,m.content);}
async function testStripeAuth(){const status=el('stripe-status');status.textContent='Checking Stripe sandbox connection…';el('checkout').hidden=true;try{const d=await Promise.race([api('/api/stripe/test'),new Promise((_,reject)=>setTimeout(()=>reject(Error('Stripe connectivity check timed out. Please report this to the owner.')),15000))]);status.textContent=d.success?(d.checkout_ready?'✓ Sandbox connection and $10/month checkout price verified.':'✓ Sandbox authenticated, but checkout price is not ready. '+(d.error||'Check STRIPE_PRICE_ID configuration.')):'Stripe test failed: '+(d.error||'Unknown error');el('checkout').hidden=!(d.success&&d.checkout_ready);}catch(e){status.textContent='Stripe connectivity check failed: '+e.message;}}
async function checkAccess(){try{const d=await api('/api/stripe/access-status');const s=d.subscription||{};el('billing-status').textContent=!s.subscription?'No practice subscription linked yet.':(d.billing_access?'✓ Paid sandbox access current. ':'Sandbox billing access is not current. ')+(s.cancel_at_period_end?'Renewal cancellation scheduled. ':'')+(s.period_end?'Paid period ends '+new Date(s.period_end*1000).toLocaleString()+'.':'');el('portal').hidden=!s.subscription;el('cancel').hidden=!s.subscription||s.cancel_at_period_end||s.status!=='active';}catch(e){el('billing-status').textContent=e.message;}}
async function showApp(){el('auth-section').style.display='none';el('app-section').style.display='block';el('user-email').textContent=userEmail;await Promise.allSettled([loadHistory(),testStripeAuth(),checkAccess()]);const q=new URLSearchParams(location.search);if(q.get('checkout')==='success')el('action-status').textContent='Returned from Stripe. Subscription status is confirmed separately by verified billing events.';}
function action(id,fn){el(id).addEventListener('click',async()=>{el(id).disabled=true;try{await fn();}catch(e){el('action-status').textContent=e.message;}finally{el(id).disabled=false;}});}
action('signin',async()=>{try{const d=await api('/api/signin',{email:el('email-input').value,accessSecret:el('secret-input').value});sessionToken=d.token;userEmail=el('email-input').value;localStorage.setItem('maya_owner_token',sessionToken);localStorage.setItem('maya_owner_email',userEmail);el('secret-input').value='';await showApp();}catch(e){el('login-error').textContent=e.message;}});
el('logout').addEventListener('click',async()=>{try{await api('/api/signout',{});}finally{logout();}});
action('send',async()=>{const content=el('prompt-input').value.trim();if(!content)return;el('prompt-input').value='';addMessage('user',content);try{const d=await api('/api/chat',{content});addMessage('assistant',d.reply);}catch(e){addMessage('error',e.message);}});
action('test-stripe',testStripeAuth);action('billing-refresh',checkAccess);
action('checkout',async()=>{const d=await api('/api/stripe/checkout',{});if(d.livemode!==false||!d.url.startsWith('https://checkout.stripe.com/'))throw Error('Invalid sandbox checkout response');location.href=d.url;});
action('import',async()=>{const subscriptionId=el('subscription-id').value.trim();if(!/^sub_[a-zA-Z0-9]+$/.test(subscriptionId))throw Error('Enter the Stripe Sandbox subscription ID beginning sub_.');if(!confirm('Link this subscription to your owner sandbox demo?'))return;await api('/api/stripe/import',{subscriptionId,confirmOwnerImport:true});el('action-status').textContent='Practice subscription linked and verified.';await checkAccess();});
action('portal',async()=>{const d=await api('/api/stripe/portal',{});if(!d.url.startsWith('https://billing.stripe.com/'))throw Error('Invalid Stripe portal URL');location.href=d.url;});
action('cancel',async()=>{if(!confirm('Cancel renewal of this sandbox practice subscription at its paid period end?'))return;const d=await api('/api/stripe/cancel',{});el('action-status').textContent=d.message;await checkAccess();});
if(sessionToken)showApp();
</script></body></html>`;


// Source: worker.mjs
// Integrated review candidate based on the owner-supplied active Worker.
// Preserves bearer owner login, existing table names and fp8 model. NOT DEPLOYED.

function generateSessionToken() {
  const bytes = new Uint8Array(32); crypto.getRandomValues(bytes);
  return Array.from(bytes, b => b.toString(16).padStart(2, '0')).join('');
}
const response = (data,status=200) => Response.json(data,{status,headers:{'Cache-Control':'no-store'}});
async function body(request) {
  const raw=await request.text(); if(raw.length>20000)throw Object.assign(Error('Request too large'),{status:413});
  try{return JSON.parse(raw);}catch{throw Object.assign(Error('Invalid JSON'),{status:400});}
}
export default {
  async fetch(request,env) {
    const url=new URL(request.url),path=url.pathname;
    if(path==='/api/stripe/webhook')return webhook(request,env);
    if(!env.STAGING_ACCESS_SECRET||!env.DB)return response({error:'Owner staging is not configured'},503);
    try {
      await env.DB.prepare('CREATE TABLE IF NOT EXISTS recovery_sessions (token TEXT PRIMARY KEY, email TEXT, created_at TEXT)').run();
      await env.DB.prepare('CREATE TABLE IF NOT EXISTS recovery_messages (id TEXT PRIMARY KEY, session_token TEXT, email TEXT, role TEXT, content TEXT, created_at TEXT)').run();
      if(path==='/'||path==='/index.html')return new Response(HTML,{headers:{'Content-Type':'text/html; charset=utf-8','Cache-Control':'no-store','X-Content-Type-Options':'nosniff'}});
      if(path==='/api/signin'&&request.method==='POST'){
        const d=await body(request);
        if(d.email!==OWNER_EMAIL||typeof d.accessSecret!=='string'||d.accessSecret!==env.STAGING_ACCESS_SECRET)return response({error:'Invalid owner credentials'},403);
        const token=generateSessionToken();
        await env.DB.prepare('INSERT INTO recovery_sessions (token,email,created_at) VALUES (?,?,?)').bind(token,OWNER_EMAIL,new Date().toISOString()).run();
        return response({token});
      }
      const token=request.headers.get('Authorization')?.match(/^Bearer ([a-f0-9]{64})$/)?.[1];
      if(!token)return response({error:'Unauthorized: Missing bearer token'},401);
      const session=await env.DB.prepare('SELECT * FROM recovery_sessions WHERE token = ?').bind(token).first();
      const age=session?Date.now()-Date.parse(session.created_at):NaN;
      if(!session||session.email!==OWNER_EMAIL||!Number.isFinite(age)||age<0||age>7200000){
        if(session)await env.DB.prepare('DELETE FROM recovery_sessions WHERE token = ?').bind(token).run();
        // Expiry removes the session, not historical conversations.
        return response({error:'Unauthorized: Invalid or expired session token'},401);
      }
      if(path==='/api/signout'&&request.method==='POST'){
        await env.DB.prepare('DELETE FROM recovery_sessions WHERE token = ?').bind(token).run();return response({ok:true});
      }
      const billing=await ownerBilling(request,env,session);if(billing)return billing;
      if(path==='/api/messages'&&request.method==='GET'){
        const rows=await env.DB.prepare("SELECT role, content FROM recovery_messages WHERE email = ? AND role != 'error' ORDER BY created_at ASC").bind(session.email).all();
        return response({messages:rows.results||[]});
      }
      if(path==='/api/chat'&&request.method==='POST'){
        const {content}=await body(request);
        if(typeof content!=='string'||!content.trim()||content.length>8000)return response({error:'Message must contain 1–8000 characters'},400);
        await env.DB.prepare("INSERT INTO recovery_messages (id,session_token,email,role,content,created_at) VALUES (?,?,?,'user',?,?)").bind(crypto.randomUUID(),token,session.email,content,new Date().toISOString()).run();
        let ai;
        try{ai=await env.AI.run('@cf/meta/llama-3.1-8b-instruct-fp8',{messages:[{role:'system',content:'You are Maya, a secure situated AI assistant upholding truth and integrity. Keep responses concise, clear, and professional.'},{role:'user',content}]});}
        catch{return response({error:'Model inference unavailable. Please retry later.'},502);}
        const reply=ai.response||ai.result;
        if(typeof reply!=='string'||!reply)return response({error:'Model returned an empty response'},502);
        await env.DB.prepare("INSERT INTO recovery_messages (id,session_token,email,role,content,created_at) VALUES (?,?,?,'assistant',?,?)").bind(crypto.randomUUID(),token,session.email,reply,new Date().toISOString()).run();
        return response({reply});
      }
      if(path==='/api/stripe/test'&&request.method==='GET'){
        testKey(env);
        // Verify the configured price itself; a list has no top-level livemode field.
        if(!/^price_[A-Za-z0-9]+$/.test(env.STRIPE_PRICE_ID||''))return response({success:false,error:'Missing sandbox price ID',checkout_ready:false});
        const price=await stripe(env,'/v1/prices/'+env.STRIPE_PRICE_ID);
        const valid=price.livemode===false&&price.active===true&&price.currency==='usd'&&price.unit_amount===1000&&price.recurring?.interval==='month'&&price.recurring?.interval_count===1;
        return response({success:valid,livemode:price.livemode,checkout_ready:valid,error:valid?null:'Configured price must be active USD $10/month in sandbox'});
      }
      if(path==='/api/stripe/checkout'&&request.method==='POST'){
        testKey(env);
        if(!/^price_[A-Za-z0-9]+$/.test(env.STRIPE_PRICE_ID||''))return response({error:'Sandbox price not configured'},503);
        // Refuse new checkout before additive migration, avoiding an untracked checkout.
        const configured=await env.DB.prepare('SELECT owner_id FROM owner_sandbox_billing WHERE owner_id=?').bind(OWNER_ID).first();
        if(!configured)return response({error:'Apply the sandbox billing migration first'},503);
        const data=await stripe(env,'/v1/checkout/sessions',{method:'POST',body:new URLSearchParams({mode:'subscription','line_items[0][price]':env.STRIPE_PRICE_ID,'line_items[0][quantity]':'1',client_reference_id:OWNER_ID,success_url:url.origin+'/?checkout=success',cancel_url:url.origin+'/?checkout=cancelled'}).toString()});
        if(data.livemode!==false||!/^cs_test_[A-Za-z0-9]+$/.test(data.id||'')||!/^https:\/\/checkout\.stripe\.com\//.test(data.url||''))return response({error:'Invalid sandbox checkout response'},502);
        await env.DB.prepare('INSERT INTO owner_sandbox_checkouts(checkout_id,owner_id) VALUES (?,?)').bind(data.id,OWNER_ID).run();
        return response({url:data.url,livemode:false});
      }
      return response({error:'Not found'},404);
    }catch(error){return response({error:error.status?error.message:'Service temporarily unavailable. Check staging configuration.'},error.status||503);}
  }
};

