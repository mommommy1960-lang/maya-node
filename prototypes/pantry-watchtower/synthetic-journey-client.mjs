/** Local-only fictional operations UI. Never accepts third-party user data. */
const byId = id => document.getElementById(id);
const actions = [...document.querySelectorAll('[data-action]')];
let busy = false;
let state = null;
const describe = status => ({ reserved: 'Fictional resources reserved, awaiting approvals.', approved: 'Three fictional approvals logged. Pickup may proceed.', picked_up: 'Fictional pickup logged; receiver receipt needed.', exception: 'Delivery discrepancy recorded. Human review would be required in a real system.', reconciled: 'Fictional receipt and order reconciled. No physical transfer occurred.', canceled: 'Fictional order canceled and unused capacity released.', expired: 'Fictional order expired.' })[status] || 'No order has been started.';
function render(s) {
  state = s;
  const order = s.order; const status = order?.state;
  const commercial = s.commercial;
  byId('commercial').textContent = commercial
    ? 'LOCAL MOCK only (not Stripe). Fictional sponsor quote 
  byId('status').textContent = describe(status);
  for (const name of ['food', 'cold', 'truck']) byId(name).textContent = String(s.capacity[name]);
  byId('receipt').textContent = s.receipt ? s.receipt.received + ' accepted, ' + s.receipt.rejected + ' rejected, ' + s.receipt.damaged + ' damaged, ' + s.receipt.missing + ' missing. ' + (s.receipt.disposition ? 'Discrepancy documented.' : '') : 'No receipt yet';
  const events = byId('events'); events.replaceChildren();
  for (const e of order?.events || []) { const li = document.createElement('li'); li.textContent = e.kind.replaceAll('_', ' ') + ' by ' + e.actorId + ' (fictional)'; events.append(li); }
  if (!order) { const li = document.createElement('li'); li.textContent = 'None yet'; events.append(li); }
  const approved = new Set(order?.approvals?.map(a => a.role) || []);
  for (const button of actions) {
    const { action, role } = button.dataset;
    button.disabled = busy || (action === 'start' ? !!order :
      action === 'approve' ? !['reserved','approved'].includes(status) || approved.has(role) :
      action === 'quote' ? status !== 'approved' || !!commercial :
      action === 'accept-terms' ? commercial?.state !== 'quoted' :
      action === 'mock-decline' ? commercial?.state !== 'accepted' || commercial.events.some(e => e.kind === 'mock_declined') :
      action === 'mock-authorize' ? commercial?.state !== 'accepted' :
      action === 'pickup' ? status !== 'approved' || commercial?.state !== 'authorized' :
      action === 'deliver' ? status !== 'picked_up' :
      action === 'document-exception' ? status !== 'exception' :
      action === 'mock-capture' ? status !== 'reconciled' || commercial?.state !== 'authorized' :
      action === 'mock-refund' ? commercial?.state !== 'captured' :
      action === 'cancel' ? !['reserved','approved'].includes(status) : true);
  }
  const steps = [...byId('steps').children];
  const done = [!!order, approved.size === 3, ['authorized','captured','refunded'].includes(commercial?.state),
    ['picked_up','exception','reconciled'].includes(status), !!s.receipt, status === 'reconciled',
    ['captured','refunded'].includes(commercial?.state)];
  steps.forEach((li, i) => { li.className = done[i] ? 'complete' : 'pending'; li.textContent = (done[i] ? '✓ ' : '○ ') + ['Reserve fictional resources', 'Record three fictional approvals', 'Prepare fictional quote, terms and local mock authorization', 'Simulate pickup', 'Record delivery receipt', 'Reconcile or document exception', 'Optional local fake capture/refund'][i]; });
}
async function request(path, payload) {
  const response = await fetch(path, payload ? { method: 'POST', headers: {'Content-Type':'application/json'}, body: JSON.stringify(payload) } : {});
  const data = await response.json();
  if (!response.ok) throw Error(data.error || 'Request failed (' + response.status + ')');
  return data;
}
for (const button of actions) button.addEventListener('click', async () => {
  if (busy || button.disabled) return;
  busy = true; byId('error').textContent = ''; render(state);
  try { render(await request('/api/action', { ...button.dataset })); }
  catch (error) { byId('error').textContent = 'Demo action blocked: ' + error.message + '.'; try { render(await request('/api/state')); } catch {} }
  finally { busy = false; if (state) render(state); }
});
try { render(await request('/api/state')); }
catch { byId('status').textContent = 'Local demo server unavailable.'; byId('error').textContent = 'Start the synthetic local server before using this page.'; } + (commercial.sponsorFeeCents/100).toFixed(2)
      + ' USD; recipient charge $0.00; sample terms ' + commercial.termsVersion
      + '; state: ' + commercial.state + '; fake net 
  byId('status').textContent = describe(status);
  for (const name of ['food', 'cold', 'truck']) byId(name).textContent = String(s.capacity[name]);
  byId('receipt').textContent = s.receipt ? s.receipt.received + ' accepted, ' + s.receipt.rejected + ' rejected, ' + s.receipt.damaged + ' damaged, ' + s.receipt.missing + ' missing. ' + (s.receipt.disposition ? 'Discrepancy documented.' : '') : 'No receipt yet';
  const events = byId('events'); events.replaceChildren();
  for (const e of order?.events || []) { const li = document.createElement('li'); li.textContent = e.kind.replaceAll('_', ' ') + ' by ' + e.actorId + ' (fictional)'; events.append(li); }
  if (!order) { const li = document.createElement('li'); li.textContent = 'None yet'; events.append(li); }
  const approved = new Set(order?.approvals?.map(a => a.role) || []);
  for (const button of actions) {
    const { action, role } = button.dataset;
    button.disabled = busy || (action === 'start' ? !!order :
      action === 'approve' ? !['reserved','approved'].includes(status) || approved.has(role) :
      action === 'pickup' ? status !== 'approved' :
      action === 'deliver' ? status !== 'picked_up' :
      action === 'document-exception' ? status !== 'exception' :
      action === 'cancel' ? !['reserved','approved'].includes(status) : true);
  }
  const steps = [...byId('steps').children];
  const done = [!!order, approved.size === 3, ['picked_up','exception','reconciled'].includes(status), !!s.receipt, status === 'reconciled'];
  steps.forEach((li, i) => { li.className = done[i] ? 'complete' : 'pending'; li.textContent = (done[i] ? '✓ ' : '○ ') + ['Reserve fictional resources', 'Record three fictional approvals', 'Simulate pickup', 'Record delivery receipt', 'Reconcile or document exception'][i]; });
}
async function request(path, payload) {
  const response = await fetch(path, payload ? { method: 'POST', headers: {'Content-Type':'application/json'}, body: JSON.stringify(payload) } : {});
  const data = await response.json();
  if (!response.ok) throw Error(data.error || 'Request failed (' + response.status + ')');
  return data;
}
for (const button of actions) button.addEventListener('click', async () => {
  if (busy || button.disabled) return;
  busy = true; byId('error').textContent = ''; render(state);
  try { render(await request('/api/action', { ...button.dataset })); }
  catch (error) { byId('error').textContent = 'Demo action blocked: ' + error.message + '.'; try { render(await request('/api/state')); } catch {} }
  finally { busy = false; if (state) render(state); }
});
try { render(await request('/api/state')); }
catch { byId('status').textContent = 'Local demo server unavailable.'; byId('error').textContent = 'Start the synthetic local server before using this page.'; } + (commercial.simulatedNetCents/100).toFixed(2) + '.'
    : 'No fictional quote yet. Recipient never pays in this demonstration.';
  byId('status').textContent = describe(status);
  for (const name of ['food', 'cold', 'truck']) byId(name).textContent = String(s.capacity[name]);
  byId('receipt').textContent = s.receipt ? s.receipt.received + ' accepted, ' + s.receipt.rejected + ' rejected, ' + s.receipt.damaged + ' damaged, ' + s.receipt.missing + ' missing. ' + (s.receipt.disposition ? 'Discrepancy documented.' : '') : 'No receipt yet';
  const events = byId('events'); events.replaceChildren();
  for (const e of order?.events || []) { const li = document.createElement('li'); li.textContent = e.kind.replaceAll('_', ' ') + ' by ' + e.actorId + ' (fictional)'; events.append(li); }
  if (!order) { const li = document.createElement('li'); li.textContent = 'None yet'; events.append(li); }
  const approved = new Set(order?.approvals?.map(a => a.role) || []);
  for (const button of actions) {
    const { action, role } = button.dataset;
    button.disabled = busy || (action === 'start' ? !!order :
      action === 'approve' ? !['reserved','approved'].includes(status) || approved.has(role) :
      action === 'pickup' ? status !== 'approved' :
      action === 'deliver' ? status !== 'picked_up' :
      action === 'document-exception' ? status !== 'exception' :
      action === 'cancel' ? !['reserved','approved'].includes(status) : true);
  }
  const steps = [...byId('steps').children];
  const done = [!!order, approved.size === 3, ['picked_up','exception','reconciled'].includes(status), !!s.receipt, status === 'reconciled'];
  steps.forEach((li, i) => { li.className = done[i] ? 'complete' : 'pending'; li.textContent = (done[i] ? '✓ ' : '○ ') + ['Reserve fictional resources', 'Record three fictional approvals', 'Simulate pickup', 'Record delivery receipt', 'Reconcile or document exception'][i]; });
}
async function request(path, payload) {
  const response = await fetch(path, payload ? { method: 'POST', headers: {'Content-Type':'application/json'}, body: JSON.stringify(payload) } : {});
  const data = await response.json();
  if (!response.ok) throw Error(data.error || 'Request failed (' + response.status + ')');
  return data;
}
for (const button of actions) button.addEventListener('click', async () => {
  if (busy || button.disabled) return;
  busy = true; byId('error').textContent = ''; render(state);
  try { render(await request('/api/action', { ...button.dataset })); }
  catch (error) { byId('error').textContent = 'Demo action blocked: ' + error.message + '.'; try { render(await request('/api/state')); } catch {} }
  finally { busy = false; if (state) render(state); }
});
try { render(await request('/api/state')); }
catch { byId('status').textContent = 'Local demo server unavailable.'; byId('error').textContent = 'Start the synthetic local server before using this page.'; }