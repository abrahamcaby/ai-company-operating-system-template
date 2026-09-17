import json
import threading
import unittest
from urllib.request import Request, urlopen
from urllib.error import HTTPError
from http.server import ThreadingHTTPServer
from app.server import Handler
from app.service import Service

class HTTPTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server=ThreadingHTTPServer(('127.0.0.1',0),Handler)
        cls.server.service=Service()
        cls.thread=threading.Thread(target=cls.server.serve_forever,daemon=True)
        cls.thread.start()
        cls.url='http://127.0.0.1:'+str(cls.server.server_port)

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown(); cls.server.server_close(); cls.server.service.db.close()

    def request(self,path,headers=None,data=None):
        request=Request(self.url+path,headers=headers or {},data=data)
        try:
            response=urlopen(request)
        except HTTPError as error:
            response=error
        return response.status,dict(response.headers),response.read()

    def test_unknown_persona_rejected(self):
        status,_,_=self.request('/api/workspace',{'X-Demo-User':'forged'})
        self.assertEqual(status,401)

    def test_workspace_does_not_expose_private_records_and_no_store(self):
        status,headers,body=self.request('/api/workspace',{'X-Demo-User':'employee'})
        self.assertEqual(status,200)
        self.assertEqual(headers['Cache-Control'],'no-store')
        self.assertNotIn(b'people-private',body)
        self.assertNotIn(b'"allow"',body)

    def test_origin_and_host_are_checked(self):
        for headers in ({'Host':'evil.example'},{'Origin':'https://evil.example'}):
            status,_,_=self.request('/api/health',headers)
            self.assertEqual(status,403)

    def test_malformed_json_and_unexpected_json_shape(self):
        for body in (b'{',b'[]'):
            status,_,_=self.request('/api/ask',{'X-Demo-User':'ceo','Content-Type':'application/json'},body)
            self.assertEqual(status,400)

    def test_permission_error_uses_uniform_resource_response(self):
        statuses=[]
        for uid in ('people-private','missing'):
            status,_,body=self.request('/api/documents/'+uid,{'X-Demo-User':'ceo'})
            statuses.append((status,json.loads(body)))
        self.assertEqual(statuses[0],statuses[1])

    def test_demo_assets_are_served_with_content_security_policy(self):
        for path in ('/','/app.js','/styles.css'):
            status,headers,body=self.request(path)
            self.assertEqual(status,200)
            self.assertTrue(body)
            self.assertIn("script-src 'self'",headers['Content-Security-Policy'])

    def test_http_evidence_and_workflow_round_trip(self):
        sales={'X-Demo-User':'sales','Content-Type':'application/json'}
        ceo={'X-Demo-User':'ceo','Content-Type':'application/json'}
        status,_,body=self.request('/api/ask',sales,json.dumps({'question':'Atlas renewal'}).encode())
        self.assertEqual(status,200)
        citations=json.loads(body)['citations']
        self.assertIn('deal',[c['id'] for c in citations])
        self.assertNotIn('atlas-brief',[c['id'] for c in citations])
        status,_,body=self.request('/api/actions',sales,json.dumps({'document_id':'deal','kind':'create_task','title':'Review Atlas'}).encode())
        self.assertEqual(status,201)
        action=json.loads(body)['action']
        for operation,expected in (('approve','approved'),('execute','simulated')):
            status,_,body=self.request('/api/actions/'+action['id']+'/'+operation,ceo,b'{}')
            self.assertEqual(status,200)
            self.assertEqual(json.loads(body)['action']['status'],expected)

    def test_static_traversal_is_not_served(self):
        status,_,_=self.request('/../app/seed.py')
        self.assertEqual(status,404)

if __name__=='__main__': unittest.main()
