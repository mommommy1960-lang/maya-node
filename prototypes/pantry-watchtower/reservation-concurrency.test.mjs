import test from "node:test";
import assert from "node:assert/strict";
import {mkdtempSync,rmSync} from "node:fs";
import {tmpdir} from "node:os";
import {join} from "node:path";
import {spawn} from "node:child_process";
import {ReservationLedger} from "./reservation-ledger.mjs";
const worker=new URL("./reservation-worker.mjs",import.meta.url);
function runWorker(file,id){return new Promise((resolve,reject)=>{const p=spawn(process.execPath,[worker.pathname,file,id],{stdio:["ignore","pipe","pipe"]});let out="",err="";p.stdout.on("data",x=>out+=x);p.stderr.on("data",x=>err+=x);p.on("error",reject);p.on("close",code=>code===0?resolve(out.trim()):reject(Error(err||"worker_exit_"+code)));});}
test("separate processes cannot reserve the same truck and food twice",async()=>{
 const dir=mkdtempSync(join(tmpdir(),"maya-race-")),file=join(dir,"shared.sqlite");
 try{
  const l=new ReservationLedger(file);l.seedResource("food",5);l.seedResource("freezer",5);l.seedResource("truck",1);l.close();
  const results=await Promise.all(Array.from({length:6},(_,i)=>runWorker(file,"claim-"+i)));
  assert.equal(results.filter(x=>x==="true").length,1);
  const check=new ReservationLedger(file);assert.equal(check.available("food"),0);assert.equal(check.available("freezer"),0);assert.equal(check.available("truck"),0);check.close();
 }finally{rmSync(dir,{recursive:true,force:true});}
});
