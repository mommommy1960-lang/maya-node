/** Synthetic deterministic order workflow. No external actions, billing, or dispatch. */
const transitions={
 proposed:["reserved","canceled"],
 reserved:["approved","canceled","expired"],
 approved:["picked_up","canceled"],
 picked_up:["delivered","exception"],
 delivered:["reconciled","exception"],
 exception:["reconciled","canceled"],
 reconciled:[],canceled:[],expired:[]
};
export function createOrder({id,offerId,needId,quantity,createdAt}) {
 if (![id,offerId,needId,createdAt].every(Boolean)||!Number.isSafeInteger(quantity)||quantity<=0||!Number.isFinite(Date.parse(createdAt))) throw new Error("invalid_order");
 return {id,offerId,needId,quantity,state:"proposed",events:[{type:"proposed",at:createdAt}],synthetic:true,dispatchEnabled:false,paymentEnabled:false};
}
export function transitionOrder(order,{to,at,actor,approvalEvidence}) {
 if (!order?.synthetic || !actor || !Number.isFinite(Date.parse(at)) || !transitions[order.state]?.includes(to)) throw new Error("invalid_transition");
 if (Date.parse(at)<Date.parse(order.events.at(-1).at)) throw new Error("out_of_order_event");
 if (to==="approved" && (!approvalEvidence?.donor || !approvalEvidence?.receiver || !approvalEvidence?.transport)) throw new Error("missing_approvals");
 const event={type:to,at,actor,...(to==="approved"?{approvalEvidence:{...approvalEvidence}}:{})};
 return {...order,state:to,events:[...order.events,event]};
}
