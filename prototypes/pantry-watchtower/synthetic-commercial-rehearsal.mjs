/**
 * Isolated, SQLite-persistent commercial REHEARSAL only.
 * Fake sponsor, fictional quote and terms, local payment-state simulator.
 * NO Stripe SDK, API keys, webhooks, network calls, charges, refund transactions or legal assent.
 */
const validTime = n => Number.isSafeInteger(n) && n >= 0;
const demand = (ok, code) => { if (!ok) throw Error(code); };
const QUOTE = Object.freeze({
  quoteId: 'SYN-QUOTE-v1', termsVersion: 'SYN-TERMS-2026-11-07-v1',
  sponsorFeeCents: 250, receiverFeeCents: 0, currency: 'USD',
  sponsorId: 'fictional-sponsor',
});
export class SyntheticCommercialRehearsal {
  constructor(orders) {
    demand(orders?.db && typeof orders.tx === 'function', 'missing_order_store');
    this.orders = orders;
    this.db = orders.db;
    this.db.exec([
      'PRAGMA foreign_keys=ON;',
      'CREATE TABLE IF NOT EXISTS synthetic_commercial (',
      'order_id TEXT PRIMARY KEY REFERENCES synthetic_orders(id),',
      'quote_id TEXT NOT NULL, terms_version TEXT NOT NULL, sponsor_id TEXT NOT NULL,',
      'fee_cents INTEGER NOT NULL CHECK(fee_cents>=0),',
      'receiver_fee_cents INTEGER NOT NULL CHECK(receiver_fee_cents=0),',
      'currency TEXT NOT NULL, state TEXT NOT NULL, created_at INTEGER NOT NULL,',
      'accepted_at INTEGER, authorized_at INTEGER, captured_at INTEGER, refunded_at INTEGER',
      ');',
      'CREATE TABLE IF NOT EXISTS synthetic_commercial_events (',
      'seq INTEGER PRIMARY KEY AUTOINCREMENT,',
      'order_id TEXT NOT NULL REFERENCES synthetic_orders(id),',
      'event_key TEXT NOT NULL, kind TEXT NOT NULL, at_ms INTEGER NOT NULL,',
      'UNIQUE(order_id,event_key)',
      ');',
      "CREATE TRIGGER IF NOT EXISTS synthetic_commercial_events_no_update BEFORE UPDATE ON synthetic_commercial_events BEGIN SELECT RAISE(ABORT,'append_only_commercial_events'); END;",
      "CREATE TRIGGER IF NOT EXISTS synthetic_commercial_events_no_delete BEFORE DELETE ON synthetic_commercial_events BEGIN SELECT RAISE(ABORT,'append_only_commercial_events'); END;",
      'CREATE TRIGGER IF NOT EXISTS synthetic_commercial_void_on_order_end AFTER UPDATE OF state ON synthetic_orders',
      "WHEN NEW.state IN ('canceled','expired') BEGIN",
      "INSERT INTO synthetic_commercial_events(order_id,event_key,kind,at_ms)",
      "SELECT NEW.id,'auto-void-' || NEW.state,'authorization_voided',",
      'COALESCE((SELECT MAX(at_ms) FROM synthetic_commercial_events WHERE order_id=NEW.id),NEW.created_at)',
      "WHERE EXISTS(SELECT 1 FROM synthetic_commercial WHERE order_id=NEW.id AND state IN ('quoted','accepted','authorized'));",
      "UPDATE synthetic_commercial SET state='voided' WHERE order_id=NEW.id AND state IN ('quoted','accepted','authorized');",
      'END;'
    ].join('\n'));
  }
  get(orderId) {
    const row=this.db.prepare('SELECT * FROM synthetic_commercial WHERE order_id=?').get(orderId);
    if (!row) return null;
    const events=this.db.prepare('SELECT seq,event_key AS eventKey,kind,at_ms AS at FROM synthetic_commercial_events WHERE order_id=? ORDER BY seq').all(orderId);
    return {
      synthetic:true, provider:'LOCAL_SIMULATOR_ONLY_NOT_STRIPE',
      orderId:row.order_id, quoteId:row.quote_id, termsVersion:row.terms_version,
      sponsorId:row.sponsor_id, sponsorFeeCents:row.fee_cents,
      receiverFeeCents:row.receiver_fee_cents, currency:row.currency, state:row.state,
      acceptedAt:row.accepted_at, authorizedAt:row.authorized_at,
      capturedAt:row.captured_at, refundedAt:row.refunded_at,
      simulatedNetCents:row.state==='captured'?row.fee_cents:0,
      events,
    };
  }
  _order(orderId) {
    const order=this.orders.get(orderId);
    demand(!!order, 'unknown_order');
    return order;
  }
  _row(orderId) {
    const row=this.db.prepare('SELECT * FROM synthetic_commercial WHERE order_id=?').get(orderId);
    demand(!!row, 'missing_fictional_quote');
    return row;
  }
  _time(orderId, at) {
    const order=this._order(orderId);
    demand(validTime(at) && at>=order.createdAt, 'invalid_commercial_time');
    const latest=this.db.prepare('SELECT MAX(at_ms) AS last FROM synthetic_commercial_events WHERE order_id=?').get(orderId).last;
    demand(latest===null || at>=latest, 'out_of_order_commercial_event');
    return order;
  }
  _event(orderId,key,kind,at) {
    this.db.prepare('INSERT INTO synthetic_commercial_events(order_id,event_key,kind,at_ms) VALUES(?,?,?,?)').run(orderId,key,kind,at);
  }
  quote({orderId,at}) {
    this.orders.tx(()=>{
      const order=this._time(orderId,at);
      demand(order.state==='approved', 'quote_requires_fictional_approvals');
      const old=this.get(orderId);
      if (old) { demand(old.quoteId===QUOTE.quoteId && old.termsVersion===QUOTE.termsVersion,'quote_conflict'); return; }
      this.db.prepare('INSERT INTO synthetic_commercial(order_id,quote_id,terms_version,sponsor_id,fee_cents,receiver_fee_cents,currency,state,created_at) VALUES(?,?,?,?,?,?,?, ?,?)').run(
        orderId,QUOTE.quoteId,QUOTE.termsVersion,QUOTE.sponsorId,QUOTE.sponsorFeeCents,0,QUOTE.currency,'quoted',at);
      this._event(orderId,'quote-v1','quote_prepared',at);
    });
    return this.get(orderId);
  }
  accept({orderId,actorId,termsVersion,at}) {
    this.orders.tx(()=>{
      const order=this._time(orderId,at), row=this._row(orderId);
      demand(order.state==='approved','agreement_requires_approved_order');
      demand(actorId===row.sponsor_id && termsVersion===row.terms_version,'fictional_agreement_mismatch');
      if (row.state==='accepted'||row.state==='authorized'||row.state==='captured'||row.state==='refunded') return;
      demand(row.state==='quoted','invalid_commercial_state');
      this.db.prepare("UPDATE synthetic_commercial SET state='accepted',accepted_at=? WHERE order_id=?").run(at,orderId);
      this._event(orderId,'agreement-v1','fictional_terms_accepted',at);
    });
    return this.get(orderId);
  }
  authorize({orderId,actorId,attemptId,mode,at}) {
    demand(typeof attemptId==='string' && /^SYN-AUTH-[a-z0-9-]{1,40}$/.test(attemptId),'invalid_mock_attempt');
    demand(mode==='approve'||mode==='decline','invalid_mock_authorization_mode');
    this.orders.tx(()=>{
      const order=this._time(orderId,at), row=this._row(orderId);
      demand(order.state==='approved','authorization_requires_approved_order');
      demand(actorId===row.sponsor_id,'unauthorized_fictional_sponsor');
      const previous=this.db.prepare('SELECT kind FROM synthetic_commercial_events WHERE order_id=? AND event_key=?').get(orderId,attemptId);
      if(previous) { demand(previous.kind===(mode==='approve'?'mock_authorized':'mock_declined'),'mock_attempt_conflict');return; }
      demand(row.state==='accepted','authorization_requires_fictional_agreement');
      if(mode==='decline') {
        this._event(orderId,attemptId,'mock_declined',at);
      } else {
        this.db.prepare("UPDATE synthetic_commercial SET state='authorized',authorized_at=? WHERE order_id=?").run(at,orderId);
        this._event(orderId,attemptId,'mock_authorized',at);
      }
    });
    return this.get(orderId);
  }
  capture({orderId,actorId,at}) {
    this.orders.tx(()=>{
      const order=this._time(orderId,at), row=this._row(orderId);
      demand(actorId===row.sponsor_id,'unauthorized_fictional_sponsor');
      demand(order.state==='reconciled','capture_requires_reconciled_delivery');
      if(row.state==='captured'||row.state==='refunded') return;
      demand(row.state==='authorized','capture_requires_mock_authorization');
      this.db.prepare("UPDATE synthetic_commercial SET state='captured',captured_at=? WHERE order_id=?").run(at,orderId);
      this._event(orderId,'mock-capture-v1','mock_captured',at);
    });
    return this.get(orderId);
  }
  refund({orderId,actorId,at}) {
    this.orders.tx(()=>{
      this._time(orderId,at);
      const row=this._row(orderId);
      demand(actorId===row.sponsor_id,'unauthorized_fictional_sponsor');
      if(row.state==='refunded') return;
      demand(row.state==='captured','refund_requires_mock_capture');
      this.db.prepare("UPDATE synthetic_commercial SET state='refunded',refunded_at=? WHERE order_id=?").run(at,orderId);
      this._event(orderId,'mock-refund-v1','mock_refunded',at);
    });
    return this.get(orderId);
  }
}
