/** Synthetic shipment chain-of-custody reconciliation. No allegations or external actions. */
export function reconcileShipment(shipment) {
  if (!shipment?.id || !Number.isSafeInteger(shipment.loaded) || shipment.loaded < 0 ||
      !Array.isArray(shipment.receipts)) throw new Error("invalid_shipment");
  const seen = new Set();
  let received = 0, rejected = 0, damaged = 0;
  const errors = [];
  for (const r of shipment.receipts) {
    if (!r?.id || seen.has(r.id)) { errors.push("duplicate_or_missing_receipt_id"); continue; }
    seen.add(r.id);
    if (!r.confirmedBy || !r.recordedAt || !Number.isFinite(Date.parse(r.recordedAt))) {
      errors.push("unverified_receipt"); continue;
    }
    for (const key of ["received","rejected","damaged"]) {
      if (!Number.isSafeInteger(r[key] ?? 0) || (r[key] ?? 0) < 0) errors.push("invalid_receipt_quantity");
    }
    if (errors.length) continue;
    received += r.received ?? 0;
    rejected += r.rejected ?? 0;
    damaged += r.damaged ?? 0;
  }
  const accounted = received + rejected + damaged;
  const difference = shipment.loaded - accounted;
  return {
    shipmentId: shipment.id, loaded:shipment.loaded, received, rejected, damaged,
    difference, status:errors.length ? "needs_record_review" :
      difference === 0 ? "reconciled" : "discrepancy_requires_review",
    errors, automatedAccusation:false, synthetic:true
  };
}
