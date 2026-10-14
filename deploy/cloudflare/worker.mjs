// Opt-in staging port. No automatic reclaims or retries of uncertain jobs.
export function payloadText(p) {
  if (!p || Object.keys(p).sort().join(',') !== 'body,recipient,subject') throw new Error('Invalid payload');
  if (!/^[^\s<>@,;]+@[^\s<>@,;]+$/.test(p.recipient) || /[\r\n]/.test(p.subject)) throw new Error('Invalid headers');
  if (typeof p.body !== 'string' || typeof p.subject !== 'string' || p.body.length > 20000 || p.subject.length > 200) throw new Error('Invalid content');
  return JSON.stringify({recipient:p.recipient,subject:p.subject,body:p.body});
}
export async function dispatch(db, id, sender) {
  const attempt = crypto.randomUUID();
  const row = await db.prepare("UPDATE jobs SET state='dispatch_committed',attempt=? WHERE id=? AND state='queued' RETURNING payload").bind(attempt,id).first();
  if (!row) return 'blocked';
  try {
    const receipt = await sender(JSON.parse(row.payload));
    if (!receipt?.id) throw new Error('Missing provider receipt');
    await db.prepare("UPDATE jobs SET state='sent',receipt=? WHERE id=? AND attempt=? AND state='dispatch_committed'").bind(JSON.stringify(receipt),id,attempt).run();
    return 'sent';
  } catch (error) {
    await db.prepare("UPDATE jobs SET state='unknown' WHERE id=? AND attempt=? AND state='dispatch_committed'").bind(id,attempt).run();
    console.error(JSON.stringify({job_id:id,state:'unknown'}));
    throw error;
  }
}
async function gmailSender(env) {
  for (const k of ['GMAIL_CLIENT_ID','GMAIL_CLIENT_SECRET','GMAIL_REFRESH_TOKEN','MAIL_FROM']) if (!env[k]) throw new Error('Missing mail configuration');
  if (!/^[^\s<>@,;]+@[^\s<>@,;]+$/.test(env.MAIL_FROM)) throw new Error('Invalid sender');
  const response = await fetch('https://oauth2.googleapis.com/token', {method:'POST', body:new URLSearchParams({client_id:env.GMAIL_CLIENT_ID,client_secret:env.GMAIL_CLIENT_SECRET,refresh_token:env.GMAIL_REFRESH_TOKEN,grant_type:'refresh_token'}),signal:AbortSignal.timeout(15000)});
  if (!response.ok) {
    // Log only known OAuth error codes, never tokens or provider descriptions.
    let code = 'unclassified';
    try {
      const detail = await response.json();
      if (['invalid_client','invalid_grant','invalid_request','unauthorized_client','unsupported_grant_type','invalid_scope'].includes(detail.error)) code = detail.error;
    } catch {}
    throw new Error(`Mail authentication failed: ${code} (HTTP ${response.status})`);
  }
  const token = (await response.json()).access_token;
  if (!token) throw new Error('Missing access token');
  return async p => {
    payloadText(p);
    const subject = btoa(String.fromCharCode(...new TextEncoder().encode(p.subject)));
    const mime = `From: ${env.MAIL_FROM}\r\nTo: ${p.recipient}\r\nSubject: =?UTF-8?B?${subject}?=\r\nMIME-Version: 1.0\r\nContent-Type: text/plain; charset=UTF-8\r\nContent-Transfer-Encoding: base64\r\n\r\n${btoa(String.fromCharCode(...new TextEncoder().encode(p.body)))}`;
    const raw=btoa(mime).replace(/\+/g,'-').replace(/\//g,'_').replace(/=+$/,'');
    const r=await fetch('https://gmail.googleapis.com/gmail/v1/users/me/messages/send',{method:'POST',headers:{Authorization:`Bearer ${token}`,'Content-Type':'application/json'},body:JSON.stringify({raw}),signal:AbortSignal.timeout(20000)});
    if (!r.ok) throw new Error('Provider submission failed');
    return r.json();
  };
}

export function safeFailure(error) {
  const message = String(error?.message || '');
  const match = /^Mail authentication failed: (invalid_client|invalid_grant|invalid_request|unauthorized_client|unsupported_grant_type|invalid_scope|unclassified) \(HTTP (\d{3})\)$/.exec(message);
  if (match) return {code:match[1],http_status:Number(match[2])};
  const known = {'Missing mail configuration':'mail_configuration_missing','Invalid sender':'sender_invalid','Missing access token':'access_token_missing','Provider submission failed':'mail_submission_failed','Missing provider receipt':'receipt_missing'};
  return {code:known[message] || 'runtime_failure'};
}
export async function reportHealth(env, state, detail = {}) {
  const report = {service:'maya-node',state,at:new Date().toISOString(),...detail};
  // Never include raw exceptions, email bodies, recipients, or credentials.
  console[state === 'error' ? 'error' : 'log'](JSON.stringify({health:report}));
  try {
    await env.DB.prepare("CREATE TABLE IF NOT EXISTS runtime_health (id INTEGER PRIMARY KEY CHECK(id=1), report TEXT NOT NULL)").run();
    await env.DB.prepare("INSERT INTO runtime_health(id,report) VALUES(1,?) ON CONFLICT(id) DO UPDATE SET report=excluded.report").bind(JSON.stringify(report)).run();
  } catch { console.error('{"health_report_storage":"failed"}'); }
  if (state === 'error' && env.ALERT_WEBHOOK_URL) {
    try {
      const url = new URL(env.ALERT_WEBHOOK_URL);
      if (url.protocol !== 'https:') throw new Error('Invalid alert URL');
      const headers = {'Content-Type':'application/json'};
      if (env.ALERT_WEBHOOK_TOKEN) headers.Authorization = `Bearer ${env.ALERT_WEBHOOK_TOKEN}`;
      const result = await fetch(url, {method:'POST',headers,body:JSON.stringify(report),signal:AbortSignal.timeout(10000),redirect:'error'});
      if (!result.ok) throw new Error('Alert rejected');
    } catch { console.error('{"health_alert_delivery":"failed"}'); }
  }
}

const REVIEW_LINKS = new Set(['plink_1UFNOZJYOy8NtnKHK8eCz4BP','plink_1UDIsVJYOy8NtnKHxpszTuON']);
const INTAKE_URL = 'https://maya-node-founding-review.myqueen1960.chatgpt.site/intake.html';
export async function verifyStripeSignature(body, header, secret, now = Math.floor(Date.now()/1000)) {
  if (!secret || !header) return false;
  const fields = header.split(',').map(p=>p.trim().split('='));
  const times = fields.filter(([k])=>k==='t');
  if(times.length!==1 || !/^\d+$/.test(times[0][1])) return false;
  const timestamp = Number(times[0][1]);
  if(Math.abs(now-timestamp)>300) return false;
  const key = await crypto.subtle.importKey('raw',new TextEncoder().encode(secret),{name:'HMAC',hash:'SHA-256'},false,['sign']);
  const signature = new Uint8Array(await crypto.subtle.sign('HMAC',key,new TextEncoder().encode(`${timestamp}.${body}`)));
  const expected = Array.from(signature,b=>b.toString(16).padStart(2,'0')).join('');
  return fields.some(([k,v])=>{
    if(k!=='v1' || !/^[0-9a-f]{64}$/.test(v||'')) return false;
    let difference=0;
    for(let i=0;i<64;i++) difference |= expected.charCodeAt(i)^v.charCodeAt(i);
    return difference===0;
  });
}
export function reviewMessages(event) {
  if(!['checkout.session.completed','checkout.session.async_payment_succeeded'].includes(event?.type)) return null;
  const s = event.data?.object;
  if(event.livemode!==true || s?.livemode!==true || (event.account && event.account!=='acct_1TOD3RJYOy8NtnKH')) return null;
  if(s?.mode!=='payment' || s.payment_status!=='paid' || !REVIEW_LINKS.has(s.payment_link) || s.currency!=='usd' || s.amount_total!==2500) return null;
  if(!/^cs_live_[a-zA-Z0-9]{1,160}$/.test(s.id||'')) throw new Error('Invalid session');
  const buyer=s.customer_details?.email || s.customer_email;
  const reference=s.id;
  const body=`Thank you for purchasing your $25 Maya Node Founding Review.\n\nComplete your intake here:\n${INTAKE_URL}\n\nDownload the completed intake file and email it, with authorized supporting materials, to mommommy1960@gmail.com from the email used at checkout. Include your payment date and order reference below.\n\nYour review is human-delivered within five business days after complete intake and usable materials are confirmed. Do not send passwords, private keys, sensitive personal data, or trade secrets.\n\nOrder reference: ${reference}\nSupport, cancellation and refunds: https://maya-node-founding-review.myqueen1960.chatgpt.site/support.html\n\nMya P. Brown\nMaya Node / The Commons Initiative`;
  const messages=[{recipient:buyer,subject:'Maya Node Founding Review — your intake instructions',body},
    {recipient:'mommommy1960@gmail.com',subject:'Maya Node — new paid $25 review',body:`A $25 Maya Node Founding Review was paid through Stripe.\n\nCheckout email: ${buyer}\nOrder reference: ${reference}\nPayment link: ${s.payment_link}\n\nThe buyer's intake email is handled by the payment delivery queue. Confirm complete intake before starting the five-business-day review period. Check the payment in Stripe before any refund or delivery decision.`}];
  for(const message of messages) payloadText(message);
  return {reference,messages};
}
export async function fulfillStripeEvent(event, env, senderFactory = gmailSender) {
  const order=reviewMessages(event);
  if(!order) return {ignored:true};
  if(env.SEND_ENABLED!=='true') throw new Error('Mail delivery disabled');
  const digest=new Uint8Array(await crypto.subtle.digest('SHA-256',new TextEncoder().encode(order.reference)));
  const base='stripe_'+Array.from(digest,b=>b.toString(16).padStart(2,'0')).join('');
  const ids=order.messages.map((_,i)=>`${base}_${i}`);
  for(let i=0;i<ids.length;i++) {
    const payload=payloadText(order.messages[i]);
    await env.DB.prepare("INSERT INTO jobs(id,payload,state) VALUES (?,?,'queued') ON CONFLICT(id) DO NOTHING").bind(ids[i],payload).run();
    const row=await env.DB.prepare('SELECT payload,state FROM jobs WHERE id=?').bind(ids[i]).first();
    if(row?.payload!==payload) throw new Error('Payload conflict');
    if(['unknown','dispatch_committed','canceled','pending'].includes(row.state)) throw new Error('Dispatch requires review');
  }
  const sender=await senderFactory(env); // OAuth failures leave jobs queued for a safe retry.
  for(const id of ids) {
    await dispatch(env.DB,id,sender);
    const row=await env.DB.prepare('SELECT state FROM jobs WHERE id=?').bind(id).first();
    if(row?.state!=='sent') throw new Error('Dispatch requires review');
  }
  return {accepted:true};
}
export async function stripeWebhook(request,env) {
  if(request.method!=='POST') return new Response('Method not allowed',{status:405});
  if(!env.STRIPE_WEBHOOK_SECRET || !env.DB) return new Response('Payment handoff unavailable',{status:503});
  const length=Number(request.headers.get('content-length')||0);
  if(length>262144) return new Response('Too large',{status:413});
  const body=await request.text();
  if(new TextEncoder().encode(body).length>262144) return new Response('Too large',{status:413});
  if(!await verifyStripeSignature(body,request.headers.get('stripe-signature'),env.STRIPE_WEBHOOK_SECRET)) return new Response('Invalid signature',{status:400});
  let event;
  try {event=JSON.parse(body);} catch {return new Response('Invalid event',{status:400});}
  try {
    const result=await fulfillStripeEvent(event,env);
    return Response.json(result,{headers:{'Cache-Control':'no-store'}});
  } catch(error) {
    await reportHealth(env,'error',{...safeFailure(error),source:'stripe_payment_handoff'});
    return new Response('Payment handoff requires retry or review',{status:503});
  }
}

export default {
  async fetch(request,env) {
    if(new URL(request.url).pathname==='/stripe/webhook') return stripeWebhook(request,env);
    if (!env.CONTROLLER_TOKEN || request.headers.get('Authorization') !== `Bearer ${env.CONTROLLER_TOKEN}`) return new Response('Unauthorized',{status:401});
    try {
      const url=new URL(request.url);
      if (request.method==='GET' && url.pathname==='/health') {
        await env.DB.prepare("CREATE TABLE IF NOT EXISTS runtime_health (id INTEGER PRIMARY KEY CHECK(id=1), report TEXT NOT NULL)").run();
        const row=await env.DB.prepare("SELECT report FROM runtime_health WHERE id=1").first();
        return Response.json({latest:row ? JSON.parse(row.report) : null, alert_route_configured:Boolean(env.ALERT_WEBHOOK_URL)});
      }
      if (request.method==='GET' && url.pathname==='/status') {
        const rows=await env.DB.prepare('SELECT state,COUNT(*) AS count FROM jobs GROUP BY state').all();
        return Response.json(rows.results);
      }
      if (request.method!=='POST') return new Response('Not found',{status:404});
      const text=await request.text();
      if(text.length>24000) return new Response('Too large',{status:413});
      const data=JSON.parse(text);
      if(url.pathname==='/mail-config-check') {
        const checks = {};
        for(const key of ['GMAIL_CLIENT_ID','GMAIL_CLIENT_SECRET','GMAIL_REFRESH_TOKEN']) {
          if(typeof data[key] !== 'string' || !data[key]) return new Response('Expected comparison values missing',{status:400});
          const actual = typeof env[key] === 'string' ? env[key] : '';
          checks[key] = {matches:actual === data[key],matches_after_trim:actual.trim() === data[key].trim()};
        }
        return Response.json(checks,{headers:{'Cache-Control':'no-store'}});
      }
      if(typeof data.id!=='string'||! /^[a-zA-Z0-9_-]{1,100}$/.test(data.id)) throw new Error('Invalid id');
      if(url.pathname==='/enqueue') {
        const payload=payloadText(data.payload);
        await env.DB.prepare("INSERT INTO jobs(id,payload,state) VALUES (?,?,'pending') ON CONFLICT(id) DO NOTHING").bind(data.id,payload).run();
        const existing=await env.DB.prepare('SELECT payload FROM jobs WHERE id=?').bind(data.id).first();
        if(existing.payload!==payload) return new Response('Payload conflict',{status:409});
      } else if(url.pathname==='/approve') {
        // Approval includes the exact payload, preventing approval of unseen content.
        const result=await env.DB.prepare("UPDATE jobs SET state='queued' WHERE id=? AND payload=? AND state='pending'").bind(data.id,payloadText(data.payload)).run();
        if(!result.meta.changes) return new Response('Not approvable',{status:409});
      } else if(url.pathname==='/cancel') {
        await env.DB.prepare("UPDATE jobs SET state='canceled' WHERE id=? AND state IN ('pending','queued')").bind(data.id).run();
        const row=await env.DB.prepare('SELECT state FROM jobs WHERE id=?').bind(data.id).first();
        if(!row) return new Response('Not found',{status:404});
        return Response.json({result:row.state==='canceled'?'canceled':'too_late'});
      } else return new Response('Not found',{status:404});
      return Response.json({ok:true});
    } catch {return new Response('Invalid request or unavailable database',{status:400});}
  },
  async scheduled(event,env) {
    if(env.SEND_ENABLED!=='true') {await reportHealth(env,'disabled'); return;}
    try {
    const sender=await gmailSender(env); // authenticate before claiming jobs
    const rows=await env.DB.prepare("SELECT id FROM jobs WHERE state='queued' LIMIT 3").all();
    for(const row of rows.results) await dispatch(env.DB,row.id,sender);
    const alerts=await env.DB.prepare("SELECT id,state FROM jobs WHERE state IN ('unknown','dispatch_committed') LIMIT 20").all();
    if(alerts.results.length) await reportHealth(env,'error',{code:'dispatch_requires_review',affected_jobs:alerts.results.length});
    else await reportHealth(env,'ok');
    } catch(error) {
      await reportHealth(env,'error',safeFailure(error));
      throw error;
    }
  }
};
