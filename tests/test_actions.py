import unittest
from app.service import Service, ServiceError

class ActionTests(unittest.TestCase):
    def setUp(self):
        self.service=Service()
        self.sales=self.service.users['sales']
        self.ceo=self.service.users['ceo']

    def tearDown(self): self.service.db.close()

    def propose(self,document_id='deal',user=None):
        return self.service.propose(user or self.sales,dict(document_id=document_id,kind='create_task',title='Draft the Atlas follow-up'))

    def test_separate_reviewer_then_idempotent_simulation(self):
        action=self.propose()
        approved=self.service.transition(self.ceo,action['id'],'approve')
        self.assertEqual(approved['status'],'approved')
        first=self.service.transition(self.ceo,action['id'],'execute')
        second=self.service.transition(self.ceo,action['id'],'execute')
        self.assertEqual(first,second)
        self.assertEqual(first['status'],'simulated')
        self.assertEqual(self.service.db.execute("SELECT COUNT(*) FROM audit WHERE event='Action execute'").fetchone()[0],1)

    def test_cannot_self_approve(self):
        action=self.propose(user=self.ceo)
        with self.assertRaises(ServiceError) as error:
            self.service.transition(self.ceo,action['id'],'approve')
        self.assertEqual(error.exception.status,403)

    def test_cannot_execute_without_approval(self):
        action=self.propose()
        with self.assertRaises(ServiceError): self.service.transition(self.ceo,action['id'],'execute')

    def test_cross_tenant_cannot_list_or_transition(self):
        action=self.propose()
        user=self.service.users['outside']
        self.assertEqual(self.service.list_actions(user),[])
        with self.assertRaises(ServiceError) as error: self.service.transition(user,action['id'],'approve')
        self.assertEqual(error.exception.status,404)

    def test_revoked_requester_cannot_have_stale_action_executed(self):
        action=self.propose()
        self.service.transition(self.ceo,action['id'],'approve')
        self.sales['groups'].remove('sales')
        with self.assertRaises(ServiceError) as error: self.service.transition(self.ceo,action['id'],'execute')
        self.assertEqual(error.exception.status,409)

    def test_changed_ancestor_evidence_invalidates_approval(self):
        action=self.propose('atlas-brief',self.service.users['cs'])
        self.service.transition(self.ceo,action['id'],'approve')
        self.service.documents['call']['version']+=1
        with self.assertRaises(ServiceError) as error: self.service.transition(self.ceo,action['id'],'execute')
        self.assertEqual(error.exception.status,409)

    def test_approver_revocation_blocks_execution(self):
        action=self.propose()
        self.service.transition(self.ceo,action['id'],'approve')
        self.ceo['groups'].remove('sales')
        with self.assertRaises(ServiceError): self.service.transition(self.ceo,action['id'],'execute')

    def test_invalid_target_and_unregistered_tool_rejected(self):
        with self.assertRaises(ServiceError): self.propose('cash')
        with self.assertRaises(ServiceError): self.service.propose(self.sales,dict(document_id='deal',kind='send_money',title='No'))

    def test_it_is_not_content_admin_or_workflow_operator(self):
        with self.assertRaises(ServiceError): self.propose('it-guide',self.service.users['it'])

    def test_audit_is_actor_scoped_and_removed_after_revocation(self):
        self.propose()
        self.assertEqual(len(self.service.workspace(self.sales)['activities']),1)
        self.assertEqual(self.service.workspace(self.ceo)['activities'],[])
        self.sales['groups'].remove('sales')
        self.assertEqual(self.service.workspace(self.sales)['activities'],[])

if __name__=='__main__': unittest.main()
