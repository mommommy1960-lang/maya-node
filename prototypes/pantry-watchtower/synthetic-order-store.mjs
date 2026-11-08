/** Isolated synthetic order + reservation transaction store. NO network, real inventory, dispatch or billing. */
const roles = Object.freeze({donor:"donor",receiver:"receiver",transport:"transport"});
const validId = x => typeof x==="string" && x.trim().length>0 && x.length<=160;
const validMs = n => Number.isSafeInteger(n) && n>=0;
function requireInput(ok,code) {if(!ok)throw Error(code);}
function normalize(items) {return [...items].sort((a,b)=>a.resourceId.localeCompare(b.resourceId));}

export class SyntheticOrderStore {
  constructor(ledger) {
    requireInput(ledger?.db, "missing_reservation_ledger");
    this.db=ledger.db;
    this.db.exec(`
      PRAGMA foreign_keys=ON;
      CREATE TABLE IF NOT EXISTS synthetic_orders(
        id TEXT PRIMARY KEY, bundle_id TEXT NOT NULL UNIQUE REFERENCES bundles(id),
        signature TEXT NOT NULL, offer_id TEXT NOT NULL, need_id TEXT NOT NULL,
        quantity INTEGER NOT NULL CHECK(quantity>0),
        donor_id TEXT NOT NULL, receiver_id TEXT NOT NULL, transport_id TEXT NOT NULL,
        expires_at INTEGER NOT NULL, created_at INTEGER NOT NULL, state TEXT NOT NULL
      );
      CREATE TABLE IF NOT EXISTS synthetic_order_approvals(
        order_id TEXT NOT NULL REFERENCES synthetic_orders(id),
        role TEXT NOT NULL, actor_id TEXT NOT NULL, evidence_ref TEXT NOT NULL,
        at_ms INTEGER NOT NULL, PRIMARY KEY(order_id,role)
      );
      CREATE TABLE IF NOT EXISTS synthetic_order_events(
        seq INTEGER PRIMARY KEY AUTOINCREMENT, order_id TEXT NOT NULL REFERENCES synthetic_orders(id),
        kind TEXT NOT NULL, actor_id TEXT NOT NULL, evidence_ref TEXT, at_ms INTEGER NOT NULL
      );
      CREATE TRIGGER IF NOT EXISTS synthetic_events_no_update
        BEFORE UPDATE ON synthetic_order_events BEGIN SELECT RAISE(ABORT,'append_only_events'); END;
      CREATE TRIGGER IF NOT EXISTS synthetic_events_no_delete
        BEFORE DELETE ON synthetic_order_events BEGIN SELECT RAISE(ABORT,'append_only_events'); END;
    `);
  }
  tx(fn) {
    this.db.exec("BEGIN IMMEDIATE");
    try {const result=fn();this.db.exec("COMMIT");return result;}
    catch(e){try{this.db.exec("ROLLBACK");}catch{}throw e;}
  }
  get(id) {
    const o=this.db.prepare("SELECT * FROM synthetic_orders WHERE id=?").get(id);
    if(!o)return null;
    return {
      id:o.id,bundleId:o.bundle_id,offerId:o.offer_id,needId:o.need_id,quantity:o.quantity,
      parties:{donor:o.donor_id,receiver:o.receiver_id,transport:o.transport_id},
      expiresAt:o.expires_at,createdAt:o.created_at,state:o.state,
      approvals:this.db.prepare("SELECT role,actor_id AS actorId,evidence_ref AS evidenceRef,at_ms AS at FROM synthetic_order_approvals WHERE order_id=? ORDER BY role").all(id),
      events:this.db.prepare("SELECT seq,kind,actor_id AS actorId,evidence_ref AS evidenceRef,at_ms AS at FROM synthetic_order_events WHERE order_id=? ORDER BY seq").all(id),
      synthetic:true,dispatchEnabled:false,paymentEnabled:false
    };
  }
  _event(id,kind,actor,at,evidence=null){
    this.db.prepare("INSERT INTO synthetic_order_events(order_id,kind,actor_id,evidence_ref,at_ms) VALUES(?,?,?,?,?)").run(id,kind,actor,evidence,at);
  }
  _time(o,at){
    requireInput(validMs(at) && at>=o.created_at,"invalid_event_time");
    const last=this.db.prepare("SELECT at_ms FROM synthetic_order_events WHERE order_id=? ORDER BY seq DESC LIMIT 1").get(o.id);
    requireInput(!last || at>=last.at_ms,"out_of_order_event");
  }
  _mappedHolds(o) {
    const b=this.db.prepare("SELECT signature,state FROM bundles WHERE id=?").get(o.bundle_id);
    requireInput(b?.state==="active","inactive_reservation");
    const expected=JSON.parse(b.signature);
    const holds=this.db.prepare("SELECT bh.resource_id,h.id,h.resource_id AS hold_resource,h.quantity,h.state,h.expires_at FROM bundle_holds bh JOIN holds h ON h.id=bh.hold_id WHERE bh.bundle_id=?").all(o.bundle_id);
    requireInput(Array.isArray(expected.items) && holds.length===expected.items.length && holds.length>0 &&
      holds.every(h=>h.state==="active" && h.resource_id===h.hold_resource &&
      expected.items.some(x=>x.resourceId===h.resource_id && x.quantity===h.quantity) &&
      h.expires_at>=o.expires_at), "corrupt_order_reservation");
    return holds;
  }
  _active(o,at){
    const holds=this._mappedHolds(o);
    requireInput(at<o.expires_at && holds.every(h=>h.expires_at>at),"reservation_expired");
    return holds;
  }
  /** New order and food/freezer/truck debits are committed together; no intermediate orphan hold. */
  createReserved({id,offerId,needId,quantity,parties,bundle,at},now=at){
    requireInput([id,offerId,needId,parties?.donor,parties?.receiver,parties?.transport,bundle?.id].every(validId) &&
      validMs(at) && validMs(now) && at<=now && Number.isSafeInteger(quantity) && quantity>0 &&
      Array.isArray(bundle?.items) && bundle.items.length>0 &&
      bundle.items.every(x=>validId(x?.resourceId) && Number.isSafeInteger(x.quantity) && x.quantity>0) &&
      new Set(bundle.items.map(x=>x.resourceId)).size===bundle.items.length &&
      validMs(bundle.expiresAt) && bundle.expiresAt>now, "invalid_order_reservation");
    const items=normalize(bundle.items);
    const sig=JSON.stringify({offerId,needId,quantity,parties,items,expiresAt:bundle.expiresAt,bundleId:bundle.id,at});
    this.tx(()=>{
      const old=this.db.prepare("SELECT signature FROM synthetic_orders WHERE id=?").get(id);
      if(old){requireInput(old.signature===sig,"order_idempotency_conflict");return;}
      requireInput(!this.db.prepare("SELECT id FROM bundles WHERE id=?").get(bundle.id),"bundle_already_used");
      for(const item of items){
        const changed=this.db.prepare("UPDATE resources SET available=available-? WHERE id=? AND available>=?").run(item.quantity,item.resourceId,item.quantity).changes;
        requireInput(changed===1,"insufficient_capacity");
      }
      this.db.prepare("INSERT INTO bundles(id,signature,state) VALUES(?,?,'active')").run(bundle.id,JSON.stringify({items,expiresAt:bundle.expiresAt}));
      for(const item of items){
        const holdId=bundle.id+":"+item.resourceId;
        this.db.prepare("INSERT INTO holds(id,resource_id,quantity,state,expires_at) VALUES(?,?,?,'active',?)").run(holdId,item.resourceId,item.quantity,bundle.expiresAt);
        this.db.prepare("INSERT INTO bundle_holds(bundle_id,resource_id,hold_id) VALUES(?,?,?)").run(bundle.id,item.resourceId,holdId);
      }
      this.db.prepare("INSERT INTO synthetic_orders(id,bundle_id,signature,offer_id,need_id,quantity,donor_id,receiver_id,transport_id,expires_at,created_at,state) VALUES(?,?,?,?,?,?,?,?,?,?,?,'reserved')")
        .run(id,bundle.id,sig,offerId,needId,quantity,parties.donor,parties.receiver,parties.transport,bundle.expiresAt,at);
      this._event(id,"proposed","synthetic-operator",at);
      this._event(id,"reserved","synthetic-operator",at);
    });
    return this.get(id);
  }
  _order(id){const o=this.db.prepare("SELECT * FROM synthetic_orders WHERE id=?").get(id);requireInput(!!o,"unknown_order");return o;}
  approve({id,role,actorId,evidenceRef,at}){
    requireInput(Object.hasOwn(roles,role) && validId(actorId) && validId(evidenceRef),"invalid_approval");
    this.tx(()=>{
      const o=this._order(id);
      this._time(o,at);
      requireInput(actorId===o[roles[role]+"_id"],"unauthorized_party");
      requireInput(["reserved","approved"].includes(o.state),"invalid_order_state");
      this._active(o,at);
      const old=this.db.prepare("SELECT actor_id,evidence_ref FROM synthetic_order_approvals WHERE order_id=? AND role=?").get(id,role);
      if(old){requireInput(old.actor_id===actorId && old.evidence_ref===evidenceRef,"approval_replay_conflict");return;}
      this.db.prepare("INSERT INTO synthetic_order_approvals(order_id,role,actor_id,evidence_ref,at_ms) VALUES(?,?,?,?,?)").run(id,role,actorId,evidenceRef,at);
      this._event(id,role+"_approved",actorId,at,evidenceRef);
      const n=this.db.prepare("SELECT COUNT(*) AS n FROM synthetic_order_approvals WHERE order_id=?").get(id).n;
      if(n===3){this.db.prepare("UPDATE synthetic_orders SET state='approved' WHERE id=?").run(id);this._event(id,"approved","synthetic-operator",at);}
    });
    return this.get(id);
  }
  pickup({id,actorId,evidenceRef,at}){
    requireInput(validId(actorId) && validId(evidenceRef),"invalid_pickup");
    this.tx(()=>{
      const o=this._order(id);this._time(o,at);
      requireInput(o.state==="approved","pickup_requires_approvals");
      requireInput(actorId===o.transport_id,"unauthorized_party");
      this._active(o,at);
      // A physically pending trip must not be reclaimed by the reservation expiry sweeper.
      this.db.prepare("UPDATE holds SET expires_at=? WHERE id IN (SELECT hold_id FROM bundle_holds WHERE bundle_id=?)").run(Number.MAX_SAFE_INTEGER,o.bundle_id);
      this.db.prepare("UPDATE synthetic_orders SET state='picked_up' WHERE id=?").run(id);
      this._event(id,"picked_up",actorId,at,evidenceRef);
    });
    return this.get(id);
  }
  /** Roll back all allocations in the SAME transaction as a pre-pickup cancellation. */
  _release(o){
    const holds=this._mappedHolds(o);
    for(const h of holds)this.db.prepare("UPDATE resources SET available=available+? WHERE id=?").run(h.quantity,h.resource_id);
    this.db.prepare("UPDATE holds SET state='released' WHERE id IN (SELECT hold_id FROM bundle_holds WHERE bundle_id=?)").run(o.bundle_id);
    this.db.prepare("UPDATE bundles SET state='released' WHERE id=?").run(o.bundle_id);
  }
  cancel({id,actorId,evidenceRef,at}){
    requireInput(validId(actorId) && validId(evidenceRef),"invalid_cancellation");
    this.tx(()=>{
      const o=this._order(id);this._time(o,at);
      requireInput(["reserved","approved"].includes(o.state),"cancellation_requires_pre_pickup");
      requireInput([o.donor_id,o.receiver_id,o.transport_id].includes(actorId),"unauthorized_party");
      this._release(o);
      this.db.prepare("UPDATE synthetic_orders SET state='canceled' WHERE id=?").run(id);
      this._event(id,"canceled",actorId,at,evidenceRef);
    });
    return this.get(id);
  }
  /** Explicit synthetic sweeper; restart safe, not a background/hosted deletion guarantee. */
  expireDue(at){
    requireInput(validMs(at),"invalid_event_time");
    const ids=this.db.prepare("SELECT id FROM synthetic_orders WHERE state IN ('reserved','approved') AND expires_at<=? ORDER BY id").all(at).map(x=>x.id);
    let count=0;
    for(const id of ids){
      this.tx(()=>{
        const o=this._order(id);
        if(!["reserved","approved"].includes(o.state) || o.expires_at>at)return;
        this._time(o,at);
        this._release(o);
        this.db.prepare("UPDATE synthetic_orders SET state='expired' WHERE id=?").run(id);
        this._event(id,"expired","synthetic-sweeper",at);
        count++;
      });
    }
    return count;
  }
}
