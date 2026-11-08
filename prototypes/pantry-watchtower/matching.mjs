/** Synthetic-only pantry watchtower matching core. No network, dispatch, or customer data. */
export function evaluateTransfer(offer, need, receiver, vehicle, now = new Date()) {
  const reasons = [];
  const validTime = value => Number.isFinite(Date.parse(value));
  const fresh = record => validTime(record.observedAt) &&
    Date.parse(record.observedAt) <= now.getTime() &&
    now.getTime() - Date.parse(record.observedAt) <= 15 * 60_000 &&
    record.status === "confirmed";
  if (!offer || !need || !receiver || !vehicle) return { eligible: false, reasons: ["missing_input"] };
  if (!fresh(offer) || !fresh(need) || !fresh(receiver) || !fresh(vehicle)) reasons.push("unverified_or_stale");
  if (offer.foodType !== need.foodType) reasons.push("food_mismatch");
  if (offer.recalled === true) reasons.push("recalled_lot");
  else if (offer.recalled != null && offer.recalled !== false) reasons.push("invalid_recall_status");
  if (need.requiresHalal != null && need.requiresHalal !== false &&
      (need.requiresHalal !== true || offer.halalVerified !== true)) reasons.push("halal_unverified");
  if (need.size != null && offer.size !== need.size) reasons.push("item_size_mismatch");
  if (offer.unit !== need.unit) reasons.push("quantity_unit_mismatch");
  if (vehicle.estimatedArrival != null) {
    const arrival = Date.parse(vehicle.estimatedArrival);
    if (!Number.isFinite(arrival) || arrival < now.getTime()) reasons.push("invalid_arrival_estimate");
    else if (arrival >= Math.min(Date.parse(need.receivingUntil), Date.parse(offer.expiresAt))) {
      reasons.push("arrival_outside_safe_window");
    }
  }
  if (offer.handling !== receiver.handling || offer.handling !== vehicle.handling) reasons.push("handling_mismatch");
  if (![offer.quantity, need.quantity, receiver.freeCapacity, vehicle.capacity].every(x => Number.isFinite(x) && x > 0)) reasons.push("invalid_capacity");
  if (!validTime(offer.expiresAt) || Date.parse(offer.expiresAt) <= now.getTime()) reasons.push("expired_food");
  if (!validTime(need.receivingUntil) || Date.parse(need.receivingUntil) <= now.getTime()) reasons.push("receiving_window_closed");
  if (vehicle.available !== true) reasons.push("vehicle_unavailable");
  const quantity = Math.min(offer.quantity, need.quantity, receiver.freeCapacity, vehicle.capacity);
  return { eligible: reasons.length === 0, quantity: reasons.length ? 0 : quantity, reasons,
    state: reasons.length ? "blocked" : "proposal_only", requires: ["donor_approval", "receiver_approval", "transport_confirmation"] };
}
export function recordEvent(log, event) {
  if (!event?.id || !event?.type || !event?.observedAt || !event?.source) throw new Error("incomplete_event");
  if (log.some(existing => existing.id === event.id)) return log;
  return [...log, Object.freeze({ ...event })];
}

