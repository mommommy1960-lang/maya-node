"""Offline unit tests for Operation Operator's fictional read-only adapter."""
import unittest
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path
import sys

spec = spec_from_file_location("operation_operator_adapter", Path(__file__).with_name("synthetic_adapter.py"))
module = module_from_spec(spec)
sys.modules[spec.name] = module
spec.loader.exec_module(module)
FoodSignal, SyntheticAdapter, propose_matches = module.FoodSignal, module.SyntheticAdapter, module.propose_matches

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
        self.assertEqual(sum(x["quantity"] for x in propose_matches(adapter)), 10)

    def test_real_data_rejected(self):
        with self.assertRaises(ValueError):
            FoodSignal("real-bank", "demo-a", "demo-s", "surplus", "produce", 10, "boxes", False)

    def test_no_cross_unit_match(self):
        adapter = SyntheticAdapter((
            FoodSignal("demo-bank", "demo-a", "demo-s", "surplus", "produce", 10, "kg"),
            FoodSignal("demo-bank", "demo-b", "demo-n", "need", "produce", 10, "boxes")))
        self.assertEqual(propose_matches(adapter), [])

    def test_fail_closed_on_external_capabilities(self):
        class UnsafeAdapter:
            def describe_capabilities(self):
                return {"mode": "production", "read_only": False, "outbound_actions": True}
        with self.assertRaises(PermissionError):
            propose_matches(UnsafeAdapter())

if __name__ == "__main__":
    unittest.main()
