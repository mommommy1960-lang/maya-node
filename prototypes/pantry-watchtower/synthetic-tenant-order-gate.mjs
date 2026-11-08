/**
 * Synthetic-only tenant/role authorization boundary for Maya's local order store.
 *
 * SECURITY LIMIT: this module does NOT authenticate anyone. Its resolver MUST be
 * injected by a separate trusted, server-side session verifier. Never resolve a
 * principal from request JSON, a query parameter, or a browser-supplied role.
 * Not installed on the current loopback demo or any hosted customer website.
 * No customer, partner, dispatch, or payment authorization is granted.
 */
const valid = x => typeof x === 'string' && x.trim().length > 0 && x.length <= 160;
const roles = new Set(['donor', 'receiver', 'transport', 'operator']);
const fail = code => { throw Error(code); };

export class SyntheticTenantOrderGate {
  constructor(store, resolveServerPrincipal) {
    if (!store?.db || typeof store.tx !== 'function' || typeof resolveServerPrincipal !== 'function')
      fail('missing_trusted_authorization_boundary');
    this.store = store;
    this.db = store.db;
    this.resolveServerPrincipal = resolveServerPrincipal;
    this.db.exec(`PRAGMA foreign_keys=ON;
      CREATE TABLE IF NOT EXISTS synthetic_order_tenants (
        order_id TEXT PRIMARY KEY REFERENCES synthetic_orders(id),
        tenant_id TEXT NOT NULL,
        bound_at_ms INTEGER NOT NULL CHECK(bound_at_ms>=0)
      );
      CREATE TRIGGER IF NOT EXISTS synthetic_order_tenants_no_update
        BEFORE UPDATE ON synthetic_order_tenants BEGIN SELECT RAISE(ABORT,'immutable_tenant_binding'); END;
      CREATE TRIGGER IF NOT EXISTS synthetic_order_tenants_no_delete
        BEFORE DELETE ON synthetic_order_tenants BEGIN SELECT RAISE(ABORT,'immutable_tenant_binding'); END;`);
  }

  /** Trusted local provisioning ONLY; cannot be called from a request route. */
  provisionForSyntheticTest(orderId, tenantId, boundAt) {
    if (!valid(orderId) || !valid(tenantId) || !Number.isSafeInteger(boundAt) || boundAt < 0)
      fail('invalid_tenant_binding');
    this.store.tx(() => {
      if (!this.store.get(orderId)) fail('unknown_order');
      const previous = this.db.prepare('SELECT tenant_id FROM synthetic_order_tenants WHERE order_id=?').get(orderId);
      if (previous) {
        if (previous.tenant_id !== tenantId) fail('tenant_binding_conflict');
        return;
      }
      this.db.prepare('INSERT INTO synthetic_order_tenants(order_id,tenant_id,bound_at_ms) VALUES(?,?,?)')
        .run(orderId, tenantId, boundAt);
    });
  }

  _authorize(orderId, allowedRoles) {
    // Call an externally authenticated resolver. This function never trusts
    // caller-supplied actor IDs, role fields or tenant claims in action input.
    const p = this.resolveServerPrincipal();
    if (!p || !valid(p.tenantId) || !valid(p.actorId) || !roles.has(p.role) ||
        p.authenticated !== true) fail('verified_principal_required');
    const bound = this.db.prepare('SELECT tenant_id FROM synthetic_order_tenants WHERE order_id=?').get(orderId);
    if (!bound || bound.tenant_id !== p.tenantId) fail('tenant_scope_denied');
    if (!allowedRoles.includes(p.role)) fail('role_denied');
    const order = this.store.get(orderId);
    if (!order) fail('unknown_order');
    if (p.role !== 'operator' && order.parties[p.role] !== p.actorId)
      fail('actor_scope_denied');
    return p;
  }

  read(orderId) {
    this._authorize(orderId, ['operator', 'donor', 'receiver', 'transport']);
    return this.store.get(orderId);
  }
  /** Authorize before any payment-state lookup to prevent cross-tenant state oracles. */
  assertPickupPermission(orderId) {
    this._authorize(orderId, ['transport']);
  }
  /** Receiver-only authorization before checking any delivery or receipt state. */
  assertReceiptPermission(orderId) {
    return this._authorize(orderId, ['receiver']);
  }
  approve({ id, role, evidenceRef, at }) {
    const p = this._authorize(id, [role]);
    if (p.role === 'operator' || !['donor','receiver','transport'].includes(role))
      fail('role_denied');
    return this.store.approve({ id, role: p.role, actorId: p.actorId, evidenceRef, at });
  }
  pickup({ id, evidenceRef, at }) {
    const p = this._authorize(id, ['transport']);
    return this.store.pickup({ id, actorId: p.actorId, evidenceRef, at });
  }
  cancel({ id, evidenceRef, at }) {
    const p = this._authorize(id, ['donor', 'receiver', 'transport']);
    return this.store.cancel({ id, actorId: p.actorId, evidenceRef, at });
  }
}
