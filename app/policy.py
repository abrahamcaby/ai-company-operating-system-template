"""Default-deny reference policy. Never treat UI role labels as authorization."""
from datetime import datetime, timezone


def can_read(user, document, documents, visited=None):
    if not isinstance(user,dict) or not isinstance(document,dict) or not isinstance(documents,dict):
        return False
    if not user.get('active') or not isinstance(user.get('id'),str) or not isinstance(document.get('id'),str):
        return False
    for field in ('allow','deny','source_ids'):
        value=document.get(field,[])
        if not isinstance(value,list) or any(not isinstance(item,str) for item in value):
            return False
    if not isinstance(user.get('groups'),list) or any(not isinstance(g,str) for g in user['groups']):
        return False
    if not user.get('tenant_id') or not document.get('tenant_id'):
        return False
    if user['tenant_id'] != document['tenant_id'] or document.get('deleted'):
        return False
    try:
        expiry = datetime.fromisoformat(document['acl_valid_until'].replace('Z','+00:00'))
        if expiry.tzinfo is None or expiry <= datetime.now(timezone.utc):
            return False
    except (KeyError, ValueError, TypeError, AttributeError):
        return False
    principals = {'user:'+user['id']} | {'group:'+g for g in user['groups']}
    if principals.intersection(document.get('deny', [])):
        return False
    if not principals.intersection(document.get('allow', [])):
        return False
    visited = set() if visited is None else set(visited)
    if document['id'] in visited:  # corrupt/cyclic lineage is not evidence of permission
        return False
    visited.add(document['id'])
    return all(can_read(user, documents.get(sid), documents, visited) for sid in document.get('source_ids', []))


def dependency_versions(document, documents, visited=None):
    visited = set() if visited is None else set(visited)
    if document['id'] in visited:
        raise ValueError('Cyclic lineage')
    visited.add(document['id'])
    result = {document['id']: document['version']}
    for source_id in document.get('source_ids', []):
        result.update(dependency_versions(documents[source_id], documents, visited))
    return result
