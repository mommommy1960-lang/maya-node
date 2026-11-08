/** Public-knowledge registry, synthetic-only. No live scraping, external calls, or operational authority. */
export function assessKnowledgeSource(source, now=new Date()) {
  const reasons=[];
  if (!source?.id || !source?.title || !source?.url || !source?.publisher) reasons.push("missing_provenance");
  if (!Number.isFinite(Date.parse(source?.retrievedAt)) || Date.parse(source.retrievedAt)>now.getTime()) reasons.push("invalid_retrieval_time");
  if (!["research","regulatory","operational_guidance"].includes(source?.kind)) reasons.push("unsupported_source_kind");
  if (source?.licenseStatus!=="verified") reasons.push("license_unverified");
  return {sourceId:source?.id??null,usableForBackground:reasons.length===0,usableForLiveInventory:false,reasons};
}
export function assessOperationalObservation(record, now=new Date()) {
  const reasons=[];
  if (!record?.organizationId || !record?.resourceId || !record?.sourceId) reasons.push("missing_identity_or_provenance");
  if (record?.authorized!==true) reasons.push("authorization_missing");
  if (record?.status!=="confirmed") reasons.push("not_confirmed");
  const observed=Date.parse(record?.observedAt);
  if (!Number.isFinite(observed) || observed>now.getTime() || now.getTime()-observed>15*60_000) reasons.push("stale_or_invalid");
  if (!Number.isFinite(record?.quantity) || record.quantity<0) reasons.push("invalid_quantity");
  return {resourceId:record?.resourceId??null,usableForMatching:reasons.length===0,reasons};
}
