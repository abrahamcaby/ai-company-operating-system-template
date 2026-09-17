# Permissions, trust and security requirements

**Status: production requirements, not a certification or completed security implementation.** The local demo's selectable fictional identities make access rules inspectable; they are not authentication. Do not expose that demo to a network or insert customer data. Passing its tests does not validate SSO, source ACL fidelity, database isolation or production operations.

## 1. Who can see what

A role controls product capabilities, such as managing a connector or approving a task. Source permissions determine access to source data. Workspace membership can further narrow access but cannot widen the source's audience. Company policy can impose additional restrictions such as business purpose, geographic restrictions or legal-entity boundaries.

```text
can_read(user, resource, context) =
  active_company_user(user)
  AND same_tenant(user, resource)
  AND resource_is_active(resource)
  AND current_access_evidence_is_complete(resource)
  AND source_effective_permission(user, resource, "read")
  AND company_policy_allows(user, resource, context)
  AND no_applicable_deny(user, resource, context)
```

Unknown is a denial. A connector's administrator token proves only that the connector can obtain the content. It does not prove that the requesting employee can read it. A CEO sees all information the organization explicitly authorizes for that person. HR investigations, private conversations, privileged legal files and restricted subsidiaries do not become visible simply because a user has an Executive role.

| Product role | May do | Does not imply |
|---|---|---|
| Employee | Search authorized knowledge, create private drafts, request approved actions | Access to every item in their department |
| Workspace steward | Curate playbooks, resolve knowledge review items, configure workspace views | Authority to override source permissions |
| Manager / executive | View authorized team or cross-company reports and approved digests | Read-all privilege or access to personal messages |
| Data owner | Approve source scope, report definitions, retention and publication for their domain | Platform administration across every domain |
| Integration administrator | Install and operate approved connections, inspect sanitized health | Browse all ingested business content |
| Security administrator | Set policy, audit decisions, revoke sessions and connections | Unrestricted content access without a separately governed support process |
| Action approver | Approve named command types within limits | Approval of different targets or payloads than the preview |

Keep duties separate where possible. Use time-limited, audited emergency access with a stated reason and customer approval for exceptional support cases. Do not ship an invisible universal support account.

## 2. Identity lifecycle

Use the customer's identity provider for login, with OIDC authorization code flow and PKCE through a maintained authentication library. Validate issuer, audience, signature, expiry, nonce and callback state. Derive tenant from a configured issuer and session, never from a client-supplied tenant field. Use secure, HTTP-only session cookies, CSRF protection for mutations and short session lifetimes appropriate to the customer's policy. [OpenID Connect specification](https://openid.net/specs/openid-connect-core-1_0.html).

Use SCIM where supported to provision/deactivate users and reconcile groups; integrate directory lifecycle events or an explicit alternative where SCIM is unavailable. Provisioning and login are separate controls. A disabled principal must be denied on every request even if an old identity token has not expired. Increment that principal's session epoch, invalidate live sessions, revoke owned jobs and re-evaluate outstanding approvals. [SCIM protocol](https://www.rfc-editor.org/info/rfc7644/).

Map source identities using source tenant plus immutable source user/group IDs, verified against the company's identity directory. Do not silently equate two users because their names match. Email changes, aliases, guest accounts, contractors and rehires require explicit lifecycle handling. Store mapping evidence and quarantine ambiguous accounts. A corporate email suffix alone never proves source access.

## 3. Revocation and freshness

Authorization is time dependent. Distinguish **known local revocation** from **an upstream change not yet observed**. No asynchronous connector can honestly promise instantaneous propagation of every source permission change.

- Once a local or observed source deny is recorded, deny the next request immediately. Publish an invalidation event and cancel affected background work.
- Give every ACL/group snapshot a configurable expiry and source revision. Expired, incomplete or unverified snapshots fail closed. The expiry must be no longer than the customer-approved maximum exposure window.
- For restricted material, require a supported live source access check immediately before retrieval/release, or exclude that source/class from the pilot. Even live checks have a small race window; document it instead of promising perfect simultaneity.
- At release, compare the resource/access revisions pinned at retrieval against current local revisions. On conflict, discard the generated response. Do not stream sensitive content before this check completes.
- If permission synchronization is degraded beyond its freshness limit, suspend affected results and explain limited coverage without exposing hidden resource names.

Suggested pilot acceptance targets are a local deny applied on the next request, identity offboarding observed within 60 seconds of a successfully received lifecycle event, and upstream ACL propagation measured against a customer-agreed target such as five minutes **only where the selected source supports it**. These are test targets, not existing service guarantees. For a connector that can only reconcile every hour, publish that limit and do not ingest data needing a five-minute contract.

## 4. Every derived surface needs authorization

Apply the same policy to document titles, counts, snippets, entity links, autocomplete, citations, screenshots, media playback, exports, chat history, audit details and saved answers. A hidden file's title can itself reveal an acquisition or employee investigation. Avoid returning restricted titles in “some results were omitted” notices.

For a compiled artifact with dependencies `D`, a reader must satisfy its own policy and `can_read(user, d)` for every `d` in `D`. Use current dependency policies, not the audience at build time. Restricted source changes invalidate the artifact. A deliberately approved publication for a broader audience is a distinct governed object with an accountable reviewer; it is not an automatic exception for summaries.

Private chat stays private by default. Sharing a conversation or exporting a report triggers an audience check over all included artifacts and source dependencies. A link recipient is reauthorized at open time. Downloaded files and sent email cannot be reliably clawed back, so apply separate export/delivery policy before producing them.

Generate scheduled briefings for each recipient's current identity and resource set. Use per-recipient cache keys including tenant, principal, permission revision, source revisions, model and prompt version. Two Sales users can have different account permissions. A cache keyed only by team, role or question is unsafe. Do not reuse another recipient's answer as context. Recheck identity and authorization when the job runs and when delivery occurs.

Approved aggregate reports need a report-specific audience policy, definition and review of inference risk. Do not infer that an aggregate is harmless because it omits names. Payroll, small cohorts and filtered customer segments can disclose underlying restricted facts. Customer policy must decide which summaries may be published independently of row access.

## 5. Storage, execution and model boundaries

| Threat | Required production control | Proof before pilot expansion |
|---|---|---|
| Cross-company data access | Dedicated customer deployment initially; tenant keys and composite foreign keys everywhere; RLS/query restrictions | Forged tenant/resource references denied across all endpoints and jobs |
| Broad integration token used as employee authority | Separate ingestion identity and runtime user policy; credential least privilege; source ACL conformance | Two employees with different source rights receive different allowed sets |
| Permission revoked while answer is being generated | Revision checks, revocation queue, final release gate, restricted streaming | Concurrent revoke prevents response release and stored-answer access |
| Prompt injection in a transcript or file | Treat retrieved text as untrusted evidence; isolate tool executor; allowlisted commands and destinations | Malicious source cannot add recipients, exfiltrate secrets or approve an action |
| Parser exploit or hostile attachment | Isolated parse workers, type/size limits, malware scanning, no privileged mounts, restricted egress | Corrupt/oversized content quarantined without affecting application workers |
| SSRF from a source URL | Provider/domain allowlists, outbound proxy, private-address blocking, redirect validation | Metadata service/local-network URLs rejected before fetching |
| Secrets or confidential prompts in logs | Secret manager, workload identities, structured redaction, payload logging disabled by default | Canary token/content absent from logs and traces |
| Unsafe generated command | Typed command schema, allowlist, preview, approval binding, execution-time authorization | Model-generated arbitrary URLs/code/SQL cannot execute |
| Replayed or duplicated work | Signed webhook validation, timestamp windows, idempotency keys, persisted state machine | Duplicate events and timeout retries produce one intended side effect |
| Stale backups resurrect deleted content | Deletion ledger, restore quarantine and replay before reopening | Restore test proves deleted content remains unreadable |

The model gateway selects only routes approved for the tenant's region, content class and purpose. Record provider/model/version, retention configuration, cost and status. Provider fallback is permitted only to a route with equal approved data-handling constraints; otherwise fail. Do not silently switch a confidential workflow to an unapproved provider after an outage.

Use company API accounts with contractual data-handling settings reviewed during procurement. Do not assume that paying for an API, a personal Codex account or a chat subscription supplies company-wide isolation, retention or confidentiality controls. The application's authorization, operational controls and customer agreement must supply those requirements.

Keep read credentials separate from optional write credentials. Action workers receive a narrowly scoped command and short-lived capability, not the entire conversation and every source token. Finance postings, external communications and destructive changes each need their own approval policy. A general “AI may act for me” setting is not sufficient for every action class.

## 6. Media and data lifecycle

Before ingesting recordings, require the customer to identify the source owner, approved collection scope, applicable recording/transcription policy, permitted purposes and retention. Store provenance and any consent/rights metadata supplied by the source. If this cannot be established, quarantine the asset. The product should support the customer's established policy rather than make a legal determination from a filename or participant list.

Transcripts, embeddings, summaries, clips, thumbnails and OCR text inherit the original asset's access and retention restrictions. Track each derivative so deletion and expiry propagate. Preserve timestamps and source version links so a statement can be checked in context. Low-confidence speaker attribution or transcription should be visible; it must not become an asserted fact about an employee.

Retention is a policy matrix by content class, source and derivative. Configure active-store deletion, index invalidation, object lifecycle, audit retention and backup expiry separately. When a hold applies, retained content remains access-restricted and unavailable to ordinary search. Restore procedures must replay deletion/hold state before opening traffic. Produce a deletion report with logical denial time, primary-store removal and backup expiry status.

## 7. Release and incident evidence

Before real customer use, collect threat model review, dependency and container scanning, secret scanning, authenticated endpoint tests, connector ACL conformance, restore exercise, model/tool adversarial tests and documented owners. Use an independent penetration test before broader enterprise rollout. These activities are work to be done; the repository does not claim SOC 2, ISO 27001, HIPAA or any other certification.

Maintain a security contact and incident process in the delivered service. A suspected disclosure triggers connection/workflow suspension, session/token revocation as applicable, preservation of minimized audit evidence, assessment of affected principals/resources and customer escalation under the agreed contract. Re-enable only after containment, access-state reconciliation and regression testing. Do not erase evidence while attempting to clean up the incident.

The operational procedures and restoration sequence are in [deployment and operations](06-deployment.md). The customer intake evidence is in [data readiness and delivery](08-data-readiness-and-delivery.md).
