/** Synthetic-only alert/escalation planner. No messaging or external side effects. */
export function planAlerts(opportunity, contacts, now = new Date()) {
  if (!opportunity?.id || !Number.isFinite(Date.parse(opportunity.deadline))) throw new Error("invalid_opportunity");
  const out = [];
  if (["completed","canceled"].includes(opportunity.state)) return out;
  const deadline = Date.parse(opportunity.deadline);
  if (deadline <= now.getTime()) return [{ type: "expired", opportunityId: opportunity.id, send: false }];
  if (opportunity.acknowledged === true) return out;
  const allowed = contacts.filter(c => c.consent === true && c.active === true && c.role === "authorized");
  const ordered = allowed.sort((a,b) => a.priority - b.priority);
  if (!ordered.length) return [{ type:"needs_human_configuration", opportunityId:opportunity.id, send:false }];
  const elapsed = now.getTime() - Date.parse(opportunity.createdAt);
  if (!Number.isFinite(elapsed) || elapsed < 0) return [{type:"invalid_timestamp", opportunityId:opportunity.id, send:false}];
  const level = elapsed >= 30*60_000 ? 2 : elapsed >= 10*60_000 ? 1 : 0;
  const contact = ordered[Math.min(level,ordered.length-1)];
  if (!contact) return out;
  if (opportunity.lastAlertAt && Number.isFinite(Date.parse(opportunity.lastAlertAt)) && now.getTime()-Date.parse(opportunity.lastAlertAt)<10*60_000) return out;
  out.push({type:level===0?"initial": "escalation", opportunityId:opportunity.id, contactId:contact.id, send:false, requires:"configured_delivery_adapter", reason:"unacknowledged"});
  return out;
}
