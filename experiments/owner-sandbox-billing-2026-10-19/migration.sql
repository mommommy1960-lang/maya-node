-- Additive, isolated owner demo billing tables. Does not alter existing tables.
CREATE TABLE IF NOT EXISTS owner_sandbox_billing (
  owner_id TEXT PRIMARY KEY,
  revision INTEGER NOT NULL DEFAULT 0,
  snapshot TEXT NOT NULL DEFAULT '{}'
);
INSERT OR IGNORE INTO owner_sandbox_billing(owner_id) VALUES ('maya-owner-demo');
CREATE TABLE IF NOT EXISTS owner_sandbox_events (event_id TEXT PRIMARY KEY);
CREATE TABLE IF NOT EXISTS owner_sandbox_checkouts (
  checkout_id TEXT PRIMARY KEY,
  owner_id TEXT NOT NULL
);
