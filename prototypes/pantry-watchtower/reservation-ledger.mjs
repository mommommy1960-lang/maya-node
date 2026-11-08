/** Synthetic-only durable reservation ledger. Node 22+ built-in SQLite; never connect to production. */
import { DatabaseSync } from "node:sqlite";
export class ReservationLedger {
  constructor(filename=":memory:") {
    this.db=new DatabaseSync(filename);
    this.db.exec(`PRAGMA foreign_keys=ON; PRAGMA busy_timeout=5000;
      CREATE TABLE IF NOT EXISTS resources (id TEXT PRIMARY KEY, available INTEGER NOT NULL CHECK(available>=0));
      CREATE TABLE IF NOT EXISTS holds (id TEXT PRIMARY KEY, resource_id TEXT NOT NULL, quantity INTEGER NOT NULL CHECK(quantity>0), state TEXT NOT NULL, expires_at INTEGER NOT NULL, FOREIGN KEY(resource_id) REFERENCES resources(id));
      CREATE TABLE IF NOT EXISTS bundles (id TEXT PRIMARY KEY, signature TEXT NOT NULL, state TEXT NOT NULL);
      CREATE TABLE IF NOT EXISTS bundle_holds (bundle_id TEXT NOT NULL, resource_id TEXT NOT NULL, hold_id TEXT PRIMARY KEY, UNIQUE(bundle_id,resource_id), FOREIGN KEY(bundle_id) REFERENCES bundles(id), FOREIGN KEY(hold_id) REFERENCES holds(id));`);
    if(filename!==":memory:")this.db.exec("PRAGMA journal_mode=WAL;");
  }
  seedResource(id,available) {
    if (!id || !Number.isSafeInteger(available) || available<0) throw Error("invalid_resource");
    this.db.prepare("INSERT INTO resources(id,available) VALUES(?,?) ON CONFLICT(id) DO NOTHING").run(id,available);
  }
  reserve({id,resourceId,quantity,expiresAt},now=Date.now()) {
    if (!id||!resourceId||!Number.isSafeInteger(quantity)||quantity<=0||!Number.isSafeInteger(now)||now<0||!Number.isSafeInteger(expiresAt)||expiresAt<=now) throw Error("invalid_hold");
    this.db.exec("BEGIN IMMEDIATE");
    try {
      const prior=this.db.prepare("SELECT resource_id,quantity,expires_at,state FROM holds WHERE id=?").get(id);
      if(prior) {
        if(prior.resource_id!==resourceId||prior.quantity!==quantity||prior.expires_at!==expiresAt) throw Error("idempotency_conflict");
        this.db.exec("COMMIT");return prior.state==="active" && prior.expires_at>now;
      }
      const result=this.db.prepare("UPDATE resources SET available=available-? WHERE id=? AND available>=?").run(quantity,resourceId,quantity);
      if(result.changes!==1){this.db.exec("ROLLBACK");return false;}
      this.db.prepare("INSERT INTO holds(id,resource_id,quantity,state,expires_at) VALUES(?,?,?,'active',?)").run(id,resourceId,quantity,expiresAt);
      this.db.exec("COMMIT");return true;
    }catch(e){if(this.db.isOpen)try{this.db.exec("ROLLBACK")}catch{};throw e;}
  }
  release(id) {
    this.db.exec("BEGIN IMMEDIATE");
    try {
      const hold=this.db.prepare("SELECT * FROM holds WHERE id=?").get(id);
      if(!hold||hold.state!=="active"){this.db.exec("COMMIT");return false;}
      // A bundled hold must be released as a unit: no half-freed truck/food/storage.
      if(this.db.prepare("SELECT 1 FROM bundle_holds WHERE hold_id=?").get(id) ||
         this.db.prepare("SELECT 1 FROM bundles WHERE state='active' AND ?=id||':'||?").get(id,hold.resource_id))
        throw Error("bundle_hold_requires_group_release");
      this.db.prepare("UPDATE holds SET state='released' WHERE id=?").run(id);
      this.db.prepare("UPDATE resources SET available=available+? WHERE id=?").run(hold.quantity,hold.resource_id);
      this.db.exec("COMMIT");return true;
    }catch(e){try{this.db.exec("ROLLBACK")}catch{};throw e;}
  }
  expire(now=Date.now()){
    const ids=this.db.prepare("SELECT h.id FROM holds h LEFT JOIN bundle_holds bh ON bh.hold_id=h.id WHERE h.state='active' AND h.expires_at<=? AND bh.hold_id IS NULL AND NOT EXISTS(SELECT 1 FROM bundles b WHERE b.state='active' AND h.id=b.id||':'||h.resource_id)").all(now).map(x=>x.id);
    for(const id of ids)this.release(id);
    return ids.length;
  }
  /** All-or-nothing reservation of food, storage and transport under one SQLite write transaction. */
  reserveBundle({id,items,expiresAt},now=Date.now()) {
    if (!id || !Array.isArray(items) || items.length===0 || !Number.isSafeInteger(now) || now<0 || !Number.isSafeInteger(expiresAt) || expiresAt<=now ||
      items.some(x=>!x?.resourceId || !Number.isSafeInteger(x.quantity) || x.quantity<=0) ||
      new Set(items.map(x=>x.resourceId)).size!==items.length) throw Error("invalid_bundle");
    const normalized=[...items].sort((a,b)=>a.resourceId.localeCompare(b.resourceId));
    const signature=JSON.stringify({items:normalized,expiresAt});
    // Eagerly reclaim expired bundle capacity before a competing claim. A released
    // idempotency key is never resurrected, even with the same payload.
    this.expireBundles(now);
    this.db.exec("BEGIN IMMEDIATE");
    try {
      const existing=this.db.prepare("SELECT signature,state FROM bundles WHERE id=?").get(id);
      if(existing){
        if(existing.signature!==signature) throw Error("idempotency_conflict");
        if(existing.state!=="active"){this.db.exec("COMMIT");return false;}
        const mapped=this.db.prepare("SELECT bh.resource_id AS mapped_id,h.resource_id AS held_id,h.quantity,h.state,h.expires_at FROM bundle_holds bh JOIN holds h ON h.id=bh.hold_id WHERE bh.bundle_id=?").all(id);
        if(!mapped.length) throw Error("legacy_bundle_requires_migration");
        // A same-key retry cannot confirm corrupted or expired durable capacity.
        if(mapped.length!==normalized.length || normalized.some(item=>!mapped.some(h=>
          h.mapped_id===item.resourceId && h.held_id===item.resourceId &&
          h.quantity===item.quantity && h.state==="active" && h.expires_at>=expiresAt)))
          throw Error("corrupt_bundle_ownership");
        // A picked-up/canceled/expired order still owns history, never fresh capacity.
        const owner=this._orderOwnsBundle(id)?
          this.db.prepare("SELECT state,expires_at FROM synthetic_orders WHERE bundle_id=?").get(id):null;
        const active=now<expiresAt && (!owner ||
          (["reserved","approved"].includes(owner.state) && now<owner.expires_at));
        this.db.exec("COMMIT");return active;
      }
      for(const item of normalized) {
        const result=this.db.prepare("UPDATE resources SET available=available-? WHERE id=? AND available>=?").run(item.quantity,item.resourceId,item.quantity);
        if(result.changes!==1){this.db.exec("ROLLBACK");return false;}
      }
      this.db.prepare("INSERT INTO bundles(id,signature,state) VALUES(?,?,'active')").run(id,signature);
      for(const item of normalized) {
        const holdId=id+":"+item.resourceId;
        this.db.prepare("INSERT INTO holds(id,resource_id,quantity,state,expires_at) VALUES(?,?,?,'active',?)").run(holdId,item.resourceId,item.quantity,expiresAt);
        this.db.prepare("INSERT INTO bundle_holds(bundle_id,resource_id,hold_id) VALUES(?,?,?)").run(id,item.resourceId,holdId);
      }
      this.db.exec("COMMIT");return true;
    }catch(e){try{this.db.exec("ROLLBACK")}catch{};throw e;}
  }
  /** Order-owned bundles must be settled/expired through the order transaction, never a generic release. */
  _orderOwnsBundle(id) {
    const exists=this.db.prepare("SELECT 1 FROM sqlite_master WHERE type='table' AND name='synthetic_orders'").get();
    return !!exists && !!this.db.prepare("SELECT 1 FROM synthetic_orders WHERE bundle_id=?").get(id);
  }
  releaseBundle(id) {
    this.db.exec("BEGIN IMMEDIATE");
    try {
      const bundle=this.db.prepare("SELECT state FROM bundles WHERE id=?").get(id);
      if(!bundle || bundle.state!=="active"){this.db.exec("COMMIT");return false;}
      if(this._orderOwnsBundle(id)) throw Error("order_bundle_requires_order_lifecycle");
      const holds=this.db.prepare("SELECT h.resource_id,h.quantity FROM bundle_holds bh JOIN holds h ON h.id=bh.hold_id WHERE bh.bundle_id=? AND h.state='active'").all(id);
      for(const h of holds)this.db.prepare("UPDATE resources SET available=available+? WHERE id=?").run(h.quantity,h.resource_id);
      const mapped=this.db.prepare("SELECT COUNT(*) n FROM bundle_holds WHERE bundle_id=?").get(id).n;
      if(!holds.length || holds.length!==mapped) throw Error("corrupt_bundle_ownership");
      this.db.prepare("UPDATE holds SET state='released' WHERE id IN (SELECT hold_id FROM bundle_holds WHERE bundle_id=?) AND state='active'").run(id);
      this.db.prepare("UPDATE bundles SET state='released' WHERE id=?").run(id);
      this.db.exec("COMMIT");return true;
    }catch(e){try{this.db.exec("ROLLBACK")}catch{};throw e;}
  }
  /** Expire active bundles as a group, avoiding partially released allocations. */
  expireBundles(now=Date.now()) {
    const ids=this.db.prepare("SELECT DISTINCT b.id FROM bundles b JOIN bundle_holds bh ON bh.bundle_id=b.id JOIN holds h ON h.id=bh.hold_id WHERE b.state='active' AND h.state='active' AND h.expires_at<=?").all(now).map(r=>r.id);
    let released=0;
    // Owned orders require a matching, audited order-state transition and are not
    // safe to reclaim using the generic bundle expiry worker.
    for(const id of ids){if(!this._orderOwnsBundle(id) && this.releaseBundle(id))released++;}
    return released;
  }
  /** Read-only gate for approval: do not approve a bundle on expired capacity. */
  isBundleActive(id,now=Date.now()){
    const bundle=this.db.prepare("SELECT state FROM bundles WHERE id=?").get(id);
    if(bundle?.state!=="active")return false;
    const counts=this.db.prepare("SELECT COUNT(*) total, SUM(CASE WHEN h.state='active' AND h.expires_at>? THEN 1 ELSE 0 END) valid FROM bundle_holds bh JOIN holds h ON h.id=bh.hold_id WHERE bh.bundle_id=?").get(now,id);
    return counts.total>0 && counts.total===counts.valid;
  }
  available(id){return this.db.prepare("SELECT available FROM resources WHERE id=?").get(id)?.available??null;}
  close(){this.db.close();}
}
