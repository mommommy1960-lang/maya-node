import { evaluateTransfer } from "./matching.mjs";
import { planAlerts } from "./alerts.mjs";

/** Synthetic proposals only. Track remaining quantities and allocate each truck once per snapshot. */
export function buildWatchtower({ offers, needs, receivers, vehicles, contacts = [], now = new Date() }) {
  const proposals = [], notifications = [];
  const blocked = new Map();
  const availableTrucks = new Set(vehicles.map(vehicle => vehicle.id));
  const uniqueOffers = new Map();
  for (const offer of offers) {
    if (!uniqueOffers.has(offer.id)) uniqueOffers.set(offer.id, offer);
  }
  const remainingOffer = new Map([...uniqueOffers].map(([id, offer]) => [id, offer.quantity]));
  const proposedPairs = new Set();
  const storageKey = (pantryId, handling) => JSON.stringify([pantryId, handling]);
  const storageByType = new Map();
  for (const receiver of receivers) {
    const key = storageKey(receiver.pantryId, receiver.handling);
    if (!storageByType.has(key)) storageByType.set(key, { ...receiver });
  }

  const receivingDeadline = need => Date.parse(need.receivingUntil) || Infinity;
  const prioritizedNeeds = [...needs].sort((a, b) => receivingDeadline(a) - receivingDeadline(b));
  const uniqueNeeds = new Map();
  for (const need of prioritizedNeeds) {
    if (!uniqueNeeds.has(need.id)) uniqueNeeds.set(need.id, need);
  }
  const remainingNeeds = new Map([...uniqueNeeds].map(([id, need]) => [id, need.quantity]));

  // Give each distinct lot a first chance at a trip before splitting surplus across more trucks.
  for (const allowSplits of [false, true]) {
    const offeredThisPass = new Set();
    for (const need of uniqueNeeds.values()) {
      for (const offer of uniqueOffers.values()) {
        const quantity = remainingOffer.get(offer.id);
        const remainingNeed = remainingNeeds.get(need.id);
        if (remainingNeed === 0) break;
        if (!offer.id || !need.id || offer.pantryId === need.pantryId || quantity === 0) continue;
        if (!allowSplits && offeredThisPass.has(offer.id)) continue;

        const receiver = storageByType.get(storageKey(need.pantryId, offer.handling))
          ?? receivers.find(entry => entry.pantryId === need.pantryId);
        const candidates = vehicles.filter(vehicle =>
          vehicle.handling === offer.handling && availableTrucks.has(vehicle.id));
        const pair = JSON.stringify([offer.id, need.id]);
        let rejection;
        for (const vehicle of candidates.length ? candidates : [undefined]) {
          const result = evaluateTransfer({ ...offer, quantity }, { ...need, quantity: remainingNeed }, receiver, vehicle, now);
          const record = { offerId: offer.id, needId: need.id, from: offer.pantryId, to: need.pantryId,
            vehicleId: vehicle?.id ?? null, ...result };
          if (!result.eligible) {
            rejection ??= record;
            continue;
          }
          availableTrucks.delete(vehicle.id);
          offeredThisPass.add(offer.id);
          remainingOffer.set(offer.id, quantity - result.quantity);
          remainingNeeds.set(need.id, remainingNeed - result.quantity);
          receiver.freeCapacity -= result.quantity;
          proposals.push(record);
          const alertId = proposedPairs.has(pair) ? JSON.stringify([offer.id, need.id, vehicle.id]) : offer.id + ":" + need.id;
          proposedPairs.add(pair);
          notifications.push(...planAlerts({ id: alertId, state: "pending",
            createdAt: offer.observedAt, deadline: need.receivingUntil, acknowledged: false }, contacts, now));
          blocked.delete(pair);
          rejection = undefined;
          break;
        }
        if (rejection && !proposedPairs.has(pair) && !blocked.has(pair)) blocked.set(pair, rejection);
      }
    }
  }
  return { asOf: now.toISOString(), synthetic: true, proposals, blocked: [...blocked.values()], notifications,
    liveDispatchEnabled: false, paymentEnabled: false };
}
