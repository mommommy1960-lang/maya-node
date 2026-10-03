import tempfile
import unittest
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
from src.sovereign.dispatch_queue import DispatchQueue


class QueueTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.path = Path(self.tmp.name) / 'queue.db'
        self.q = DispatchQueue(self.path)
        self.q.enqueue('one', {'recipient': 'test@example.invalid', 'body': 'approved'})

    def test_requires_approval(self):
        self.assertIsNone(self.q.claim('one'))

    def test_cancel_survives_restart(self):
        self.q.approve('one'); self.q.cancel('one')
        self.assertIsNone(DispatchQueue(self.path).claim('one'))

    def test_competing_workers_claim_once(self):
        self.q.approve('one')
        with ThreadPoolExecutor(max_workers=8) as pool:
            claims = list(pool.map(lambda _: DispatchQueue(self.path).claim('one'), range(8)))
        self.assertEqual(sum(c is not None for c in claims), 1)

    def test_timeout_never_retries(self):
        self.q.approve('one')
        def uncertain(payload):
            raise TimeoutError('provider may have accepted')
        with self.assertRaises(TimeoutError):
            self.q.dispatch('one', uncertain)
        q = DispatchQueue(self.path)
        self.assertEqual(q.status('one'), 'unknown')
        self.assertIsNone(q.claim('one'))

    def test_crash_after_claim_never_reclaims(self):
        self.q.approve('one'); self.q.claim('one')
        self.assertIsNone(DispatchQueue(self.path).claim('one'))

    def test_sent_survives_restart(self):
        self.q.approve('one'); calls=[]
        self.q.dispatch('one', lambda p: calls.append(p) or {'id':'receipt'})
        self.assertEqual(DispatchQueue(self.path).dispatch('one', lambda p: calls.append(p)), 'blocked')
        self.assertEqual(len(calls), 1)

    def test_payload_change_rejected(self):
        with self.assertRaises(ValueError):
            self.q.enqueue('one', {'recipient':'changed@example.invalid'})

    def test_cancellation_after_commit_reports_too_late(self):
        self.q.approve('one'); self.q.claim('one')
        self.assertEqual(self.q.cancel('one'), 'too_late')

    def test_cancel_and_claim_race_has_one_winner(self):
        self.q.approve('one')
        with ThreadPoolExecutor(max_workers=2) as pool:
            a=pool.submit(DispatchQueue(self.path).cancel,'one')
            b=pool.submit(DispatchQueue(self.path).claim,'one')
            canceled,claim=a.result(),b.result()
        self.assertTrue((canceled=='canceled' and claim is None) or (canceled=='too_late' and claim is not None))

    def test_wrong_receipt_attempt_rejected(self):
        self.q.approve('one'); self.q.claim('one')
        with self.assertRaises(ValueError):
            self.q.complete('one','wrong', {'id':'receipt'})

    def test_worker_alerts_uncertain_outcome(self):
        self.q.approve('one'); alerts=[]
        def fail(payload): raise TimeoutError()
        self.q.run_once(fail, alerts.append)
        self.assertEqual(alerts[0]['state'], 'unknown')
        self.assertEqual(self.q.inspection()['counts']['unknown'], 1)
        calls=[]
        DispatchQueue(self.path).run_once(lambda p: calls.append(p), alerts.append)
        self.assertEqual(calls, [])

    def test_alert_failure_is_visible(self):
        self.q.approve('one'); self.q.claim('one')
        def fail_alert(item): raise RuntimeError('alert unavailable')
        with self.assertRaises(RuntimeError): self.q.run_once(lambda p: None, fail_alert)

    def test_actual_process_restart_keeps_cancellation(self):
        import subprocess, sys
        self.q.approve('one'); self.q.cancel('one')
        code = 'from src.sovereign.dispatch_queue import DispatchQueue; import sys; q=DispatchQueue(sys.argv[1]); assert q.claim("one") is None; assert q.status("one")=="canceled"'
        subprocess.run([sys.executable, '-c', code, str(self.path)], check=True)
