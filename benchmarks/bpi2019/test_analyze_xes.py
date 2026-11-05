import tempfile
import unittest
from pathlib import Path
from analyze_xes import analyze

FIXTURE = """<log xmlns="http://www.xes-standard.org/">
<trace>
<string key="concept:name" value="PO-1-10"/>
<string key="Item Category" value="3-way matching, invoice after goods receipt"/>
<event><string key="concept:name" value="Record Goods Receipt"/><date key="time:timestamp" value="2018-01-01T10:00:00+00:00"/></event>
<event><string key="concept:name" value="Record Invoice Receipt"/><date key="time:timestamp" value="2018-01-02T10:00:00+00:00"/></event>
<event><string key="concept:name" value="Clear Invoice"/><date key="time:timestamp" value="2018-01-04T10:00:00+00:00"/></event>
</trace></log>"""

class AnalyzerTests(unittest.TestCase):
    def run_fixture(self, content):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        path = Path(tmp.name) / "fixture.xes"
        path.write_text(content, encoding="utf-8")
        return analyze(path)

    def test_case_event_category_and_intervals(self):
        result = self.run_fixture(FIXTURE)
        self.assertEqual(result["cases"], 1)
        self.assertEqual(result["events"], 3)
        self.assertEqual(result["item_categories"]["3-way matching, invoice after goods receipt"], 1)
        self.assertEqual(result["throughput_diagnostics"]["goods_receipt_to_first_invoice"]["median_hours"], 24.0)
        self.assertEqual(result["throughput_diagnostics"]["first_invoice_to_first_clear"]["median_hours"], 48.0)

    def test_timezone_less_dates_are_not_assumed(self):
        result = self.run_fixture(FIXTURE.replace("+00:00", ""))
        self.assertEqual(result["data_quality"]["missing_or_unparseable_timestamps"], 3)
        self.assertIsNone(result["timestamp_range"]["min"])

if __name__ == "__main__":
    unittest.main()
