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

export default {
  async fetch(request,env) {
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
