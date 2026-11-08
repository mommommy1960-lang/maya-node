/** Local-only synthetic delivery and receipt settlement. No real inventory, authentication or dispatch. */
const validId=x=>typeof x==="string" && x.trim().length>0 && x.length<=160;
const validTime=x=>Number.isSafeInteger(x) && x>=0;
const nonnegative=x=>Number.isSafeInteger(x) && x>=0;
const requireInput=(ok,code)=>{if(!ok)throw Error(code);};

export class SyntheticDeliverySettlement {
  constructor(orderStore) {
    requireInput(orderStore?.db && typeof orderStore.tx==="function", "missing_order_store");
    this.store=orderStore;
    this.db=orderStore.db;
    this.db.exec(`
      PRAGMA foreign_keys=ON;
      CREATE TABLE IF NOT EXISTS synthetic_delivery_receipts(
        id TEXT PRIMARY KEY,
        order_id TEXT NOT NULL UNIQUE REFERENCES synthetic_orders(id),
        signature TEXT NOT NULL,
        food_resource_id TEXT NOT NULL,
        actor_id TEXT NOT NULL,
        evidence_ref TEXT NOT NULL,
        received INTEGER NOT NULL CHECK(received>=0),
        rejected INTEGER NOT NULL CHECK(rejected>=0),
        damaged INTEGER NOT NULL CHECK(damaged>=0),
        missing INTEGER NOT NULL CHECK(missing>=0),
        at_ms INTEGER NOT NULL
      );
      CREATE TABLE IF NOT EXISTS synthetic_receipt_dispositions(
        order_id TEXT PRIMARY KEY REFERENCES synthetic_orders(id),
        actor_id TEXT NOT NULL, evidence_ref TEXT NOT NULL,
        resolution_code TEXT NOT NULL, explanation TEXT NOT NULL,
        at_ms INTEGER NOT NULL
      );
      CREATE TRIGGER IF NOT EXISTS synthetic_receipts_no_update
        BEFORE UPDATE ON synthetic_delivery_receipts BEGIN SELECT RAISE(ABORT,'append_only_receipts'); END;
      CREATE TRIGGER IF NOT EXISTS synthetic_receipts_no_delete
        BEFORE DELETE ON synthetic_delivery_receipts BEGIN SELECT RAISE(ABORT,'append_only_receipts'); END;
      CREATE TRIGGER IF NOT EXISTS synthetic_dispositions_no_update
        BEFORE UPDATE ON synthetic_receipt_dispositions BEGIN SELECT RAISE(ABORT,'append_only_dispositions'); END;
      CREATE TRIGGER IF NOT EXISTS synthetic_dispositions_no_delete
        BEFORE DELETE ON synthetic_receipt_dispositions BEGIN SELECT RAISE(ABORT,'append_only_dispositions'); END;
    `);
  }
  getReceipt(orderId) {
    const r=this.db.prepare("SELECT * FROM synthetic_delivery_receipts WHERE order_id=?").get(orderId);
    if(!r)return null;
    const d=this.db.prepare("SELECT * FROM synthetic_receipt_dispositions WHERE order_id=?").get(orderId);
    return {
      id:r.id,orderId:r.order_id,foodResourceId:r.food_resource_id,
      actorId:r.actor_id,evidenceRef:r.evidence_ref,received:r.received,rejected:r.rejected,
      damaged:r.damaged,missing:r.missing,at:r.at_ms,
      discrepancy:r.rejected+r.damaged+r.missing>0,
      disposition:d?{actorId:d.actor_id,evidenceRef:d.evidence_ref,code:d.resolution_code,explanation:d.explanation,at:d.at_ms}:null,
      synthetic:true,verifiedSignature:false
    };
  }
  /** Receiver's fictional receipt consumes the reserved food but restores only reusable truck/storage slots. */
  recordReceipt({id,receiptId,actorId,evidenceRef,foodResourceId,received,rejected,damaged,at}) {
    requireInput([id,receiptId,actorId,evidenceRef,foodResourceId].every(validId) &&
      validTime(at) && [received,rejected,damaged].every(nonnegative),
      "invalid_delivery_receipt");
    const total=received+rejected+damaged;
    requireInput(Number.isSafeInteger(total),"invalid_delivery_quantity");
    const sig=JSON.stringify({id,receiptId,actorId,evidenceRef,foodResourceId,received,rejected,damaged,at});
    this.store.tx(()=>{
      const o=this.store._order(id);
      const old=this.db.prepare("SELECT signature FROM synthetic_delivery_receipts WHERE order_id=?").get(id);
      if(old){requireInput(old.signature===sig,"receipt_replay_conflict");return;}
      this.store._time(o,at);
      requireInput(o.state==="picked_up","delivery_requires_pickup");
      requireInput(actorId===o.receiver_id,"unauthorized_receiver");
      requireInput(total<=o.quantity,"receipt_quantity_exceeds_order");
      const holds=this.store._mappedHolds(o);
      const food=holds.find(h=>h.resource_id===foodResourceId);
      requireInput(food && food.quantity===o.quantity,"invalid_food_allocation");
      const missing=o.quantity-total;
      this.db.prepare(`INSERT INTO synthetic_delivery_receipts
        (id,order_id,signature,food_resource_id,actor_id,evidence_ref,received,rejected,damaged,missing,at_ms)
        VALUES(?,?,?,?,?,?,?,?,?,?,?)`).run(receiptId,id,sig,foodResourceId,actorId,evidenceRef,received,rejected,damaged,missing,at);
      for(const h of holds) {
        if(h.id===food.id){
          // Once picked up, even damaged/missing food is not automatically made available again.
          this.db.prepare("UPDATE holds SET state='consumed' WHERE id=? AND state='active'").run(h.id);
        } else {
          this.db.prepare("UPDATE resources SET available=available+? WHERE id=?").run(h.quantity,h.resource_id);
          this.db.prepare("UPDATE holds SET state='released' WHERE id=? AND state='active'").run(h.id);
        }
      }
      this.db.prepare("UPDATE bundles SET state='settled' WHERE id=?").run(o.bundle_id);
      this.store._event(id,"delivered",actorId,at,evidenceRef);
      const nextState=missing+rejected+damaged===0?"reconciled":"exception";
      this.db.prepare("UPDATE synthetic_orders SET state=? WHERE id=?").run(nextState,id);
      this.store._event(id,nextState,actorId,at,evidenceRef);
    });
    return {order:this.store.get(id),receipt:this.getReceipt(id)};
  }
  /** A recorded exception can be acknowledged without pretending missing/unsafe food was returned. */
  recordDisposition({id,actorId,evidenceRef,resolutionCode,explanation,at}) {
    requireInput([id,actorId,evidenceRef,explanation].every(validId) &&
      validTime(at) && ["shortage_recorded","damage_recorded","rejection_recorded","exception_documented"].includes(resolutionCode),
      "invalid_disposition");
    this.store.tx(()=>{
      const o=this.store._order(id);
      this.store._time(o,at);
      requireInput(o.state==="exception","disposition_requires_exception");
      requireInput(actorId===o.receiver_id,"unauthorized_receiver");
      requireInput(!!this.db.prepare("SELECT id FROM synthetic_delivery_receipts WHERE order_id=?").get(id),
        "missing_delivery_receipt");
      this.db.prepare(`INSERT INTO synthetic_receipt_dispositions
        (order_id,actor_id,evidence_ref,resolution_code,explanation,at_ms)
        VALUES(?,?,?,?,?,?)`).run(id,actorId,evidenceRef,resolutionCode,explanation,at);
      this.db.prepare("UPDATE synthetic_orders SET state='reconciled' WHERE id=?").run(id);
      this.store._event(id,"exception_documented",actorId,at,evidenceRef);
    });
    return {order:this.store.get(id),receipt:this.getReceipt(id)};
  }
}
