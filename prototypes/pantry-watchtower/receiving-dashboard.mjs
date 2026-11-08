/** Fictional receiving dashboard. Each accepted event updates one in-memory snapshot. */
const initialShipments = [
  { id: 'SYN-DAIRY', label: 'Milk cartons', storage: 'chilled', expected: 15, state: 'accepted' },
  { id: 'SYN-PRODUCE', label: 'Produce cartons', storage: 'ambient', expected: 10, state: 'accepted' },
  { id: 'SYN-DRY', label: 'Dry goods cartons', storage: 'ambient', expected: 15, state: 'accepted' },
  { id: 'SYN-GRAINS', label: 'Grain cartons', storage: 'ambient', expected: 5, state: 'pending' }
];
const fixtureEvents = {
  outage: { id: 'SYN-OUTAGE-1', type: 'outage' },
  cancel: { id: 'SYN-CANCEL-1', type: 'cancel', shipmentId: 'SYN-PRODUCE' },
  short: { id: 'SYN-RECEIPT-1', type: 'receipt', shipmentId: 'SYN-DRY', received: 12 },
  accept: { id: 'SYN-ACCEPT-1', type: 'accept', shipmentId: 'SYN-GRAINS' },
  decline: { id: 'SYN-DECLINE-1', type: 'decline', shipmentId: 'SYN-GRAINS' },
  hold: { id: 'SYN-HOLD-1', type: 'hold', shipmentId: 'SYN-GRAINS' }
};
const holdsSpace = shipment => shipment.state === 'accepted' || shipment.reservationRetained === true;

export function createReceivingDashboard(clock = () => Date.now()) {
  const shipments = initialShipments.map(shipment => ({ ...shipment }));
  const storage = {
    chilled: { total: 100, occupied: 60, online: true },
    ambient: { total: 100, occupied: 60, online: true }
  };
  const events = new Map();
  let updatedAt = clock();

  function capacity() {
    return Object.fromEntries(Object.entries(storage).map(([kind, space]) => {
      const reserved = shipments.filter(s => s.storage === kind && holdsSpace(s))
        .reduce((sum, s) => sum + s.expected, 0);
      return [kind, { ...space, reserved, available: space.online ? Math.max(0, space.total - space.occupied - reserved) : 0 }];
    }));
  }

  function snapshot(view = 'staff') {
    const summary = {
      pending: shipments.filter(s => s.state === 'pending').length,
      accepted: shipments.filter(s => s.state === 'accepted').length,
      held: shipments.filter(s => s.state === 'held').length,
      canceled: shipments.filter(s => s.state === 'canceled').length,
      declined: shipments.filter(s => s.state === 'declined').length,
      received: shipments.reduce((sum, s) => sum + (s.received ?? 0), 0),
      short: shipments.reduce((sum, s) => sum + (s.short ?? 0), 0)
    };
    const shared = { synthetic: true, revision: events.size, updatedAt, summary };
    return view === 'sponsor' ? shared : {
      ...shared, capacity: capacity(), shipments: shipments.map(s => ({ ...s })),
      events: [...events.values()].map(event => ({ ...event }))
    };
  }

  function applyFixture(action) {
    const event = action === 'duplicate' ? fixtureEvents.short : fixtureEvents[action];
    if (!Object.hasOwn(fixtureEvents, action) && action !== 'duplicate') throw Error('unknown_receiving_fixture');
    if (action === 'duplicate' && !events.has(event.id)) throw Error('receiving_duplicate_needs_original');
    if (events.has(event.id)) return { outcome: 'duplicate', ...snapshot() };
    const shipment = shipments.find(s => s.id === event.shipmentId);
    if (event.type === 'outage') {
      storage.chilled.online = false;
      for (const s of shipments) {
        if (s.storage === 'chilled' && s.state === 'accepted') {
          s.state = 'held';
          s.reservationRetained = true;
          s.reason = 'Cooler outage. Staff must confirm an alternative.';
        }
      }
    } else if (event.type === 'cancel') {
      if (shipment.state !== 'accepted') throw Error('receiving_fixture_transition_denied');
      shipment.state = 'canceled';
      shipment.reason = 'Truck canceled. A replacement needs approval.';
    } else if (event.type === 'receipt') {
      if (shipment.state !== 'accepted' || !storage[shipment.storage].online) throw Error('receiving_fixture_transition_denied');
      shipment.state = 'received';
      shipment.received = event.received;
      shipment.short = shipment.expected - event.received;
      shipment.reason = 'Staff review the difference against the receiving count.';
      storage[shipment.storage].occupied += event.received;
    } else {
      if (shipment.state !== 'pending') throw Error('receiving_fixture_transition_denied');
      if (event.type === 'accept' && capacity()[shipment.storage].available < shipment.expected) {
        throw Error('receiving_fixture_insufficient_space');
      }
      shipment.state = { accept: 'accepted', decline: 'declined', hold: 'held' }[event.type];
      shipment.reason = { accept: 'Staff accepted and reserved space.', decline: 'Staff declined.',
        hold: 'Staff paused this decision for review.' }[event.type];
    }
    updatedAt = clock();
    events.set(event.id, { ...event, at: updatedAt });
    return { outcome: 'applied', ...snapshot() };
  }
  return { snapshot, applyFixture };
}
