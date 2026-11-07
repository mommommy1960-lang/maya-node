import { evaluateTransfer } from "./matching.mjs";
import { planAlerts } from "./alerts.mjs";
/** Synthetic demonstration only. Does not contact pantries, reserve resources, or charge money. */
export function buildWatchtower({ offers, needs, receivers, vehicles, contacts = [], now = new Date() }) {
  const proposals = [];
  const blocked = [];
  const notifications = [];
  for (const offer of offers) {
    for (const need of needs) {
      const receiver = receivers.find(r => r.pantryId === need.pantryId);
      const vehicle = vehicles.find(v => v.available && v.handling === offer.handling);
      const result = evaluateTransfer(offer, need, receiver, vehicle, now);
      const record = { offerId:offer.id, needId:need.id, from:offer.pantryId, to:need.pantryId, ...result };
      if (result.eligible) {
        proposals.push(record);
        notifications.push(...planAlerts({
          id: offer.id + ":" + need.id, state:"pending", createdAt:offer.observedAt,
          deadline:need.receivingUntil, acknowledged:false
        }, contacts, now));
      } else blocked.push(record);
    }
  }
  return { asOf:now.toISOString(), synthetic:true, proposals, blocked, notifications, liveDispatchEnabled:false, paymentEnabled:false };
}
