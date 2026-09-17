"""Fictional demonstration data. Never place customer exports in this file."""
from datetime import datetime, timedelta, timezone

TENANT = 'meridian'

def iso_now():
    return datetime.now(timezone.utc).isoformat()

def users():
    definitions = [
        ('ceo', 'Alex Morgan', 'Chief executive', 'Leadership', ['executive','sales','finance','ops','cs','marketing'], True),
        ('sales', 'Jordan Lee', 'Account executive', 'Sales', ['sales'], False),
        ('finance', 'Sam Rivera', 'Finance director', 'Finance', ['finance'], True),
        ('people', 'Casey Brooks', 'People partner', 'People', ['people'], False),
        ('it', 'Taylor Chen', 'IT administrator', 'IT', ['it'], False),
        ('employee', 'Jamie Park', 'Team member', 'Company', [], False),
        ('ops', 'Avery Patel', 'Operations lead', 'Operations', ['ops','cs'], True),
        ('cs', 'Riley James', 'Customer success manager', 'Customer success', ['cs','sales'], False),
        ('marketing', 'Robin Ellis', 'Marketing lead', 'Marketing', ['marketing'], False),
    ]
    result = {}
    for uid, name, title, department, groups, approve in definitions:
        result[uid] = dict(id=uid, name=name, title=title, department=department,
            tenant_id=TENANT, groups=['company']+groups, active=True,
            can_propose=uid != 'it', can_approve=approve, can_admin=uid == 'it')
    result['outside'] = dict(id='outside',name='Other tenant',title='Test fixture',department='Other',
        tenant_id='other',groups=['company','finance','sales'],active=True,
        can_propose=True,can_approve=True,can_admin=False)
    return result

def documents():
    freshness = (datetime.now(timezone.utc)+timedelta(days=3650)).isoformat()
    rows = [
      ('strategy', 'Company priorities · Q3', 'Company wiki', 'File workspace', 'company',
       'Deliver dependable implementations and make customer handoffs easier.',
       'Our three priorities are dependable implementations, faster customer handoffs, and clear operating ownership. Every project needs an accountable owner and a current decision log.',
       'Leadership', ['strategy','goals','priorities'], []),
      ('all-hands', 'Company all-hands · September', 'Meeting', 'Meeting platform', 'company',
       'The all-hands confirms an October onboarding pilot.',
       'The company all-hands confirmed an October onboarding pilot. Operations owns the rollout. The open issue is the support handoff checklist. The next decision review is September 24. Recording reference: 12:40–14:10; fictional transcript.',
       'Operations', ['meeting','pilot','onboarding'], []),
      ('handbook', 'How we make decisions', 'File', 'File workspace', 'company',
       'Document the decision, owner, rationale, and review date.',
       'Record decisions in the shared project log. Include the accountable owner, supporting evidence, rationale, and review date. Confidential decisions belong in a restricted workspace.',
       'Operations', ['policy','decisions','onboarding'], []),
      ('deal', 'Atlas renewal · CRM record', 'CRM', 'CRM', 'sales',
       'Atlas has a renewal review on September 30; security review is still open.',
       'Atlas renewal is in review. The customer requested a security addendum before September 30. Jordan owns the next step. CRM amount: USD 180,000 annual contract value. This is a fictional snapshot, not a live forecast.',
       'Sales', ['atlas','renewal','pipeline','customer'], []),
      ('call', 'Atlas customer call · Evidence', 'Recording', 'Sales recording platform', 'sales',
       'The buyer wants a named implementation owner before renewal.',
       'At 08:12 in this fictional call, the buyer requests a named implementation owner. At 14:36 they ask for the security addendum. Treat these as customer requests, not accepted contractual commitments.',
       'Sales', ['atlas','renewal','recording','security'], []),
      ('handoff', 'Atlas implementation handoff', 'Project', 'Project management', 'cs',
       'Customer success is preparing the implementation checklist.',
       'Atlas onboarding needs an implementation owner, security addendum, and customer kickoff. Operations and Customer Success will agree ownership at the September 24 review.',
       'Customer success', ['atlas','onboarding','project','handoff'], []),
      ('atlas-brief', 'Atlas account brief · Compiled', 'Compiled brief', 'Company OS', 'company',
       'CRM, call evidence, and the handoff plan are linked in one account brief.',
       'Atlas renewal depends on a security addendum and a named implementation owner. This compiled page combines the CRM record, call transcript, and handoff plan. Its audience is the intersection of all three source audiences.',
       'Customer success', ['atlas','renewal','compiled'], ['deal','call','handoff']),
      ('cash', 'Cash and receivables · Approved snapshot', 'Finance', 'Accounting', 'finance',
       'Approved illustrative cash snapshot with USD, period, and entity recorded.',
       'Meridian Works US, USD, as of September 15, 2026: bank cash 2,400,000; open accounts receivable 620,000. These are fictional approved report values. Use the accounting report for actual balances. Revenue recognition and cash are different measures.',
       'Finance', ['cash','receivables','finance','bookkeeping'], []),
      ('board', 'Operating review · Leadership', 'Compiled brief', 'Company OS', 'executive',
       'Leadership review joins strategy, renewal posture, and approved finance data.',
       'Leadership should review the Atlas renewal dependency alongside the approved finance snapshot. The operational priority remains the October onboarding pilot. This is a fictional compiled briefing, not an automatically reconciled report.',
       'Leadership', ['leadership','review','atlas','finance'], ['strategy','deal','cash']),
      ('people-private', 'Restricted employee case', 'People', 'People system', 'people',
       'Confidential People case for the assigned People team.',
       'Synthetic confidential employee case. Case identifier PEOPLE-DEMO-42. This resource must never appear in CEO, Sales, Finance, employee, or IT results.',
       'People', ['people','private'], []),
      ('campaign', 'Customer education campaign', 'Media', 'Media library', 'marketing',
       'Campaign assets are cleared for the customer education launch.',
       'The customer education campaign includes an approved explainer video and a product guide. Only licensed assets cleared by Marketing may be reused. Raw customer recordings require separate consent and access.',
       'Marketing', ['campaign','media','video'], []),
      ('project', 'Onboarding pilot · Delivery plan', 'Project', 'Project management', 'ops',
       'Operations owns the October pilot and support handoff checklist.',
       'Operations owns the October onboarding pilot. Avery is accountable for the support handoff checklist. The next milestone is a September 24 readiness review.',
       'Operations', ['project','onboarding','pilot','delivery'], []),
      ('it-guide', 'Connector operations runbook', 'File', 'IT workspace', 'it',
       'Connection owners monitor sync freshness, scope, and revocation.',
       'Every connector needs a service owner, approved scope, identity mapping, reconciliation job, and revocation procedure. IT access to connector configuration does not grant access to the connected business content.',
       'IT', ['connector','permissions','sync'], []),
    ]
    result = {}
    for uid,title,kind,system,group,summary,content,owner,tags,sources in rows:
        result[uid] = dict(id=uid,tenant_id=TENANT,title=title,kind=kind,system=system,
          summary=summary,content=content,owner=owner,tags=tags,source_ids=sources,
          source_url='/?document='+uid,updated_at='2026-09-16T14:00:00Z',
          classification='Company' if group=='company' and not sources else 'Restricted',
          allow=['group:'+group],deny=[],deleted=False,acl_valid_until=freshness,version=1)
    return result

CONNECTIONS = [
    dict(id=uid,name=name,category=category,status='Planned adapter',description=description)
    for uid,name,category,description in [
      ('communication','Slack / Microsoft Teams','Communication','Channels, threads, membership, and source links.'),
      ('files','Google Drive / SharePoint / Box','Company files','Documents, versions, folders, and inherited access.'),
      ('meetings','Zoom / Teams / Google Meet','Meetings','Recordings and transcripts with attendee and source permissions.'),
      ('calls','Gong / recording providers','Sales recordings','Call evidence with speaker labels and time references.'),
      ('crm','Salesforce / HubSpot','CRM','Accounts, contacts, opportunities, and field-level policy.'),
      ('projects','Jira / Asana / ClickUp','Project management','Projects, work items, owners, and dependencies.'),
      ('books','QuickBooks / NetSuite / Xero','Accounting','Approved structured reports, entities, periods, and currency.'),
      ('people','HRIS / people systems','People','Separate restricted domain; selected policies and approved records.'),
      ('media','Object storage / DAM','Media','Rights, transcript/OCR derivatives, ownership, and retention.'),
      ('identity','Entra ID / Okta / OIDC provider','Identity','Verified sign-in, groups, lifecycle, and provisioning.'),
      ('custom','Custom API / governed import','Extension','Implement the connector contract for another source system.')
    ]
]
