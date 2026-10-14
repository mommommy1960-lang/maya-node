import {test} from 'node:test';
import assert from 'node:assert/strict';
import {DatabaseSync} from 'node:sqlite';
import {readFileSync} from 'node:fs';
import worker,{dispatch,payloadText} from './worker.mjs';
function database() {
 const raw=new DatabaseSync(':memory:');raw.exec(readFileSync(new URL('./schema.sql',import.meta.url),'utf8'));
 return {raw,prepare(sql){return {bind(...args){const s=raw.prepare(sql);return {async first(){return s.get(...args)||null},async run(){const r=s.run(...args);return {meta:{changes:r.changes}}},async all(){return {results:s.all(...args)}}}},async all(){return {results:raw.prepare(sql).all()}}}}};
}
const p={recipient:'test@example.invalid',subject:'test',body:'test'};
function queued(db,state='queued'){db.raw.prepare('INSERT INTO jobs(id,payload,state) VALUES (?,?,?)').run('one',payloadText(p),state);}
test('competing dispatches call sender once',async()=>{const db=database();queued(db);let calls=0;await Promise.all([dispatch(db,'one',async()=>{calls++;return {id:'receipt'}}),dispatch(db,'one',async()=>{calls++;return {id:'receipt'}})]);assert.equal(calls,1);assert.equal(db.raw.prepare('SELECT state FROM jobs').get().state,'sent');});
test('cancellation prevents sending',async()=>{const db=database();queued(db,'canceled');assert.equal(await dispatch(db,'one',()=>assert.fail()),'blocked');});
test('timeout and crash claims never reclaim',async()=>{const db=database();queued(db);await assert.rejects(dispatch(db,'one',async()=>{throw new Error('timeout')}));assert.equal(await dispatch(db,'one',()=>assert.fail()),'blocked');db.raw.exec("UPDATE jobs SET state='dispatch_committed'");assert.equal(await dispatch(db,'one',()=>assert.fail()),'blocked');});
test('immutable database payload',()=>{const db=database();queued(db);assert.throws(()=>db.raw.exec("UPDATE jobs SET payload='{}'"));});
test('unauthenticated controller rejected',async()=>{const r=await worker.fetch(new Request('https://test/status'),{});assert.equal(r.status,401);});
test('sending disabled by default',async()=>{await worker.scheduled({},{});});
test('header injection rejected',()=>{assert.throws(()=>payloadText({...p,subject:'test\r\nBcc: evil@example.invalid'}));assert.throws(()=>payloadText({...p,recipient:'a@example.invalid,b@example.invalid'}));});
