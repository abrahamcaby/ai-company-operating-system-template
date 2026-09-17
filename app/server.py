"""Local fictional demo only. Do not expose this impersonation interface publicly."""
import argparse
import json
import os
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse
from .service import Service, ServiceError

ROOT = Path(__file__).resolve().parents[1]

class Handler(BaseHTTPRequestHandler):
    server_version = 'CompanyOS-Demo'

    def send(self, status, body, content_type='application/json; charset=utf-8'):
        data = json.dumps(body).encode() if isinstance(body,(dict,list)) else body
        self.send_response(status)
        self.send_header('Content-Type',content_type)
        self.send_header('Content-Length',str(len(data)))
        self.send_header('Cache-Control','no-store')
        self.send_header('X-Content-Type-Options','nosniff')
        self.send_header('Referrer-Policy','no-referrer')
        self.send_header('Content-Security-Policy',"default-src 'self'; script-src 'self'; style-src 'self'; img-src 'self' data:; connect-src 'self'; frame-ancestors 'none'; base-uri 'none'; form-action 'self'")
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):
        self.handle_request('GET')

    def do_POST(self):
        self.handle_request('POST')

    def handle_request(self, method):
        try:
            host = self.headers.get('Host','')
            if urlparse('//'+host).hostname not in {'localhost','127.0.0.1','::1'}:
                raise ServiceError('This demo accepts localhost requests only.',403)
            origin = self.headers.get('Origin')
            if origin and origin != 'http://'+host:
                raise ServiceError('Cross-origin requests are disabled.',403)
            path = urlparse(self.path).path
            service = self.server.service
            if path == '/api/health' and method == 'GET':
                return self.send(200,{'status':'ok','mode':'fictional-demo'})
            if path == '/api/demo/users' and method == 'GET':
                return self.send(200,{'users':[{k:u[k] for k in ('id','name','title','department')}
                   for u in service.users.values() if u['tenant_id']=='meridian']})
            if path.startswith('/api/'):
                user = service.user(self.headers.get('X-Demo-User'))
                payload = {}
                if method == 'POST':
                    if self.headers.get('Content-Type','').split(';')[0] != 'application/json':
                        raise ServiceError('Use application/json.',415)
                    try:
                        length = int(self.headers.get('Content-Length','0'))
                    except ValueError:
                        raise ServiceError('Invalid request length.')
                    if length < 0 or length > 16384:
                        raise ServiceError('Request is too large.',413)
                    try:
                        payload = json.loads(self.rfile.read(length))
                    except (ValueError,UnicodeDecodeError):
                        raise ServiceError('Invalid JSON.')
                    if not isinstance(payload,dict):
                        raise ServiceError('Expected a JSON object.')
                if path == '/api/workspace' and method == 'GET':
                    return self.send(200,service.workspace(user))
                if path.startswith('/api/documents/') and method == 'GET':
                    return self.send(200,{'document':service.public_document(service.document(user,path.split('/')[-1]))})
                if path == '/api/ask' and method == 'POST':
                    return self.send(200,service.ask(user,payload.get('question')))
                if path == '/api/actions':
                    if method == 'GET':
                        return self.send(200,{'actions':service.list_actions(user)})
                    return self.send(201,{'action':service.propose(user,payload)})
                parts = path.split('/')
                if len(parts)==5 and parts[2]=='actions' and method=='POST':
                    return self.send(200,{'action':service.transition(user,parts[3],parts[4])})
                raise ServiceError('Resource unavailable.',404)
            files = {'/':('index.html','text/html; charset=utf-8'),
                     '/index.html':('index.html','text/html; charset=utf-8'),
                     '/app.js':('app.js','application/javascript; charset=utf-8'),
                     '/styles.css':('styles.css','text/css; charset=utf-8'),
                     '/favicon.svg':('favicon.svg','image/svg+xml')}
            if method != 'GET' or path not in files:
                raise ServiceError('Resource unavailable.',404)
            filename,content_type = files[path]
            file = ROOT/'web'/filename
            if not file.is_file():
                raise ServiceError('Resource unavailable.',404)
            self.send(200,file.read_bytes(),content_type)
        except ServiceError as error:
            self.send(error.status,{'error':str(error)})
        except Exception:
            self.send(500,{'error':'The local demo could not complete the request.'})

    def log_message(self, format, *args):
        # Never log request bodies or credentials.
        pass

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--port',type=int,default=8080)
    parser.add_argument('--host',choices=['127.0.0.1','0.0.0.0'],default='127.0.0.1')
    parser.add_argument('--database',default=str(ROOT/'.local'/'demo.sqlite3'))
    args = parser.parse_args()
    if os.environ.get('COMPANY_OS_MODE','demo') != 'demo':
        parser.error('Only fictional demo mode is implemented; production requires the documented build.')
    Path(args.database).parent.mkdir(parents=True,exist_ok=True)
    server = ThreadingHTTPServer((args.host,args.port),Handler)
    server.service = Service(args.database)
    print('Fictional Company OS demo: http://localhost:'+str(args.port),flush=True)
    print('No live tools, model calls, SSO, or customer data. Use only on your own computer.',flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
        server.service.db.close()

if __name__ == '__main__':
    main()
