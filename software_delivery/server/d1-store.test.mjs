import test from 'node:test';import assert from 'node:assert/strict';
import {DatabaseSync} from 'node:sqlite';import {readFileSync} from 'node:fs';
import {D1Store} from './d1-store.mjs';
function setup(){
 const sqlite=new DatabaseSync(':memory:');sqlite.exec(readFileSync(new URL('./schema.sql',import.meta.url),'utf8'));
 const db={prepare(sql){let values=[];return {bind(...args){values=args;return this;},async first(){return sqlite.prepare(sql).get(...values)||null;},async run(){return sqlite.prepare(sql).run(...values);}};},async batch(statements){sqlite.exec('BEGIN IMMEDIATE');try{const out=[];for(const s of statements)out.push(await s.run());sqlite.exec('COMMIT');return out;}catch(e){sqlite.exec('ROLLBACK');throw e;}}};
 return {store:new D1Store(db),sqlite};
}
test('D1 SQL persists one exact hour across repeated starts',async()=>{const {store}=setup();await store.startTrial('a',100,3600);assert.equal((await store.startTrial('a',4000,3600)).allowed,false);assert.equal((await store.status('a',3699)).allowed,true);assert.equal((await store.status('a',3700)).allowed,false);});
test('D1 SQL consumes only ten trial reservations',async()=>{const {store}=setup();await store.startTrial('a',100,3600);const out=await Promise.all(Array.from({length:30},()=>store.reserve('a',200)));assert.equal(out.filter(Boolean).length,10);assert.equal((await store.status('a',200)).allowed,false);});
test('D1 SQL duplicate order does not restore used quota',async()=>{const {store}=setup();const o={session:'cs_1',subject:'a',paymentIntent:'pi_1',expires:5000};await store.grantOrder(o);await store.reserve('a',200);await store.grantOrder(o);assert.equal((await store.status('a',200)).replies_remaining,99);});
test('D1 SQL refunds and late payments remain denied',async()=>{const {store}=setup();await store.revokePayment('pi_1');await store.grantOrder({session:'cs_1',subject:'a',paymentIntent:'pi_1',expires:5000});assert.equal((await store.status('a',200)).allowed,false);});
test('D1 SQL refund after grant removes paid access',async()=>{const {store}=setup();await store.grantOrder({session:'cs_1',subject:'a',paymentIntent:'pi_1',expires:5000});await store.revokePayment('pi_1');assert.equal((await store.status('a',200)).allowed,false);});
test('D1 SQL subjects cannot share quota',async()=>{const {store}=setup();await store.grantOrder({session:'cs_1',subject:'a',paymentIntent:'pi_1',expires:5000});assert.equal(await store.reserve('b',200),false);});
test('D1 SQL suspension overrides both types',async()=>{const {store,sqlite}=setup();await store.startTrial('a',100,3600);await store.grantOrder({session:'cs_1',subject:'a',paymentIntent:'pi_1',expires:5000});sqlite.prepare('UPDATE maya_accounts SET suspended=1 WHERE subject=?').run('a');assert.equal(await store.reserve('a',200),false);});
test('D1 SQL paid quota capped at 100',async()=>{const {store}=setup();await store.grantOrder({session:'cs_1',subject:'a',paymentIntent:'pi_1',expires:5000});for(let i=0;i<100;i++)assert.equal(await store.reserve('a',200),true);assert.equal(await store.reserve('a',200),false);});
