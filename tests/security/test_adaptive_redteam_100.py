# SPDX-License-Identifier: CERL-1.0
"""Adaptive red-team wave: 100 materially enumerated adversarial cases.

These are controlled attacks against MAYA's local security invariants. Each case has
an explicit expected defensive outcome. A passing case means that specific attack
was blocked in this implementation; it is not a claim of global security.
"""
import copy
import time
import unittest

from src.sovereign.consent_tokens import ConsentTokenManager, ConsentScope, ConsentStatus
from src.services.ledger.ledger import ImmutableLedger


class TestAdaptiveRedTeam100(unittest.TestCase):
    def setUp(self):
        self.m = ConsentTokenManager(secret_key="redteam-test-key")

    def _fresh(self, **kw):
        args = dict(user_id="alice", operation="op.read", scope=ConsentScope.SINGLE_OPERATION,
                    ttl_seconds=300, metadata={"purpose": "test", "level": 1})
        args.update(kw)
        return self.m.generate_token(**args)

    def _assert_tamper_rejected(self, mutator):
        t = self._fresh()
        mutator(t)
        self.assertFalse(self.m.verify_token(t))

    # 01-10: subject tampering
    def test_001_user_swap(self): self._assert_tamper_rejected(lambda t: setattr(t, 'user_id', 'bob'))
    def test_002_user_empty(self): self._assert_tamper_rejected(lambda t: setattr(t, 'user_id', ''))
    def test_003_user_case(self): self._assert_tamper_rejected(lambda t: setattr(t, 'user_id', 'ALICE'))
    def test_004_user_space(self): self._assert_tamper_rejected(lambda t: setattr(t, 'user_id', 'alice '))
    def test_005_user_prefix(self): self._assert_tamper_rejected(lambda t: setattr(t, 'user_id', 'xalice'))
    def test_006_user_suffix(self): self._assert_tamper_rejected(lambda t: setattr(t, 'user_id', 'alicex'))
    def test_007_user_unicode(self): self._assert_tamper_rejected(lambda t: setattr(t, 'user_id', 'a\u0131ice'))
    def test_008_user_nullish(self): self._assert_tamper_rejected(lambda t: setattr(t, 'user_id', 'alice\x00'))
    def test_009_user_newline(self): self._assert_tamper_rejected(lambda t: setattr(t, 'user_id', 'alice\nadmin'))
    def test_010_user_pathlike(self): self._assert_tamper_rejected(lambda t: setattr(t, 'user_id', '../alice'))

    # 11-20: operation/scope tampering
    def test_011_op_swap(self): self._assert_tamper_rejected(lambda t: setattr(t, 'operation', 'op.write'))
    def test_012_op_empty(self): self._assert_tamper_rejected(lambda t: setattr(t, 'operation', ''))
    def test_013_op_case(self): self._assert_tamper_rejected(lambda t: setattr(t, 'operation', 'OP.READ'))
    def test_014_op_space(self): self._assert_tamper_rejected(lambda t: setattr(t, 'operation', 'op.read '))
    def test_015_op_admin(self): self._assert_tamper_rejected(lambda t: setattr(t, 'operation', 'admin'))
    def test_016_op_wildcard(self): self._assert_tamper_rejected(lambda t: setattr(t, 'operation', '*'))
    def test_017_op_newline(self): self._assert_tamper_rejected(lambda t: setattr(t, 'operation', 'op.read\nop.write'))
    def test_018_scope_session(self): self._assert_tamper_rejected(lambda t: setattr(t, 'scope', ConsentScope.SESSION))
    def test_019_scope_batch(self): self._assert_tamper_rejected(lambda t: setattr(t, 'scope', ConsentScope.BATCH))
    def test_020_scope_flip_after_sign(self):
        t=self._fresh(scope=ConsentScope.SESSION); t.scope=ConsentScope.SINGLE_OPERATION; self.assertFalse(self.m.verify_token(t))

    # 21-30: time/expiry tampering
    def test_021_extend_expiry(self): self._assert_tamper_rejected(lambda t: setattr(t,'expires_at',t.expires_at+999999))
    def test_022_reduce_expiry(self): self._assert_tamper_rejected(lambda t: setattr(t,'expires_at',t.expires_at-1))
    def test_023_future_timestamp(self): self._assert_tamper_rejected(lambda t: setattr(t,'timestamp',t.timestamp+1000))
    def test_024_past_timestamp(self): self._assert_tamper_rejected(lambda t: setattr(t,'timestamp',0))
    def test_025_zero_expiry(self): self._assert_tamper_rejected(lambda t: setattr(t,'expires_at',0))
    def test_026_negative_expiry(self): self._assert_tamper_rejected(lambda t: setattr(t,'expires_at',-1))
    def test_027_infinite_expiry(self): self._assert_tamper_rejected(lambda t: setattr(t,'expires_at',float('inf')))
    def test_028_expired_token(self):
        t=self._fresh(ttl_seconds=-1); self.assertFalse(self.m.verify_token(t))
    def test_029_expiry_boundary(self):
        t=self._fresh(ttl_seconds=0); time.sleep(0.001); self.assertFalse(self.m.verify_token(t))
    def test_030_revoked_beats_time(self):
        t=self._fresh(); self.m.revoke_token(t.token_id); self.assertFalse(self.m.verify_token(t))

    # 31-45: signature attacks
    def test_031_signature_empty(self): self._assert_tamper_rejected(lambda t:setattr(t,'signature',''))
    def test_032_signature_zeroes(self): self._assert_tamper_rejected(lambda t:setattr(t,'signature','0'*64))
    def test_033_signature_ones(self): self._assert_tamper_rejected(lambda t:setattr(t,'signature','1'*64))
    def test_034_signature_truncate(self): self._assert_tamper_rejected(lambda t:setattr(t,'signature',t.signature[:-1]))
    def test_035_signature_extend(self): self._assert_tamper_rejected(lambda t:setattr(t,'signature',t.signature+'0'))
    def test_036_signature_upper(self): self._assert_tamper_rejected(lambda t:setattr(t,'signature',t.signature.upper()))
    def test_037_signature_reverse(self): self._assert_tamper_rejected(lambda t:setattr(t,'signature',t.signature[::-1]))
    def test_038_signature_prefix(self): self._assert_tamper_rejected(lambda t:setattr(t,'signature','00'+t.signature[2:]))
    def test_039_signature_suffix(self): self._assert_tamper_rejected(lambda t:setattr(t,'signature',t.signature[:-2]+'00'))
    def test_040_signature_other_token(self):
        a=self._fresh(); b=self._fresh(operation='op.write'); a.signature=b.signature; self.assertFalse(self.m.verify_token(a))
    def test_041_signature_other_manager(self):
        t=self._fresh(); other=ConsentTokenManager(secret_key='other'); other.tokens[t.token_id]=t; self.assertFalse(other.verify_token(t))
    def test_042_signature_whitespace(self): self._assert_tamper_rejected(lambda t:setattr(t,'signature',' '+t.signature))
    def test_043_signature_newline(self): self._assert_tamper_rejected(lambda t:setattr(t,'signature',t.signature+'\n'))
    def test_044_signature_hex_case_mutation(self): self._assert_tamper_rejected(lambda t:setattr(t,'signature',('f' if t.signature[0]!='f' else 'e')+t.signature[1:]))
    def test_045_signature_mid_mutation(self): self._assert_tamper_rejected(lambda t:setattr(t,'signature',t.signature[:32]+('0' if t.signature[32]!='0' else '1')+t.signature[33:]))

    # 46-60: metadata integrity attacks
    def test_046_metadata_value(self): self._assert_tamper_rejected(lambda t:t.metadata.__setitem__('level',2))
    def test_047_metadata_add_admin(self): self._assert_tamper_rejected(lambda t:t.metadata.__setitem__('admin',True))
    def test_048_metadata_remove(self): self._assert_tamper_rejected(lambda t:t.metadata.pop('purpose'))
    def test_049_metadata_empty(self): self._assert_tamper_rejected(lambda t:setattr(t,'metadata',{}))
    def test_050_metadata_nested(self): self._assert_tamper_rejected(lambda t:t.metadata.__setitem__('nested',{'role':'admin'}))
    def test_051_metadata_list(self): self._assert_tamper_rejected(lambda t:t.metadata.__setitem__('roles',['admin']))
    def test_052_metadata_null(self): self._assert_tamper_rejected(lambda t:t.metadata.__setitem__('purpose',None))
    def test_053_metadata_unicode(self): self._assert_tamper_rejected(lambda t:t.metadata.__setitem__('purpose','t\u0435st'))
    def test_054_metadata_newline(self): self._assert_tamper_rejected(lambda t:t.metadata.__setitem__('purpose','test\nadmin'))
    def test_055_metadata_number(self): self._assert_tamper_rejected(lambda t:t.metadata.__setitem__('purpose',1))
    def test_056_metadata_bool(self): self._assert_tamper_rejected(lambda t:t.metadata.__setitem__('purpose',True))
    def test_057_metadata_extra_zero(self): self._assert_tamper_rejected(lambda t:t.metadata.__setitem__('x',0))
    def test_058_metadata_extra_empty(self): self._assert_tamper_rejected(lambda t:t.metadata.__setitem__('x',''))
    def test_059_metadata_key_case(self): self._assert_tamper_rejected(lambda t:t.metadata.__setitem__('Purpose','test'))
    def test_060_metadata_copy_mutation(self):
        t=self._fresh(); t.metadata=copy.deepcopy(t.metadata); t.metadata['level']=999; self.assertFalse(self.m.verify_token(t))

    # 61-75: token identity/state/replay
    def test_061_unknown_token(self):
        t=self._fresh(); del self.m.tokens[t.token_id]; self.assertFalse(self.m.verify_token(t))
    def test_062_token_id_swap(self): self._assert_tamper_rejected(lambda t:setattr(t,'token_id','deadbeef'))
    def test_063_token_id_empty(self): self._assert_tamper_rejected(lambda t:setattr(t,'token_id',''))
    def test_064_token_id_other(self):
        a=self._fresh(); b=self._fresh(); a.token_id=b.token_id; self.assertFalse(self.m.verify_token(a))
    def test_065_single_replay(self):
        t=self._fresh(); self.assertTrue(self.m.use_token(t.token_id)); self.assertFalse(self.m.use_token(t.token_id))
    def test_066_revoked_use(self):
        t=self._fresh(); self.m.revoke_token(t.token_id); self.assertFalse(self.m.use_token(t.token_id))
    def test_067_expired_use(self):
        t=self._fresh(ttl_seconds=-1); self.assertFalse(self.m.use_token(t.token_id))
    def test_068_used_verify(self):
        t=self._fresh(); self.m.use_token(t.token_id); self.assertFalse(self.m.verify_token(t))
    def test_069_revoked_verify(self):
        t=self._fresh(); self.m.revoke_token(t.token_id); self.assertFalse(self.m.verify_token(t))
    def test_070_unknown_revoke(self): self.assertFalse(self.m.revoke_token('missing'))
    def test_071_unknown_use(self): self.assertFalse(self.m.use_token('missing'))
    def test_072_unknown_get(self): self.assertIsNone(self.m.get_token('missing'))
    def test_073_user_filter_isolation(self):
        self._fresh(user_id='alice'); self._fresh(user_id='bob'); self.assertTrue(all(t.user_id=='alice' for t in self.m.get_user_tokens('alice')))
    def test_074_session_reuse_explicit(self):
        t=self._fresh(scope=ConsentScope.SESSION); self.assertTrue(self.m.use_token(t.token_id)); self.assertTrue(self.m.use_token(t.token_id))
    def test_075_batch_reuse_explicit(self):
        t=self._fresh(scope=ConsentScope.BATCH); self.assertTrue(self.m.use_token(t.token_id)); self.assertTrue(self.m.use_token(t.token_id))

    # 76-100: ledger tamper attacks
    def _ledger(self):
        l=ImmutableLedger(); l.append('a',{'x':1}); l.append('b',{'y':2}); l.append('c',{'z':3}); return l
    def _ledger_attack(self, mutator):
        l=self._ledger(); mutator(l); self.assertFalse(l.verify_integrity())
    def test_076_ledger_data(self): self._ledger_attack(lambda l:l.entries[1].data.__setitem__('x',9))
    def test_077_ledger_operation(self): self._ledger_attack(lambda l:setattr(l.entries[1],'operation','evil'))
    def test_078_ledger_timestamp(self): self._ledger_attack(lambda l:setattr(l.entries[1],'timestamp',0))
    def test_079_ledger_index(self): self._ledger_attack(lambda l:setattr(l.entries[1],'index',99))
    def test_080_ledger_previous_hash(self): self._ledger_attack(lambda l:setattr(l.entries[2],'previous_hash','0'*64))
    def test_081_ledger_entry_hash(self): self._ledger_attack(lambda l:setattr(l.entries[2],'entry_hash','0'*64))
    def test_082_ledger_genesis_data(self): self._ledger_attack(lambda l:l.entries[0].data.__setitem__('note','evil'))
    def test_083_ledger_genesis_prev(self): self._ledger_attack(lambda l:setattr(l.entries[0],'previous_hash','1'*64))
    def test_084_ledger_genesis_hash(self): self._ledger_attack(lambda l:setattr(l.entries[0],'entry_hash','1'*64))
    def test_085_ledger_middle_delete(self): self._ledger_attack(lambda l:l.entries.pop(2))
    def test_086_ledger_first_delete(self): self._ledger_attack(lambda l:l.entries.pop(0))
    def test_087_ledger_reorder(self): self._ledger_attack(lambda l:l.entries.__setitem__(slice(1,3),[l.entries[2],l.entries[1]]))
    def test_088_ledger_duplicate(self): self._ledger_attack(lambda l:l.entries.insert(2,copy.deepcopy(l.entries[1])))
    def test_089_ledger_append_forged(self):
        def m(l):
            e=copy.deepcopy(l.entries[-1]); e.index+=1; l.entries.append(e)
        self._ledger_attack(m)
    def test_090_ledger_data_add(self): self._ledger_attack(lambda l:l.entries[2].data.__setitem__('admin',True))
    def test_091_ledger_data_remove(self): self._ledger_attack(lambda l:l.entries[2].data.pop('y'))
    def test_092_ledger_data_type(self): self._ledger_attack(lambda l:l.entries[2].data.__setitem__('y','2'))
    def test_093_ledger_op_empty(self): self._ledger_attack(lambda l:setattr(l.entries[3],'operation',''))
    def test_094_ledger_op_case(self): self._ledger_attack(lambda l:setattr(l.entries[3],'operation','C'))
    def test_095_ledger_time_future(self): self._ledger_attack(lambda l:setattr(l.entries[3],'timestamp',l.entries[3].timestamp+999))
    def test_096_ledger_index_zero(self): self._ledger_attack(lambda l:setattr(l.entries[3],'index',0))
    def test_097_ledger_prev_from_genesis(self): self._ledger_attack(lambda l:setattr(l.entries[3],'previous_hash',l.entries[0].entry_hash))
    def test_098_ledger_hash_truncate(self): self._ledger_attack(lambda l:setattr(l.entries[3],'entry_hash',l.entries[3].entry_hash[:-1]))
    def test_099_ledger_hash_extend(self): self._ledger_attack(lambda l:setattr(l.entries[3],'entry_hash',l.entries[3].entry_hash+'0'))
    def test_100_ledger_chain_splice(self):
        def m(l):
            l.entries[2].data={'y':'evil'}
            l.entries[2].entry_hash=l._compute_hash(l.entries[2])
            # attacker forgets to rewrite downstream linkage
        self._ledger_attack(m)


if __name__ == '__main__':
    unittest.main()
