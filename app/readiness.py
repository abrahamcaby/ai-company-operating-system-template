"""Validate a local onboarding manifest without connecting to or uploading data.

This checks declared evidence and shape, not whether a permission or consent is true.
"""
import argparse
import json
from datetime import datetime, timezone
from pathlib import Path


def validate(manifest):
    errors=[]
    if not isinstance(manifest,dict):
        return ['Manifest must be an object.']
    for key in ('tenant_id','business_owner','technical_owner','identity_provider','retention_policy'):
        if not isinstance(manifest.get(key),str) or not manifest[key].strip():
            errors.append('Missing '+key)
    connections=manifest.get('connections',[])
    if not isinstance(connections,list) or not connections:
        return errors+['At least one connection is required.']
    seen=set()
    by_connection={}
    for n,c in enumerate(connections):
        prefix='connections['+str(n)+']'
        if not isinstance(c,dict):
            errors.append(prefix+' must be an object'); continue
        for key in ('id','system','owner','source_of_truth_for','access_model','revocation_procedure','capture_method'):
            if not isinstance(c.get(key),str) or not c[key].strip():
                errors.append(prefix+' missing '+key)
        if not isinstance(c.get('id'),str) or c.get('id') in seen:
            errors.append(prefix+' requires a unique string id')
        else:
            seen.add(c['id'])
            by_connection[c['id']]=c
        if c.get('access_model') not in ('source_acl','approved_audience'):
            errors.append(prefix+' access_model must be source_acl or approved_audience')
        if not isinstance(c.get('identity_mapping_verified'),bool) or c['identity_mapping_verified'] is not True:
            errors.append(prefix+' identity mapping has not been verified')
        if c.get('sample_access_test') != 'passed':
            errors.append(prefix+' sample allow/deny access test is not passed')
        if c.get('revocation_test') != 'passed':
            errors.append(prefix+' revocation test is not passed')
        if c.get('capture_method') == 'recording' and (not isinstance(c.get('recording_policy_reference'),str) or not c['recording_policy_reference'].strip()):
            errors.append(prefix+' recording requires a nonempty string policy reference')
    records=manifest.get('sample_records',[])
    if not isinstance(records,list) or not records:
        return errors+['At least one representative sample record is required.']
    ids=set()
    for n,r in enumerate(records):
        prefix='sample_records['+str(n)+']'
        if not isinstance(r,dict):
            errors.append(prefix+' must be an object'); continue
        for key in ('id','connection_id','source_id','source_url','owner','version','updated_at','classification','kind','readable_text_reference'):
            if not isinstance(r.get(key),str) or not r[key].strip():
                errors.append(prefix+' missing '+key)
        if not isinstance(r.get('id'),str) or r.get('id') in ids:
            errors.append(prefix+' requires a unique string id')
        else:
            ids.add(r['id'])
        try:
            updated=datetime.fromisoformat(r['updated_at'].replace('Z','+00:00'))
            if updated.tzinfo is None:
                errors.append(prefix+' updated_at requires a timezone')
        except (KeyError,TypeError,ValueError,AttributeError):
            errors.append(prefix+' valid updated_at timestamp required')
        if r.get('tenant_id') != manifest.get('tenant_id'):
            errors.append(prefix+' tenant mismatch')
        if not isinstance(r.get('connection_id'),str) or r.get('connection_id') not in seen:
            errors.append(prefix+' unknown connection')
        if not isinstance(r.get('allow_principals'),list) or not r['allow_principals']:
            errors.append(prefix+' explicit access principals required')
        elif any(not isinstance(p,str) or not p.startswith(('user:','group:')) or len(p.split(':',1)[1])==0 for p in r['allow_principals']):
            errors.append(prefix+' invalid principal format')
        try:
            expires=datetime.fromisoformat(r['acl_valid_until'].replace('Z','+00:00'))
            if expires.tzinfo is None or expires <= datetime.now(timezone.utc):
                errors.append(prefix+' access snapshot expired or has no timezone')
        except (KeyError,TypeError,ValueError,AttributeError):
            errors.append(prefix+' valid acl_valid_until required')
        connection_id=r.get('connection_id')
        recording=isinstance(connection_id,str) and by_connection.get(connection_id,{}).get('capture_method')=='recording'
        if recording and r.get('kind') not in ('customer_call','internal_meeting','media_asset'):
            errors.append(prefix+' recording connection requires a recording-compatible kind')
        if recording or r.get('kind') == 'customer_call':
            required=['recording_policy_reference','transcript_reference']
            if r.get('kind') in ('customer_call','internal_meeting'):
                required.append('meeting_id')
            if r.get('kind') == 'customer_call':
                required.append('account_id')
            for key in required:
                if not isinstance(r.get(key),str) or not r[key].strip():
                    errors.append(prefix+' call missing '+key)
            if r.get('speaker_and_timestamp_review') != 'passed':
                errors.append(prefix+' call speaker/timestamp review is not passed')
    return errors


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('manifest',type=Path)
    args=parser.parse_args()
    try:
        errors=validate(json.loads(args.manifest.read_text()))
    except (OSError,ValueError) as error:
        print(json.dumps({'status':'invalid','errors':[str(error)]},indent=2))
        raise SystemExit(1)
    print(json.dumps({'status':'needs-work' if errors else 'declarations-complete',
      'note':'Checks declarations only. This is not verification of real permissions, consent, connectivity, compliance, or production readiness.',
      'errors':errors},indent=2))
    raise SystemExit(1 if errors else 0)

if __name__=='__main__': main()
