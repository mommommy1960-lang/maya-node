let view = 'staff';
let generation = 0;
let busy = false;
let shown = null;
let nextRequest = 0;
let lastResponse = 0;
const get = id => document.getElementById(id);
const actionButtons = [...document.querySelectorAll('[data-action]')];
const labels = { pending: 'Awaiting decision', accepted: 'Expected', held: 'On hold',
  canceled: 'Canceled', declined: 'Declined', received: 'Received cartons', short: 'Cartons to review' };
const list = (id, entries) => get(id).replaceChildren(...entries.map(text => {
  const li = document.createElement('li');
  li.textContent = text;
  return li;
}));

function render(state) {
  get('connection').textContent = 'Connected to synthetic feed · last event ' +
    new Date(state.updatedAt).toLocaleTimeString() + ' · checked ' + new Date().toLocaleTimeString() + ' · revision ' + state.revision;
  if (shown === state.revision) return;
  shown = state.revision;
  get('summary').replaceChildren(...Object.entries(state.summary).map(([key, value]) => {
    const card = document.createElement('div');
    const count = document.createElement('strong');
    count.textContent = value;
    card.append(count, labels[key]);
    return card;
  }));
  if (view === 'sponsor') return;
  list('capacity', Object.entries(state.capacity).map(([type, s]) =>
    type + ': ' + s.available + ' available · ' + s.occupied + ' occupied · ' + s.reserved + ' reserved' + (s.online ? '' : ' · offline')));
  list('shipments', state.shipments.map(s => s.label + ': ' + s.state +
    ' · ' + s.expected + ' expected' + (s.received == null ? '' : ' · ' + s.received + ' received · ' + s.short + ' short') +
    (s.reason ? ' · ' + s.reason : '')));
  list('events', state.events.map(e => e.id + ' · ' + e.type + ' · ' + new Date(e.at).toLocaleTimeString()));
}

async function refresh() {
  const requested = generation;
  const request = ++nextRequest;
  try {
    const response = await fetch('/api/receiving' + (view === 'sponsor' ? '/sponsor' : ''), { cache: 'no-store' });
    if (!response.ok) throw Error();
    const state = await response.json();
    if (requested === generation && request > lastResponse) {
      lastResponse = request;
      render(state);
    }
  } catch {
    if (requested === generation && request > lastResponse) {
      lastResponse = request;
      get('connection').textContent = 'Feed unavailable. Displayed data may be stale.';
    }
  }
}
document.querySelectorAll('[data-view]').forEach(button => button.onclick = () => {
  view = button.dataset.view;
  generation++;
  shown = null;
  get('summary').replaceChildren();
  get('staff').hidden = view !== 'staff';
  get('view-title').textContent = view === 'staff' ? 'Staff operations' : 'Sponsor summary';
  document.querySelectorAll('[data-view]').forEach(b => b.setAttribute('aria-pressed', String(b === button)));
  refresh();
});
actionButtons.forEach(button => button.onclick = async () => {
  if (busy) return;
  busy = true;
  actionButtons.forEach(b => b.disabled = true);
  try {
    const response = await fetch('/api/receiving/fixture', {
      method: 'POST', headers: { 'content-type': 'application/json' }, body: JSON.stringify({ action: button.dataset.action })
    });
    const data = await response.json();
    get('feedback').textContent = response.ok ? (data.outcome === 'duplicate' ? 'Duplicate ignored. Counts unchanged.' : 'Update recorded.') :
      data.error === 'receiving_duplicate_needs_original' ? 'Record the short delivery first.' : 'That action is unavailable in the current state.';
    await refresh();
  } catch { get('feedback').textContent = 'Could not send the simulated update.'; }
  finally { busy = false; actionButtons.forEach(b => b.disabled = false); }
});
refresh();
setInterval(refresh, 1000);
