// Integrated review candidate based on the owner-supplied active Worker.
// Preserves bearer owner login, existing table names and fp8 model. NOT DEPLOYED.
import { HTML } from './ui.mjs';
import { OWNER_ID, OWNER_EMAIL, webhook, ownerBilling, stripe, testKey } from './payments.mjs';

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
