"""Offline unit tests for Operation Operator's fictional read-only adapter."""
import unittest
from dataclasses import replace
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path
import sys

spec = spec_from_file_location("operation_operator_adapter", Path(__file__).with_name("synthetic_adapter.py"))
module = module_from_spec(spec)
sys.modules[spec.name] = module
spec.loader.exec_module(module)
FoodSignal, SyntheticAdapter, propose_matches = module.FoodSignal, module.SyntheticAdapter, module.propose_matches
HandoffWindow = module.HandoffWindow

class OperationOperatorTests(unittest.TestCase):
    def test_approval_only_match(self):
        adapter = SyntheticAdapter((
            FoodSignal("demo-bank", "demo-pantry-a", "demo-s1", "surplus", "tomatoes", 50, "boxes"),
            FoodSignal("demo-bank", "demo-pantry-b", "demo-n1", "need", "tomatoes", 30, "boxes")))
        matches = propose_matches(adapter)
        self.assertEqual(len(matches), 1)
        self.assertEqual(matches[0]["quantity"], 30)
        self.assertTrue(matches[0]["human_approval_required"])
        self.assertFalse(matches[0]["dispatched"])
        self.assertFalse(adapter.describe_capabilities()["outbound_actions"])

    def test_no_overallocation(self):
        adapter = SyntheticAdapter((
            FoodSignal("demo-bank", "demo-a", "demo-s", "surplus", "produce", 10, "boxes"),
            FoodSignal("demo-bank", "demo-b", "demo-n1", "need", "produce", 8, "boxes"),
            FoodSignal("demo-bank", "demo-c", "demo-n2", "need", "produce", 8, "boxes")))
        matches = propose_matches(adapter)
        self.assertEqual(sum(x["quantity"] for x in matches), 10)
        reversed_adapter = SyntheticAdapter(adapter.fetch_surplus() + adapter.fetch_needs()[::-1])
        self.assertEqual(matches, propose_matches(reversed_adapter))

    def test_real_data_rejected(self):
        with self.assertRaises(ValueError):
            FoodSignal("real-bank", "demo-a", "demo-s", "surplus", "produce", 10, "boxes", False)

    def test_priority_and_input_order(self):
        supply = FoodSignal("demo-bank", "demo-a", "demo-s", "surplus", "produce", 10, "boxes")
        first = FoodSignal("demo-bank", "demo-b", "demo-n1", "need", "produce", 8, "boxes")
        second = FoodSignal("demo-bank", "demo-c", "demo-n2", "need", "produce", 8, "boxes", priority=1)
        matches = propose_matches(SyntheticAdapter((supply, first, second)))
        self.assertEqual(matches, propose_matches(SyntheticAdapter((second, first, supply))))
        self.assertEqual([(match["to"], match["quantity"]) for match in matches],
                         [("demo-c", 8), ("demo-b", 2)])

    def test_milk_capacity_and_timing(self):
        supply = FoodSignal("demo-store", "demo-c", "demo-s", "surplus", "milk", 5000, "gallons")
        for handoff, expected in (
            (HandoffWindow(800, 800, 840, 900), [800]),
            (HandoffWindow(300, 800, 840, 900), [300]),
            (HandoffWindow(800, 500, 840, 900), [500]),
            (HandoffWindow(800, 800, 960, 900), []),
            (None, []),
        ):
            with self.subTest(handoff=handoff):
                need = FoodSignal("demo-pantry", "demo-a", "demo-n", "need", "milk", 2000,
                                  "gallons", handoff=handoff)
                matches = propose_matches(SyntheticAdapter((supply, need)))
                self.assertEqual([match["quantity"] for match in matches], expected)
                self.assertTrue(all(match["human_approval_required"] and not match["dispatched"]
                                    for match in matches))

    def test_no_cross_unit_match(self):
        adapter = SyntheticAdapter((
            FoodSignal("demo-bank", "demo-a", "demo-s", "surplus", "produce", 10, "kg"),
            FoodSignal("demo-bank", "demo-b", "demo-n", "need", "produce", 10, "boxes")))
        self.assertEqual(propose_matches(adapter), [])

    def test_small_recipients_then_storage_and_escalation(self):
        supply = FoodSignal("demo-store", "demo-c", "demo-s", "surplus", "milk", 5000, "gallons")
        pantry = FoodSignal("demo-pantry", "demo-a", "demo-n1", "need", "milk", 2000, "gallons",
                            handoff=HandoffWindow(800, 800, 840, 900))
        school = FoodSignal("demo-school", "demo-b", "demo-n2", "need", "milk", 5, "gallons",
                            handoff=HandoffWindow(5, 5, 840, 900))
        cold_room = FoodSignal("demo-warehouse", "demo-d", "demo-h1", "storage", "milk", 1000, "gallons",
                               handoff=HandoffWindow(1000, 1000, 840, 900))
        unknown = FoodSignal("demo-warehouse", "demo-e", "demo-h2", "storage", "milk", 5000, "gallons")
        late = FoodSignal("demo-warehouse", "demo-f", "demo-h3", "storage", "milk", 5000, "gallons",
                          handoff=HandoffWindow(5000, 5000, 960, 900))
        plan = module.plan_redistribution(SyntheticAdapter((supply, school, pantry)),
                                          (unknown, cold_room, late))
        self.assertEqual([(m["to"], m["quantity"]) for m in plan["recipient_proposals"]],
                         [("demo-a", 800), ("demo-b", 5)])
        self.assertEqual([(m["to"], m["quantity"]) for m in plan["storage_proposals"]],
                         [("demo-d", 1000)])
        self.assertTrue(plan["storage_proposals"][0]["human_approval_required"])
        self.assertFalse(plan["storage_proposals"][0]["dispatched"])
        self.assertEqual(plan["unplaced"][0]["quantity"], 3195)
        self.assertTrue(plan["unplaced"][0]["needs_human_review"])

    def test_fail_closed_on_external_capabilities(self):
        class UnsafeAdapter:
            def describe_capabilities(self):
                return {"mode": "production", "read_only": False, "outbound_actions": True}
        with self.assertRaises(PermissionError):
            propose_matches(UnsafeAdapter())

    def test_commercial_fallback_only_uses_eligible_unplaced_surplus(self):
        terms = module.SaleTerms(True, True, True, 125)
        supply = FoodSignal("demo-store", "demo-c", "demo-s", "surplus", "milk", 100,
                            "gallons", sale_terms=terms)
        window = HandoffWindow(100, 100, 840, 900)
        recipient = FoodSignal("demo-pantry", "demo-a", "demo-n", "need", "milk", 30,
                               "gallons", handoff=window)
        storage = FoodSignal("demo-storage", "demo-d", "demo-h", "storage", "milk", 20,
                             "gallons", handoff=window)
        buyer = FoodSignal("demo-grocer", "demo-b", "demo-b1", "buyer", "milk", 100,
                           "gallons", handoff=window, buyer_max_unit_price_cents=125)
        plan = module.plan_redistribution(SyntheticAdapter((supply, recipient)), (storage,),
                                          buyer_options=(buyer,))
        self.assertEqual(plan["recipient_proposals"][0]["quantity"], 30)
        self.assertEqual(plan["storage_proposals"][0]["quantity"], 20)
        self.assertEqual(plan["unplaced"], [])
        offer, = plan["commercial_proposals"]
        self.assertEqual((offer["quantity"], offer["total_price_cents"], offer["currency"]),
                         (50, 6250, "USD"))
        self.assertTrue(offer["human_approval_required"])
        self.assertFalse(offer["dispatched"])

        for restricted_terms, buyer_option in (
            (None, buyer),
            (replace(terms, seller_authorized=False), buyer),
            (replace(terms, resale_eligible=False), buyer),
            (replace(terms, donation_options_exhausted=False), buyer),
            (terms, replace(buyer, buyer_max_unit_price_cents=None)),
            (terms, replace(buyer, buyer_max_unit_price_cents=124)),
            (terms, replace(buyer, handoff=None)),
        ):
            with self.subTest(terms=restricted_terms, buyer=buyer_option):
                restricted = replace(supply, sale_terms=restricted_terms)
                plan = module.plan_redistribution(SyntheticAdapter((restricted, recipient)),
                                                  (storage,), buyer_options=(buyer_option,))
                self.assertEqual(plan["commercial_proposals"], [])
                self.assertEqual(plan["unplaced"][0]["quantity"], 50)

if __name__ == "__main__":
    unittest.main()
