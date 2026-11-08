import assert from "node:assert/strict";
import test from "node:test";
import { reviewPantryReceiving } from "./pantry-receiving-review.mjs";

const asOf = "2026-11-07T21:00:00Z";
const shipment = { id: "synthetic-delivery", loaded: 40, unit: "carton", dueAt: "2026-11-07T20:00:00Z" };
const receipt = { id: "synthetic-count", shipmentId: shipment.id, received: 36,
  unit: "carton", confirmedBy: "fictional-clerk", recordedAt: "2026-11-07T20:05:00Z" };
const run = (receipts, shipments = [shipment]) => reviewPantryReceiving({ synthetic: true, shipments, receipts }, asOf);

test("four missing cartons are flagged without assigning blame", () => {
  const [review] = run([receipt]).shipments;
  assert.equal(review.difference, 4);
  assert.equal(review.status, "discrepancy_requires_review");
  assert.equal(review.automatedAccusation, false);
});
test("distinguish an overdue receipt from an upcoming arrival", () => {
  const reviews = run([], [shipment, { ...shipment, id: "later", dueAt: "2026-11-07T22:00:00Z" }]).shipments;
  assert.deepEqual(reviews.map(review => review.status), ["receiving_record_missing", "awaiting_receipt"]);
});
test("unit mismatches, future receipts and unlinked records do not count as arrivals", () => {
  const review = run([
    { ...receipt, unit: "case" },
    { ...receipt, id: "later-count", recordedAt: "2026-11-07T22:00:00Z" },
    { ...receipt, id: "unknown-count", shipmentId: "unknown" }
  ]);
  assert.deepEqual(review.unlinked, ["unknown-count"]);
  assert.equal(review.shipments[0].received, 0);
  assert.equal(review.shipments[0].status, "needs_record_review");
  assert.deepEqual(review.shipments[0].errors, ["quantity_unit_mismatch", "future_receipt"]);
});
test("refuse duplicate receipts and require synthetic mode", () => {
  assert.throws(() => run([receipt, receipt]), /duplicate_receipt/);
  assert.throws(() => reviewPantryReceiving({ shipments: [shipment], receipts: [receipt] }, asOf),
    /invalid_synthetic_batch/);
});
