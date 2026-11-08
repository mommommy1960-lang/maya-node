import { reconcileShipment } from "./reconciliation.mjs";

/** Review a fictional one-pantry receiving export. No connector, write-back or dispatch. */
export function reviewPantryReceiving(batch, asOf) {
  const at = Date.parse(asOf);
  if (batch?.synthetic !== true || !Array.isArray(batch.shipments) ||
      !Array.isArray(batch.receipts) || !Number.isFinite(at)) throw Error("invalid_synthetic_batch");

  const shipments = new Map();
  for (const shipment of batch.shipments) {
    if (typeof shipment.id !== "string" || !shipment.id || shipments.has(shipment.id) ||
        typeof shipment.unit !== "string" || !shipment.unit ||
        !Number.isSafeInteger(shipment.loaded) || shipment.loaded < 1 ||
        !Number.isFinite(Date.parse(shipment.dueAt))) throw Error("invalid_or_duplicate_shipment");
    shipments.set(shipment.id, { shipment, receipts: [], issues: [] });
  }

  const unlinked = [];
  const receiptIds = new Set();
  for (const receipt of batch.receipts) {
    if (typeof receipt.id !== "string" || !receipt.id || receiptIds.has(receipt.id)) {
      throw Error("invalid_or_duplicate_receipt");
    }
    receiptIds.add(receipt.id);
    const linked = shipments.get(receipt.shipmentId);
    if (!linked) {
      unlinked.push(receipt.id);
      continue;
    }
    if (receipt.unit !== linked.shipment.unit) linked.issues.push("quantity_unit_mismatch");
    else if (Date.parse(receipt.recordedAt) > at) linked.issues.push("future_receipt");
    else linked.receipts.push(receipt);
  }

  return {
    synthetic: true,
    unlinked,
    shipments: [...shipments.values()].map(({ shipment, receipts, issues }) => {
      const result = reconcileShipment({ ...shipment, receipts });
      const status = issues.length || result.errors.length ? "needs_record_review"
        : receipts.length ? result.status
        : Date.parse(shipment.dueAt) <= at ? "receiving_record_missing" : "awaiting_receipt";
      return { ...result, status, unit: shipment.unit, errors: [...result.errors, ...issues] };
    })
  };
}
