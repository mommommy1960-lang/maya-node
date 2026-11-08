/** Local-only test fixture for Chromium -> tenant-guarded HTTP -> SQLite.
 * Headers simulate fictional principals and are NOT real authentication.
 * The sponsor mock is controlled on stdin, never via an HTTP bypass route.
 */
import { createInterface } from 'node:readline';
import { createLocalDemo } from './synthetic-local-demo-server.mjs';

const fixtures = {
  donor: {authenticated:true, tenantId:'SYN-TEAM-A', role:'donor', actorId:'fictional-donor'},
  receiver: {authenticated:true, tenantId:'SYN-TEAM-A', role:'receiver', actorId:'fictional-receiver'},
  transport: {authenticated:true, tenantId:'SYN-TEAM-A', role:'transport', actorId:'fictional-transporter'},
  'wrong-tenant': {authenticated:true, tenantId:'SYN-TEAM-B', role:'receiver', actorId:'fictional-receiver'},
  'wrong-actor': {authenticated:true, tenantId:'SYN-TEAM-A', role:'receiver', actorId:'fictional-impostor'},
};
const app = createLocalDemo({
  tenantGuardedOnly: true,
  clock: () => 1000,
  resolveServerPrincipal: req => fixtures[req.headers['x-syn-session']] || null
});
app.act({action:'start'});
app.tenantGate.provisionForSyntheticTest('SYN-DEMO-ORDER','SYN-TEAM-A',1000);
const url = await app.listen(0);
console.log('TEST_GUARDED_URL ' + url);
const lines = createInterface({input:process.stdin});
lines.on('line', line => {
  if (line !== 'AUTHORIZE_FAKE_SPONSOR') return;
  try {
    // The ONLY payment state is an in-process fake, not Stripe TEST.
    for (const action of ['quote','accept-terms','mock-authorize'])
      app.act({action});
    console.log('TEST_FIXTURE_AUTHORIZED');
  } catch (error) {
    console.log('TEST_FIXTURE_ERROR ' + error.message);
  }
});
async function exit() { lines.close(); await app.close(); process.exit(0); }
process.on('SIGTERM', () => exit().catch(e => {console.error(e);process.exit(1);}));
