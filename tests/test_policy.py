import copy
import unittest
from datetime import datetime, timedelta, timezone
from app.service import Service, ServiceError
from app.policy import can_read

class PolicyTests(unittest.TestCase):
    def setUp(self):
        self.service = Service()
        self.documents = self.service.documents
        self.users = self.service.users

    def tearDown(self):
        self.service.db.close()

    def test_tenant_boundary_even_when_group_names_match(self):
        self.assertFalse(can_read(self.users['outside'],self.documents['cash'],self.documents))
        self.assertEqual(self.service.workspace(self.users['outside'])['documents'],[])

    def test_ceo_and_it_cannot_read_private_people_record(self):
        for uid in ('ceo','it','sales','finance','employee'):
            self.assertFalse(can_read(self.users[uid],self.documents['people-private'],self.documents))
        self.assertTrue(can_read(self.users['people'],self.documents['people-private'],self.documents))

    def test_intersection_of_sources_is_required_for_compiled_brief(self):
        for uid in ('sales','ops','employee'):
            self.assertFalse(can_read(self.users[uid],self.documents['atlas-brief'],self.documents))
        for uid in ('ceo','cs'):
            self.assertTrue(can_read(self.users[uid],self.documents['atlas-brief'],self.documents))

    def test_explicit_deny_wins(self):
        self.documents['cash']['deny']=['user:ceo']
        self.assertFalse(can_read(self.users['ceo'],self.documents['cash'],self.documents))

    def test_revocation_removes_derived_documents_and_citations_immediately(self):
        user = self.users['ceo']
        self.assertTrue(can_read(user,self.documents['board'],self.documents))
        self.documents['cash']['allow']=[]
        self.assertFalse(can_read(user,self.documents['board'],self.documents))
        result = self.service.ask(user,'cash finance leadership')
        self.assertNotIn('2,400,000',result['answer'])
        self.assertNotIn('cash',[c['id'] for c in result['citations']])
        self.assertNotIn('board',[c['id'] for c in result['citations']])

    def test_unmapped_expired_deleted_missing_and_cyclic_lineage_fail_closed(self):
        for mutation in ('unknown','expired','deleted','missing','cycle'):
            with self.subTest(mutation=mutation):
                docs=copy.deepcopy(self.documents)
                d=docs['strategy']
                if mutation=='unknown': d['allow']=['group:unknown']
                if mutation=='expired': d['acl_valid_until']=(datetime.now(timezone.utc)-timedelta(seconds=1)).isoformat()
                if mutation=='deleted': d['deleted']=True
                if mutation=='missing': d['source_ids']=['does-not-exist']
                if mutation=='cycle': d['source_ids']=['strategy']
                self.assertFalse(can_read(self.users['ceo'],d,docs))

    def test_malformed_acl_values_deny_instead_of_crashing_retrieval(self):
        self.documents['strategy']['acl_valid_until']=123
        self.documents['cash']['allow']={'bad':'shape'}
        workspace=self.service.workspace(self.users['ceo'])
        self.assertNotIn('strategy',[d['id'] for d in workspace['documents']])
        self.assertNotIn('cash',[d['id'] for d in workspace['documents']])

    def test_disabled_user_and_removed_group_fail_closed(self):
        self.users['sales']['active']=False
        self.assertFalse(can_read(self.users['sales'],self.documents['deal'],self.documents))
        self.users['ceo']['groups'].remove('finance')
        self.assertFalse(can_read(self.users['ceo'],self.documents['board'],self.documents))

    def test_missing_and_forbidden_ids_have_same_error(self):
        responses=[]
        for doc_id in ('cash','does-not-exist'):
            with self.assertRaises(ServiceError) as err:
                self.service.document(self.users['employee'],doc_id)
            responses.append((err.exception.status,str(err.exception)))
        self.assertEqual(responses[0],responses[1])

    def test_no_private_metadata_or_answer_text_in_employee_workspace(self):
        import json
        workspace=json.dumps(self.service.workspace(self.users['employee']))
        for fragment in ('Restricted employee case','people-private','PEOPLE-DEMO-42','cash','2,400,000','Atlas'):
            self.assertNotIn(fragment,workspace)
        answer=self.service.ask(self.users['employee'],'PEOPLE-DEMO-42 private case cash')
        self.assertEqual(answer['citations'],[])

    def test_no_cross_user_answer_cache(self):
        self.assertIn('2,400,000',self.service.ask(self.users['finance'],'cash')['answer'])
        self.assertNotIn('2,400,000',self.service.ask(self.users['employee'],'cash')['answer'])

if __name__=='__main__': unittest.main()
