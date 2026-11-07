/** Synthetic-only durable reservation ledger. Node 22+ built-in SQLite; never connect to production. */
import { DatabaseSync } from "node:sqlite";
export class ReservationLedger {
  constructor(filename=":memory:") {
    this.db=new DatabaseSync(filename);
    this.db.exec(`PRAGMA busy_timeout=5000; CREATE TABLE IF NOT EXISTS resources (id TEXT PRIMARY KEY, available INTEGER NOT NULL CHECK(available>=0)); CREATE TABLE IF NOT EXISTS holds (id TEXT PRIMARY KEY, resource_id TEXT NOT NULL, quantity INTEGER NOT NULL CHECK(quantity>0), state TEXT NOT NULL, expires_at INTEGER NOT NULL, FOREIGN KEY(resource_id) REFERENCES resources(id));`);
  }
  seedResource(id,available) {
    if (!id || !Number.isSafeInteger(available) || available<0) throw Error("invalid_resource");
    this.db.prepare("INSERT INTO resources(id,available) VALUES(?,?) ON CONFLICT(id) DO NOTHING").run(id,available);
  }
  reserve({id,resourceId,quantity,expiresAt},now=Date.now()) {
    if (!id||!resourceId||!Number.isSafeInteger(quantity)||quantity<=0||!Number.isFinite(expiresAt)||expiresAt<=now) throw Error("invalid_hold");
    this.db.exec("BEGIN IMMEDIATE");
    try {
      const prior=this.db.prepare("SELECT resource_id,quantity,expires_at,state FROM holds WHERE id=?").get(id);
      if(prior) {
        if(prior.resource_id!==resourceId||prior.quantity!==quantity||prior.expires_at!==expiresAt) throw Error("idempotency_conflict");
        this.db.exec("COMMIT");return prior.state==="active";
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
      this.db.prepare("UPDATE holds SET state='released' WHERE id=?").run(id);
      this.db.prepare("UPDATE resources SET available=available+? WHERE id=?").run(hold.quantity,hold.resource_id);
      this.db.exec("COMMIT");return true;
    }catch(e){try{this.db.exec("ROLLBACK")}catch{};throw e;}
  }
  expire(now=Date.now()){
    const ids=this.db.prepare("SELECT id FROM holds WHERE state='active' AND expires_at<=?").all(now).map(x=>x.id);
    for(const id of ids)this.release(id);
    return ids.length;
  }
  /** All-or-nothing reservation of food, storage and transport under one SQLite write transaction. */
  reserveBundle({id,items,expiresAt},now=Date.now()) {
    if (!id || !Array.isArray(items) || items.length===0 || !Number.isFinite(expiresAt) || expiresAt<=now ||
      items.some(x=>!x?.resourceId || !Number.isSafeInteger(x.quantity) || x.quantity<=0) ||
      new Set(items.map(x=>x.resourceId)).size!==items.length) throw Error("invalid_bundle");
    const normalized=[...items].sort((a,b)=>a.resourceId.localeCompare(b.resourceId));
    const signature=JSON.stringify({items:normalized,expiresAt});
    this.db.exec("BEGIN IMMEDIATE");
    try {
      this.db.exec("CREATE TABLE IF NOT EXISTS bundles (id TEXT PRIMARY KEY, signature TEXT NOT NULL, state TEXT NOT NULL)");
      const existing=this.db.prepare("SELECT signature,state FROM bundles WHERE id=?").get(id);
      if(existing){
        if(existing.signature!==signature) throw Error("idempotency_conflict");
        this.db.exec("COMMIT");return existing.state==="active";
      }
      for(const item of normalized) {
        const result=this.db.prepare("UPDATE resources SET available=available-? WHERE id=? AND available>=?").run(item.quantity,item.resourceId,item.quantity);
        if(result.changes!==1){this.db.exec("ROLLBACK");return false;}
      }
      this.db.prepare("INSERT INTO bundles(id,signature,state) VALUES(?,?,'active')").run(id,signature);
      for(const item of normalized) this.db.prepare("INSERT INTO holds(id,resource_id,quantity,state,expires_at) VALUES(?,?,?,'active',?)").run(id+":"+item.resourceId,item.resourceId,item.quantity,expiresAt);
      this.db.exec("COMMIT");return true;
    }catch(e){try{this.db.exec("ROLLBACK")}catch{};throw e;}
  }
  releaseBundle(id) {
    this.db.exec("BEGIN IMMEDIATE");
    try {
      const bundle=this.db.prepare("SELECT state FROM bundles WHERE id=?").get(id);
      if(!bundle || bundle.state!=="active"){this.db.exec("COMMIT");return false;}
      const holds=this.db.prepare("SELECT resource_id,quantity FROM holds WHERE substr(id,1,?)=? AND state='active'").all(id.length+1,id+":");
      for(const h of holds)this.db.prepare("UPDATE resources SET available=available+? WHERE id=?").run(h.quantity,h.resource_id);
      this.db.prepare("UPDATE holds SET state='released' WHERE substr(id,1,?)=? AND state='active'").run(id.length+1,id+":");
      this.db.prepare("UPDATE bundles SET state='released' WHERE id=?").run(id);
      this.db.exec("COMMIT");return true;
    }catch(e){try{this.db.exec("ROLLBACK")}catch{};throw e;}
  }
  /** Expire active bundles as a group, avoiding partially released allocations. */
  expireBundles(now=Date.now()) {
    const ids=this.db.prepare("SELECT DISTINCT b.id FROM bundles b JOIN holds h ON substr(h.id,1,length(b.id)+1)=b.id||':' WHERE b.state='active' AND h.state='active' AND h.expires_at<=?").all(now).map(r=>r.id);
    for(const id of ids)this.releaseBundle(id);
    return ids.length;
  }
  available(id){return this.db.prepare("SELECT available FROM resources WHERE id=?").get(id)?.available??null;}
  close(){this.db.close();}
}
