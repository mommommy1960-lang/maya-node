/** Test-only browser interface for the server-injected, spoofable fictional tenant gate.
 * No client role selector and no credentials. Every HTTP action is authorized server-side.
 */
const status = document.querySelector('#status');
const state = document.querySelector('#order-state');
const approvals = document.querySelector('#approvals');
const receipt = document.querySelector('#receipt');
const buttons = [...document.querySelectorAll('button[data-action]')];
function render(data) {
  const order = data?.order;
  state.textContent = order ? 'Fictional order state: ' + order.state : 'Order not available';
  approvals.textContent = order
    ? 'Approvals: ' + (order.approvals?.length ?? 0) + ' of 3 fictional participants'
    : 'Approvals: not available';
  const r = data?.receipt;
  receipt.textContent = r
    ? 'Receipt: ' + r.received + ' received; ' + r.rejected + ' rejected; ' + r.missing +
      ' missing; disposition ' + (r.disposition?.code ?? 'none')
    : 'Receipt: not available for this fictional principal';
}
async function request(action, mode) {
  status.textContent = 'Checking fictional permissions…';
  buttons.forEach(button => { button.disabled = true; });
  try {
    const init = action
      ? { method: 'POST', headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ action, ...(mode ? {mode} : {}) }) }
      : { method: 'GET' };
    const response = await fetch('/api/tenant-order', init);
    const data = await response.json();
    if (!response.ok) {
      // Do not render previous sensitive state after a denial.
      render(null);
      status.textContent = 'Blocked (' + response.status + '): ' + (data.error || 'not permitted');
      return;
    }
    render(data);
    status.textContent = action ? 'Completed fictional action: ' + action : 'Authorized fictional view';
  } catch {
    render(null);
    status.textContent = 'Unavailable: local fictional server could not be reached';
  } finally {
    buttons.forEach(button => { button.disabled = false; });
  }
}
document.querySelector('#refresh').addEventListener('click', () => request());
buttons.forEach(button => button.addEventListener('click', () =>
  request(button.dataset.action, button.dataset.mode)));
request();