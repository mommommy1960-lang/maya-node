export const HTML = `<!DOCTYPE html>
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
<p id="billing-status" role="status"></p>
<button id="discover-subscription" style="background:#0f766e">Find Existing Paid Sandbox Subscription</button>
<p id="discovery-status" class="muted" role="status"></p>
<button id="link-discovered" hidden style="background:#059669">Link Verified Subscription to Owner Demo</button>
<button id="billing-refresh">Refresh Subscription Status</button>
<details><summary>Link the existing paid practice subscription</summary><p class="muted">Copy the subscription ID beginning sub_ from your Stripe Sandbox subscription. This links it to this owner demo only.</p>
<input id="subscription-id" aria-label="Existing sandbox subscription ID" placeholder="sub_…"><button id="import">Link Existing Practice Subscription</button></details>
<button id="portal" hidden>Manage Subscription in Stripe</button><button id="cancel" hidden style="background:#b45309">Cancel Renewal at Period End</button>
<p id="action-status" role="status"></p></div></div></div>
<script>
let discoveredSubscriptionId='';
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
async function discoverSubscription(){
  const status=el('discovery-status');status.textContent='Searching the configured Stripe sandbox for the existing owner subscription…';
  el('link-discovered').hidden=true;discoveredSubscriptionId='';
  const d=await api('/api/stripe/discover');
  if(!d.found){status.textContent=d.message||'No matching subscription found.';return;}
  discoveredSubscriptionId=d.subscription_id;
  status.textContent='Verified one paid, active sandbox subscription. Paid period ends '+new Date(d.period_end*1000).toLocaleString()+'. No billing or database changes have been made.';
  el('link-discovered').hidden=false;
}
action('discover-subscription',discoverSubscription);
action('link-discovered',async()=>{
  if(!discoveredSubscriptionId)throw Error('Run the read-only discovery again before linking.');
  if(!confirm('Link the verified sandbox subscription to this owner demo? This writes the owner billing record in the connected staging database.'))return;
  await api('/api/stripe/import',{subscriptionId:discoveredSubscriptionId,confirmOwnerImport:true});
  el('discovery-status').textContent='Subscription linked to the owner demo after your confirmation.';
  discoveredSubscriptionId='';el('link-discovered').hidden=true;await checkAccess();
});
action('test-stripe',testStripeAuth);action('billing-refresh',checkAccess);
action('checkout',async()=>{const d=await api('/api/stripe/checkout',{});if(d.livemode!==false||!d.url.startsWith('https://checkout.stripe.com/'))throw Error('Invalid sandbox checkout response');location.href=d.url;});
action('import',async()=>{const subscriptionId=el('subscription-id').value.trim();if(!/^sub_[a-zA-Z0-9]+$/.test(subscriptionId))throw Error('Enter the Stripe Sandbox subscription ID beginning sub_.');if(!confirm('Link this subscription to your owner sandbox demo?'))return;await api('/api/stripe/import',{subscriptionId,confirmOwnerImport:true});el('action-status').textContent='Practice subscription linked and verified.';await checkAccess();});
action('portal',async()=>{const d=await api('/api/stripe/portal',{});if(!d.url.startsWith('https://billing.stripe.com/'))throw Error('Invalid Stripe portal URL');location.href=d.url;});
action('cancel',async()=>{if(!confirm('Cancel renewal of this sandbox practice subscription at its paid period end?'))return;const d=await api('/api/stripe/cancel',{});el('action-status').textContent=d.message;await checkAccess();});
if(sessionToken)showApp();
</script></body></html>`;
