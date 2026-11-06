// Apply schema.sql as a deployment migration before using this adapter.
export class D1Store {
  constructor(db){this.db=db;}
  async status(subject,now){
    const row=await this.db.prepare('SELECT * FROM maya_accounts WHERE subject=?').bind(subject).first();
    if(!row)return {allowed:false,reason:'not_started'};
    if(row.suspended)return {allowed:false,reason:'suspended'};
    if(row.paid_end>now&&row.paid_used<100)return {allowed:true,reason:'paid',expires_at:row.paid_end,replies_remaining:100-row.paid_used};
    if(row.trial_end>now&&row.trial_used<10)return {allowed:true,reason:'trial',expires_at:row.trial_end,replies_remaining:10-row.trial_used};
    return {allowed:false,reason:'expired_or_used',expires_at:Math.max(row.trial_end,row.paid_end),replies_remaining:0};
  }
  async startTrial(subject,now,seconds){
    await this.db.prepare('INSERT INTO maya_accounts(subject,trial_end) VALUES(?,?) ON CONFLICT(subject) DO NOTHING').bind(subject,now+seconds).run();
    return this.status(subject,now);
  }
  async reserve(subject,now){
    let row=await this.db.prepare('UPDATE maya_accounts SET paid_used=paid_used+1 WHERE subject=? AND suspended=0 AND paid_end>? AND paid_used<100 RETURNING subject').bind(subject,now).first();
    if(row)return true;
    row=await this.db.prepare('UPDATE maya_accounts SET trial_used=trial_used+1 WHERE subject=? AND suspended=0 AND trial_end>? AND trial_used<10 RETURNING subject').bind(subject,now).first();
    return Boolean(row);
  }
  async recordCheckout(o){await this.db.prepare('INSERT INTO maya_checkouts VALUES(?,?,?,?)').bind(o.session,o.subject,o.price,o.created).run();}
  getCheckout(session){return this.db.prepare('SELECT * FROM maya_checkouts WHERE session=?').bind(session).first();}
  async grantOrder(o){
    if(typeof o.paymentIntent!=='string'||!o.paymentIntent.startsWith('pi_'))throw new Error('Invalid payment intent');
    await this.db.batch([
      this.db.prepare('INSERT INTO maya_accounts(subject) VALUES(?) ON CONFLICT(subject) DO NOTHING').bind(o.subject),
      this.db.prepare('INSERT INTO maya_orders(session,subject,payment_intent,expires,revoked) VALUES(?,?,?,?,EXISTS(SELECT 1 FROM maya_payment_revocations WHERE payment_intent=?)) ON CONFLICT(session) DO NOTHING').bind(o.session,o.subject,o.paymentIntent,o.expires,o.paymentIntent),
      this.db.prepare('UPDATE maya_accounts SET paid_end=MAX(paid_end,?),paid_used=0 WHERE subject=? AND EXISTS(SELECT 1 FROM maya_orders WHERE session=? AND subject=? AND applied=0 AND revoked=0)').bind(o.expires,o.subject,o.session,o.subject),
      this.db.prepare('UPDATE maya_orders SET applied=1 WHERE session=?').bind(o.session)
    ]);
  }
  async revokePayment(paymentIntent){
    await this.db.batch([
      this.db.prepare('INSERT INTO maya_payment_revocations VALUES(?) ON CONFLICT DO NOTHING').bind(paymentIntent),
      this.db.prepare('UPDATE maya_orders SET revoked=1 WHERE payment_intent=?').bind(paymentIntent),
      this.db.prepare('UPDATE maya_accounts SET paid_end=COALESCE((SELECT MAX(expires) FROM maya_orders WHERE subject=maya_accounts.subject AND revoked=0),0) WHERE subject IN (SELECT subject FROM maya_orders WHERE payment_intent=?)').bind(paymentIntent)
    ]);
  }
}
