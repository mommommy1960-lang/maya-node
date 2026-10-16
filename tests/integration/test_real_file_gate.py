import json
from pathlib import Path
import tempfile
import threading
import unittest
from unittest.mock import patch
from src.adapters.file_write_gate import FileWriteGate, verify_receipts

class RealFileGateTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.g = FileWriteGate(Path(self.temp.name) / 'run')
    def tearDown(self):
        self.g.close(); self.temp.cleanup()
    def test_real_write_then_revocation(self):
        t=self.g.authorize('owner','yes.txt','actual bytes')
        self.assertEqual(self.g.execute(t,'owner','yes.txt','actual bytes')['outcome'],'created')
        self.assertEqual((self.g.output/'yes.txt').read_bytes(),b'actual bytes')
        self.g.revoke(t)
        self.assertEqual(self.g.execute(t,'owner','yes.txt','actual bytes')['reason'],'permission_revoked')
        self.assertTrue(verify_receipts(self.g.root/'receipts.jsonl'))
    def test_revoke_prevents_real_side_effect(self):
        t=self.g.authorize('owner','no.txt','x');self.g.revoke(t)
        self.assertEqual(self.g.execute(t,'owner','no.txt','x')['outcome'],'blocked')
        self.assertFalse((self.g.output/'no.txt').exists())
    def test_payload_actor_filename_are_bound(self):
        t=self.g.authorize('owner','yes.txt','x')
        for actor,name,text in [('other','yes.txt','x'),('owner','other.txt','x'),('owner','yes.txt','y')]:
            self.assertEqual(self.g.execute(t,actor,name,text)['reason'],'request_does_not_match_permission')
        self.assertEqual(list(self.g.output.iterdir()),[])
        self.assertEqual(self.g.execute(t,'owner','yes.txt','x')['outcome'],'created')
    def test_expiry(self):
        t=self.g.authorize('owner','expired.txt','x')
        with patch('src.sovereign.consent_tokens.time.time',return_value=self.g.tokens.get_token(t).expires_at):
            self.assertEqual(self.g.execute(t,'owner','expired.txt','x')['reason'],'permission_expired')
        self.assertFalse((self.g.output/'expired.txt').exists())
    def test_single_use(self):
        t=self.g.authorize('owner','yes.txt','x');self.g.execute(t,'owner','yes.txt','x')
        self.assertEqual(self.g.execute(t,'owner','yes.txt','x')['reason'],'permission_used')
    def test_existing_file_never_overwritten(self):
        (self.g.output/'yes.txt').write_text('original')
        t=self.g.authorize('owner','yes.txt','replacement')
        self.assertEqual(self.g.execute(t,'owner','yes.txt','replacement')['reason'],'target_exists')
        self.assertEqual((self.g.output/'yes.txt').read_text(),'original')
    def test_symlink_never_followed(self):
        outside=Path(self.temp.name)/'outside';outside.write_text('safe')
        (self.g.output/'link').symlink_to(outside)
        t=self.g.authorize('owner','link','bad')
        self.assertEqual(self.g.execute(t,'owner','link','bad')['outcome'],'failed')
        self.assertEqual(outside.read_text(),'safe')
    def test_path_traversal_and_size_rejected(self):
        for name in ['../outside','/tmp/bad','a/b','a\\b']:
            with self.assertRaises(ValueError): self.g.authorize('owner',name,'x')
        with self.assertRaises(ValueError):self.g.authorize('owner','big','x'*65537)
    def test_unknown_permission(self):
        self.assertEqual(self.g.execute('unknown','owner','no.txt','x')['reason'],'unknown_permission')
        self.assertFalse((self.g.output/'no.txt').exists())
    def test_audit_failure_stops_write(self):
        t=self.g.authorize('owner','no.txt','x')
        with patch.object(self.g,'_persist',side_effect=OSError('disk unavailable')):
            with self.assertRaises(OSError):self.g.execute(t,'owner','no.txt','x')
        self.assertFalse((self.g.output/'no.txt').exists())
    def test_concurrent_requests_have_one_side_effect(self):
        t=self.g.authorize('owner','once','x');results=[]
        threads=[threading.Thread(target=lambda:results.append(self.g.execute(t,'owner','once','x')['outcome'])) for _ in range(2)]
        for th in threads:th.start()
        for th in threads:th.join()
        self.assertCountEqual(results,['created','blocked'])
    def test_receipts_detect_edited_entry(self):
        t=self.g.authorize('owner','a','x');self.g.execute(t,'owner','a','x')
        p=self.g.root/'receipts.jsonl';rows=p.read_text().splitlines();r=json.loads(rows[-1]);r['data']['outcome']='fabricated';rows[-1]=json.dumps(r);p.write_text('\n'.join(rows)+'\n')
        self.assertFalse(verify_receipts(p))
    def test_existing_output_directory_refused(self):
        with self.assertRaises(FileExistsError):FileWriteGate(self.g.root)

if __name__=='__main__':unittest.main()
