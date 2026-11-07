/** Synthetic chain-of-custody reconciliation; invalid records never suppress later valid ones. */
export function reconcileShipment(shipment) {
  if (!shipment?.id || !Number.isSafeInteger(shipment.loaded) || shipment.loaded<0 || !Array.isArray(shipment.receipts)) throw new Error("invalid_shipment");
  const seen=new Set(), errors=[];
  let received=0,rejected=0,damaged=0;
  for (const r of shipment.receipts) {
    if (!r?.id || seen.has(r.id)) { errors.push("duplicate_or_missing_receipt_id"); continue; }
    seen.add(r.id);
    if (!r.confirmedBy || !Number.isFinite(Date.parse(r.recordedAt))) {errors.push("unverified_receipt");continue;}
    if (["received","rejected","damaged"].some(k=>!Number.isSafeInteger(r[k]??0)||(r[k]??0)<0)) {errors.push("invalid_receipt_quantity");continue;}
    received+=r.received??0;rejected+=r.rejected??0;damaged+=r.damaged??0;
  }
  const difference=shipment.loaded-(received+rejected+damaged);
  return {shipmentId:shipment.id,loaded:shipment.loaded,received,rejected,damaged,difference,
    status:errors.length?"needs_record_review":difference===0?"reconciled":"discrepancy_requires_review",
    errors,automatedAccusation:false,synthetic:true};
}
