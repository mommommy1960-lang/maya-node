"""Offline acceptance tests for synthetic reconciliation; never touches hosted services."""
import unittest
from demos.aao_reconciliation import analyze

class ReconciliationTests(unittest.TestCase):
    def test_detects_missing_delivery_stock_and_overpayment(self):
        data=[
          {"synthetic":True,"kind":"order","order_id":"demo-001","quantity":100,"amount":"250.00"},
          {"synthetic":True,"kind":"delivery","order_id":"demo-001","quantity":80},
          {"synthetic":True,"kind":"inventory","order_id":"demo-001","quantity":60},
          {"synthetic":True,"kind":"payment","order_id":"demo-001","quantity":0,"amount":"300.00"}]
        result=analyze(data)
        self.assertEqual([x["type"] for x in result["findings"]],["missing_delivery","unaccounted_inventory","payment_exceeds_order"])
        self.assertTrue(result["human_approval_required"])
        self.assertFalse(result["automated_actions"])
    def test_reconciled_order_has_no_findings(self):
        data=[{"synthetic":True,"kind":k,"order_id":"demo-2","quantity":0 if k=="payment" else 5,"amount":"10.00" if k in ("order","payment") else "0"} for k in ("order","delivery","inventory","payment")]
        self.assertEqual(analyze(data)["findings"],[])
    def test_rejects_real_data_and_bad_amounts(self):
        for bad in ([{"kind":"order","order_id":"demo-1","quantity":1}], [{"synthetic":True,"kind":"payment","order_id":"demo-1","quantity":0,"amount":"NaN"}], [{"synthetic":True,"kind":"order","order_id":"real-1","quantity":1}]):
            with self.assertRaises(ValueError):analyze(bad)
if __name__=="__main__":unittest.main()
