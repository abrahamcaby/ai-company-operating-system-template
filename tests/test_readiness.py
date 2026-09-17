import copy
import json
import unittest
from pathlib import Path
from app.readiness import validate

class ReadinessTests(unittest.TestCase):
    def setUp(self):
        self.manifest=json.loads((Path(__file__).parents[1]/'examples/readiness-manifest.json').read_text())

    def test_example_is_complete_but_not_verified(self): self.assertEqual(validate(self.manifest),[])

    def test_missing_recording_policy_is_flagged(self):
        del self.manifest['sample_records'][0]['recording_policy_reference']
        self.assertTrue(any('recording_policy_reference' in e for e in validate(self.manifest)))

    def test_tenant_mismatch_and_unknown_connection_are_flagged(self):
        self.manifest['sample_records'][0]['tenant_id']='other'
        self.manifest['sample_records'][0]['connection_id']='unknown'
        errors=validate(self.manifest)
        self.assertTrue(any('tenant mismatch' in e for e in errors))
        self.assertTrue(any('unknown connection' in e for e in errors))

    def test_access_and_revocation_evidence_required(self):
        self.manifest['connections'][0]['identity_mapping_verified']=False
        self.manifest['connections'][0]['revocation_test']='not tested'
        self.manifest['sample_records'][0]['acl_valid_until']='2020-01-01T00:00:00Z'
        self.assertEqual(len(validate(self.manifest)),3)

    def test_missing_kind_cannot_bypass_recording_checks(self):
        record=self.manifest['sample_records'][0]
        for key in ('kind','account_id','meeting_id','transcript_reference','recording_policy_reference','speaker_and_timestamp_review'):
            record.pop(key)
        errors=validate(self.manifest)
        self.assertTrue(any('missing kind' in e for e in errors))
        self.assertTrue(any('transcript_reference' in e for e in errors))

    def test_invalid_timestamp_and_policy_type_are_rejected(self):
        self.manifest['sample_records'][0]['updated_at']='not-a-timestamp'
        self.manifest['connections'][0]['recording_policy_reference']=42
        self.assertEqual(len(validate(self.manifest)),2)

    def test_bad_shapes_fail_without_crashing(self):
        for value in (None,[],{}, {'connections':[{}]}, {'connections':'bad'}):
            self.assertTrue(validate(value))

if __name__=='__main__': unittest.main()
