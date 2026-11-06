CREATE TABLE jobs(id TEXT PRIMARY KEY, payload TEXT NOT NULL, state TEXT NOT NULL CHECK(state IN ('pending','queued','canceled','dispatch_committed','unknown','sent')), attempt TEXT, receipt TEXT);
CREATE INDEX jobs_state ON jobs(state);
CREATE TRIGGER immutable_payload BEFORE UPDATE OF payload ON jobs BEGIN SELECT RAISE(ABORT,'immutable payload'); END;
CREATE TABLE service_guard(id INTEGER PRIMARY KEY CHECK(id=1), paused INTEGER NOT NULL CHECK(paused IN (0,1)), reason TEXT NOT NULL);
INSERT INTO service_guard VALUES(1,1,'initial_review_required');
