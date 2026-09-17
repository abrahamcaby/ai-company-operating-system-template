"""Policy-enforced fictional evidence and simulated workflow service."""
import json
import re
import sqlite3
import threading
import uuid
from . import seed
from .policy import can_read, dependency_versions

PUBLIC_FIELDS = ('id','title','kind','system','summary','content','updated_at','owner',
                 'classification','tags','source_ids','source_url')

class ServiceError(Exception):
    def __init__(self, message, status=400):
        self.status = status
        super().__init__(message)

class Service:
    def __init__(self, database=':memory:'):
        self.users = seed.users()
        self.documents = seed.documents()
        self.lock = threading.RLock()
        self.db = sqlite3.connect(database, check_same_thread=False)
        self.db.row_factory = sqlite3.Row
        self.db.executescript('''
        CREATE TABLE IF NOT EXISTS actions (
          id TEXT PRIMARY KEY, tenant_id TEXT NOT NULL, document_id TEXT NOT NULL,
          kind TEXT NOT NULL, title TEXT NOT NULL, status TEXT NOT NULL,
          requested_by TEXT NOT NULL, approved_by TEXT, created_at TEXT NOT NULL,
          versions TEXT NOT NULL);
        CREATE TABLE IF NOT EXISTS audit (
          id TEXT PRIMARY KEY, tenant_id TEXT NOT NULL, actor_id TEXT NOT NULL,
          event TEXT NOT NULL, document_id TEXT, detail TEXT NOT NULL, created_at TEXT NOT NULL);
        ''')

    def user(self, user_id):
        user = self.users.get(user_id)
        if not user or not user['active']:
            raise ServiceError('Choose an active demo persona.', 401)
        return user

    def document(self, user, document_id):
        document = self.documents.get(document_id)
        if not can_read(user, document, self.documents):
            # Uniform missing/forbidden response avoids resource enumeration.
            raise ServiceError('Resource unavailable.', 404)
        return document

    def public_document(self, document):
        return {key: document[key] for key in PUBLIC_FIELDS}

    def audit(self, user, event, document_id=None, detail=''):
        self.db.execute('INSERT INTO audit VALUES (?,?,?,?,?,?,?)',
            (str(uuid.uuid4()),user['tenant_id'],user['id'],event,document_id,detail,seed.iso_now()))
        self.db.commit()

    def workspace(self, user):
        with self.lock:
            docs = [self.public_document(d) for d in self.documents.values() if can_read(user,d,self.documents)]
            activities = []
            for row in self.db.execute('SELECT * FROM audit WHERE tenant_id=? AND actor_id=? ORDER BY created_at DESC LIMIT 20',
                                       (user['tenant_id'],user['id'])):
                if row['document_id'] and not can_read(user,self.documents.get(row['document_id']),self.documents):
                    continue
                activities.append({k:row[k] for k in ('id','event','detail','created_at')})
            return dict(user={k:user[k] for k in ('id','name','title','department')},
                documents=docs,connections=seed.CONNECTIONS,activities=activities,
                permissions={k:user[k] for k in ('can_propose','can_approve','can_admin')},mode='fictional-demo')

    def ask(self, user, question):
        if not isinstance(question,str) or not 1 <= len(question.strip()) <= 2000:
            raise ServiceError('Enter a question between 1 and 2,000 characters.')
        stop = {'what','when','where','with','that','this','have','does','from','about','which','tell','company','show','please','their','would','could','should','your','the','and','for','are','our','can','how'}
        words = set(re.findall(r'[a-z0-9]+',question.lower()))-stop
        with self.lock:
            # Authorization happens BEFORE ranking, snippet creation or evidence assembly.
            candidates = [d for d in self.documents.values() if can_read(user,d,self.documents)]
            ranked = []
            for d in candidates:
                body = set(re.findall(r'[a-z0-9]+',' '.join([d['title'],d['content']]+d['tags']).lower()))
                score = len(words & body)
                if score:
                    ranked.append((score,d))
            ranked.sort(key=lambda pair:(-pair[0],pair[1]['id']))
            matched = [d for _,d in ranked[:3]]
            self.audit(user,'Evidence search',detail='Searched currently authorized fictional evidence.')
            return dict(answer=('Evidence preview from your accessible sources:\n\n'+'\n\n'.join(d['content'] for d in matched))
                 if matched else 'No matching evidence is available in your accessible demo sources. Try “Atlas renewal”, “onboarding pilot”, or “cash”.',
                 citations=[{k:d[k] for k in ('id','title','system')} for d in matched],mode='extractive-demo')

    def list_actions(self, user):
        with self.lock:
            rows = self.db.execute('SELECT * FROM actions WHERE tenant_id=? ORDER BY created_at DESC',(user['tenant_id'],)).fetchall()
            return [self.public_action(row) for row in rows if can_read(user,self.documents.get(row['document_id']),self.documents)
                    and (row['requested_by']==user['id'] or user['can_approve'])]

    def public_action(self, row):
        return {k:row[k] for k in ('id','title','status','kind','document_id','requested_by','approved_by','created_at')}

    def propose(self,user,payload):
        if not user['can_propose']:
            raise ServiceError('This persona cannot propose actions.',403)
        if payload.get('kind') != 'create_task':
            raise ServiceError('Only the simulated create_task capability is available.')
        title = payload.get('title')
        if not isinstance(title,str) or not 1 <= len(title.strip()) <= 200:
            raise ServiceError('A task title between 1 and 200 characters is required.')
        document_id = payload.get('document_id')
        if not isinstance(document_id,str):
            raise ServiceError('Select a source document.')
        with self.lock:
            document = self.document(user,document_id)
            action_id = str(uuid.uuid4())
            self.db.execute('INSERT INTO actions VALUES (?,?,?,?,?,?,?,?,?,?)',
                (action_id,user['tenant_id'],document_id,'create_task',title.strip(),'proposed',user['id'],None,
                 seed.iso_now(),json.dumps(dependency_versions(document,self.documents),sort_keys=True)))
            self.audit(user,'Action proposed',document_id,'A simulated task is waiting for a separate reviewer.')
            return self.public_action(self.db.execute('SELECT * FROM actions WHERE id=?',(action_id,)).fetchone())

    def transition(self,user,action_id,operation):
        with self.lock:
            row = self.db.execute('SELECT * FROM actions WHERE id=? AND tenant_id=?',(action_id,user['tenant_id'])).fetchone()
            if not row:
                raise ServiceError('Resource unavailable.',404)
            document = self.document(user,row['document_id'])
            if not user['can_approve']:
                raise ServiceError('This persona cannot review actions.',403)
            requester = self.users.get(row['requested_by'])
            if not can_read(requester,document,self.documents) or not requester.get('can_propose'):
                raise ServiceError('Requester access changed. Create a new proposal.',409)
            if dependency_versions(document,self.documents) != json.loads(row['versions']):
                raise ServiceError('Source evidence changed. Create a new proposal.',409)
            if operation == 'approve':
                if row['requested_by'] == user['id']:
                    raise ServiceError('A different authorized person must approve this proposal.',403)
                if row['status'] != 'proposed':
                    raise ServiceError('Only proposed actions can be approved.',409)
                self.db.execute('UPDATE actions SET status=?, approved_by=? WHERE id=?',('approved',user['id'],action_id))
                detail = 'A separate authorized reviewer approved the simulation.'
            elif operation == 'execute':
                if row['approved_by'] != user['id']:
                    raise ServiceError('Only the recorded reviewer can run this simulation.',403)
                if row['status'] == 'simulated':
                    return self.public_action(row)  # idempotent replay; no duplicated action
                if row['status'] != 'approved':
                    raise ServiceError('Approval is required first.',409)
                self.db.execute('UPDATE actions SET status=? WHERE id=?',('simulated',action_id))
                detail = 'Simulation completed. No external system was changed.'
            else:
                raise ServiceError('Unknown action operation.',404)
            self.audit(user,'Action '+operation,document['id'],detail)
            return self.public_action(self.db.execute('SELECT * FROM actions WHERE id=?',(action_id,)).fetchone())
