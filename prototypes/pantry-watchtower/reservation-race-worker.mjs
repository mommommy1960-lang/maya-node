/** Separate OS-process contender for synthetic SQLite reservation races.
 * Test-only worker. No network, pantry data, dispatch or billing.
 */
import { ReservationLedger } from './reservation-ledger.mjs';
import { SyntheticOrderStore } from './synthetic-order-store.mjs';

const [file, operation, identifier] = process.argv.slice(2);
if (!file || !operation) throw Error('race_worker_arguments_required');
const items = [
  { resourceId: 'food', quantity: 5 },
  { resourceId: 'freezer', quantity: 5 },
  { resourceId: 'truck', quantity: 1 }
];
const ledger = new ReservationLedger(file);
try {
  const orders = new SyntheticOrderStore(ledger);
  let value;
  try {
    switch (operation) {
      case 'claim':
        value = ledger.reserveBundle({ id: identifier, items, expiresAt: 400 }, 201);
        break;
      case 'expire-order':
        value = orders.expireDue(201);
        break;
      case 'pickup':
        orders.pickup({ id: 'race-order', actorId: 'transport', evidenceRef: 'synthetic-pickup-proof', at: 150 });
        value = true;
        break;
      case 'cancel':
        orders.cancel({ id: 'race-order', actorId: 'donor', evidenceRef: 'synthetic-cancel-proof', at: 150 });
        value = true;
        break;
      default:
        throw Error('unknown_race_worker_operation');
    }
    console.log(JSON.stringify({ ok: true, value }));
  } catch (err) {
    // State conflicts are expected in these races; infrastructure faults
    // such as SQLITE_BUSY must remain observable in the parent test.
    console.log(JSON.stringify({ ok: false, error: err?.message ?? String(err) }));
  }
} finally {
  ledger.close();
}
