import { evaluateTransfer } from "./matching.mjs";
import { planAlerts } from "./alerts.mjs";
/** Synthetic proposals only. Conservatively allocate each offer, need, truck and receiving capacity once per snapshot. */
export function buildWatchtower({ offers, needs, receivers, vehicles, contacts = [], now = new Date() }) {
  const proposals=[], blocked=[], notifications=[];
  const allocatedOffers=new Set(), allocatedNeeds=new Set(), allocatedVehicles=new Set();
  const remainingStorage=new Map(receivers.map(r=>[r.pantryId,r.freeCapacity]));
  for (const offer of offers) {
    for (const need of needs) {
      if (offer.pantryId===need.pantryId) continue;
      if (allocatedOffers.has(offer.id) || allocatedNeeds.has(need.id)) continue;
      const receiver=receivers.find(r=>r.pantryId===need.pantryId);
      const vehicle=vehicles.find(v=>v.handling===offer.handling && !allocatedVehicles.has(v.id));
      const capacity=remainingStorage.get(need.pantryId);
      const adjustedReceiver=receiver && {...receiver,freeCapacity:capacity};
      const result=evaluateTransfer(offer,need,adjustedReceiver,vehicle,now);
      const record={offerId:offer.id,needId:need.id,from:offer.pantryId,to:need.pantryId,vehicleId:vehicle?.id??null,...result};
      if (result.eligible) {
        allocatedOffers.add(offer.id); allocatedNeeds.add(need.id); allocatedVehicles.add(vehicle.id);
        remainingStorage.set(need.pantryId,capacity-result.quantity);
        proposals.push(record);
        notifications.push(...planAlerts({id:offer.id+":"+need.id,state:"pending",createdAt:offer.observedAt,deadline:need.receivingUntil,acknowledged:false},contacts,now));
      } else blocked.push(record);
    }
  }
  return {asOf:now.toISOString(),synthetic:true,proposals,blocked,notifications,liveDispatchEnabled:false,paymentEnabled:false};
}
