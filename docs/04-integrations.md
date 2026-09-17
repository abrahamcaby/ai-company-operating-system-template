# Integration contracts and connector plan

**Status: all external connectors below are planned.** The repository's fictional connector catalog is a demonstration, not an installed integration marketplace. A company can choose equivalents from its existing stack. No claim of universal plug-and-play connectivity is made.

## 1. Connect by capability

The core product asks for capabilities such as `documents.read`, `messages.read`, `recordings.read`, `crm.query`, `projects.read`, `finance.report` and `tasks.propose`. It does not assume one brand per category. A connector advertises its supported operations, authentication modes, permission fidelity, event coverage, data residency constraints and tested versions.

| Adapter contract | Required behavior |
|---|---|
| `discover(config)` | Return accessible containers, scopes, source tenant ID, available capabilities and limitations without importing content |
| `list_resources(cursor, scope)` | Paged initial inventory with stable IDs, version evidence and resumable checkpoints |
| `get_resource(id, version?)` | Metadata, content reference, canonical URL, source timestamps, provenance and deletion state |
| `get_access(id)` | Complete inherited and direct source policy or explicit `incomplete`; never substitute the connector token's access |
| `resolve_principals(ids)` | Source user/group IDs mapped to verified company identities, including nested/external memberships |
| `check_access(subject, id, action)` | Live source authorization where supported, with permit/deny/unknown and expiry |
| `changes(cursor)` | Idempotent event envelope for update/delete/access-change; declare unavailable event types |
| `reconcile(scope)` | Authoritative inventory/access comparison to repair lost events or cursor gaps |
| `query(report_id, typed_args, subject)` | Approved structured read with result schema, freshness and source traceability |
| `propose/execute(command)` | Optional separately granted writes with exact preview, idempotency and postcondition verification |
| `disconnect()` | Revoke/forget credentials, stop jobs, tombstone the connection, invalidate derived data and run configured deletion workflow |

MCP can be an adapter transport when its server meets these contracts. It is not the permission model, sync engine or durable knowledge store. An ETL service or existing enterprise integration platform can supply ingestion, but its output must carry usable source identities, ACLs, deletion events and lineage. A flat export without these is eligible only for a deliberately approved audience with a responsible data owner.

## 2. Connector acceptance manifest

Each implementation must check in a manifest alongside its tests. The following is a **planned contract example**, not runnable connector configuration:

```yaml
kind: documents.example
contract_version: 1
implementation_status: planned
auth_modes: [delegated_oauth, application_oauth]
capabilities: [documents.read]
permission_mode: source_snapshot_with_live_check
acl_support:
  inherited: true
  groups: true
  external_guests: false
  anonymous_links: false
  missing_semantics: quarantine
changes:
  content: cursor
  deletion: cursor
  permissions: reconcile_and_live_check
data_policy:
  raw_media: disabled
  retention_profile: customer_defined
  secret_storage: reference_only
tested_source_versions: []
```

The status can advance from `planned` to `experimental` to `pilot_validated` to `supported` only with evidence. The release record must include source API version, exact OAuth scopes, subscription renewal behavior, tested account editions, ACL fixtures, performance envelope, operational owner and known exclusions.

## 3. Candidate matrix

Phase A means a candidate for the first pilot; select **one documents source, one communication source and one business system**, not every row. Phase B follows a successful pilot. Phase C requires specialist controls or customer demand. All phases still require implementation. Documentation was checked on 2026-09-17; actual tenant entitlements and scopes must be verified during onboarding. API details and limits can change.

| Category / candidates | Phase and useful data | Access design / known constraint | Backfill, updates, revocation and operating requirements |
|---|---|---|---|
| Google Drive / Docs | A: selected shared drives, files, exported document text | Preserve direct and inherited permissions, source group membership, shared-drive semantics and external guests. Domain/anyone links are not automatic company-wide grants. Prefer the least scope that covers selected content. | Establish a changes token, inventory selected scope, then replay changes. Watch notifications indicate that the change feed should be fetched. Persist versions/hash and re-read ACLs on access or hierarchy changes; reconcile permission changes independently. [Changes](https://developers.google.com/workspace/drive/api/guides/manage-changes), [sharing](https://developers.google.com/workspace/drive/api/guides/manage-sharing). |
| SharePoint / OneDrive via Microsoft Graph | A alternative: sites, drives, files | Consider Selected permissions to limit the app to approved resources. That application grant is not proof that an employee can read every item; resolve sharing, group and item inheritance separately. | Backfill with drive delta and persist the returned delta link; process deleted facets. Resync invalid delta state. Reconcile inheritance and source identity changes. Subscription and throttling behavior must be tested in the target tenant. [Delta](https://learn.microsoft.com/en-us/graph/api/driveitem-delta?view=graph-rest-1.0), [Selected permissions](https://learn.microsoft.com/en-us/graph/permissions-selected-overview). |
| Slack | A: explicitly selected channels and threads | Bot visibility differs from user membership. Respect private channels, guests, shared channels, retention and file access. Exclude DMs in the first pilot. | Cursor-paged history plus Events API; deduplicate event IDs, refetch edited/deleted items and refresh membership. Budget backfills per method/workspace and app distribution: Slack has special history/replies limits for some commercially distributed apps. Pause rather than flood retries; reconcile missed events. [Events](https://docs.slack.dev/apis/events-api/), [rate limits](https://docs.slack.dev/apis/web-api/rate-limits/). |
| Microsoft Teams | A alternative/B: approved channels and meeting context | Separate team/channel/chat membership and tenant boundaries; private/shared channels need explicit testing. Teams files have SharePoint permissions and must not inherit a guessed chat audience. | Graph change notifications cover specified resources; implement subscription creation/renewal/lifecycle recovery and independent historical reads. Validate endpoint-specific permissions/licensing before committing to transcript coverage. [Teams notifications](https://learn.microsoft.com/en-us/graph/teams-change-notification-in-microsoft-teams-overview). |
| Zoom or equivalent meeting platform | B: approved cloud recordings, transcripts, participant metadata | Admin recording access is not every employee's viewing permission. Preserve recording sharing restrictions and obtain the customer's recording/transcription policy and provenance. Meeting attendance alone is insufficient. | Backfill recording metadata in date windows, ingest approved transcript/media when ready, version replacements and tombstone deletions. Use applicable recording events and periodic reconciliation; handle expiring download links server-side. Rate limits vary by plan and request class. [Meetings API](https://developers.zoom.us/docs/api/meetings/), [rate limits](https://developers.zoom.us/docs/commerce/rate-limits/). |
| Gong or equivalent revenue intelligence | B: sales call metadata, transcript, selected recordings and CRM links | Gong documents company-level OAuth, not user-level OAuth. Implement permission profiles, call-specific sharing and hierarchy semantics separately. If the effective permission cannot be proven, exclude the call. CRM record access and call access are distinct. | Page through call inventory by time range; capture source IDs, updates, revisions and transcript timecodes. Verify event availability in the customer's plan, otherwise use overlap polling and full reconciliation. Honor documented 429/Retry-After and per-company quotas. [OAuth](https://help.gong.io/docs/create-an-app-for-gong), [permissions](https://help.gong.io/docs/available-permission-settings), [API limits/cursors](https://help.gong.io/apidocs/introduction-2). |
| Salesforce | A/B: accounts, opportunities, activities, approved reports | Use record, object and field access; sales role alone is insufficient. Favor delegated reads or tested effective-access evaluation. Omit restricted fields before indexing or generation. | Inventory chosen objects with supported REST/bulk reads; CDC/Pub/Sub where available. Persist replay checkpoints and reconcile expired gaps: documented event retention is 72 hours. Record sharing changes need their own reconciliation strategy. Pin API version and query metadata; do not assume custom fields. [Event durability](https://developer.salesforce.com/docs/platform/pub-sub-api/guide/event-message-durability.html). |
| HubSpot | A alternative/B: companies, contacts, deals, activities | OAuth object scopes can exceed a person's UI permissions. Validate team/owner/record/field restrictions in the actual account. If no reliable user-equivalent access path exists, restrict to approved report outputs or a narrower imported dataset. | Use selected object reads/search and the webhook model supported by the app version. HubSpot's documented journal/v4 subscription API is beta and is not interchangeable with v3; it uses polled journals and limited history. Record chosen API/version and reconcile lost history and merges. [Journal API](https://developers.hubspot.com/docs/api-reference/legacy/webhooks/webhooks-journal). |
| Jira Cloud | A/B: projects, issues, comments, delivery milestones | Map Browse Projects plus issue security and restricted comment visibility. Project membership is not enough. Enterprise/on-prem versions need separate adapters. | Paged issue inventory plus supported webhooks; renew expiring registrations where required. Reconcile JQL-selected scope, moves, deletions and permission schemes. Parse retry/rate-limit headers; pin endpoint version and custom-field mapping. [Webhooks](https://developer.atlassian.com/cloud/jira/platform/webhooks/), [limits](https://developer.atlassian.com/cloud/jira/platform/rate-limiting/). |
| Asana | A alternative/B: projects, tasks, milestones and comments | Respect private projects/tasks and source membership. A task in multiple projects must follow actual source access, not an invented all-project or one-project rule. | Inventory selected resources, subscribe where supported and fetch full resource after event hints. Verify signatures, monitor webhook liveness, reconcile deletions/membership and honor per-token/concurrency limits. [Webhooks](https://developers.asana.com/docs/webhooks-guide), [limits](https://developers.asana.com/docs/rate-limits). |
| QuickBooks Online | C: approved financial reports and selected read-only ledger queries | An accounting OAuth connection is not equivalent to an employee's financial entitlement. Gate approved report IDs, legal entities and output fields through a Finance-owned policy. No postings in the initial connector. | Implement supported reports/entities, webhook-assisted refresh and a reconciled read strategy after checking the live docs and sandbox. Retain entity/source versions and audit report definitions. Intuit's documentation page was reachable but its full body was not extractable in this research; event coverage, CDC windows and exact scopes remain validation tasks. [Official webhook guide](https://developer.intuit.com/app/developer/qbo/docs/develop/webhooks). |
| NetSuite / other ERP | C: approved reports, subsidiaries, transactions, inventory | Use a dedicated least-privilege integration role and finance-approved reporting contract. Enforce subsidiary, employee and field restrictions; avoid unrestricted SQL authored by the model. | Use SuiteTalk REST and parameterized approved SuiteQL reads where available. Inspect record metadata per customer, page by stable keys, use overlapping modified-time windows and periodic reconciliation. Verify concurrency/governance limits and deletion detection. [REST overview](https://docs.oracle.com/en/cloud/saas/netsuite/ns-online-help/chapter_1540391670.html), [SuiteQL](https://docs.oracle.com/en/cloud/saas/netsuite/ns-online-help/section_157909186990.html). |
| Media / DAM / object storage / approved uploads | B/C: assets, decks, recordings, images, transcripts | Keep owner, source URL, license/rights, permitted uses, consent basis, expiry and audience. A downloaded asset is not automatically licensed for broad reuse. OCR/transcripts inherit source access. | Use provider SDK/events or a signed manifest with stable IDs, versions, checksums and ACLs. Quarantine untrusted files, enforce size/type limits, capture page/timecode provenance and propagate deletion to every derivative. Build a DAM-specific adapter for its permission model. |
| Other business systems / customer API | Customer-selected | REST, GraphQL, database views, SFTP exports or an integration platform are possible transports. Require a named data owner and explicit identity, ACL, provenance and deletion semantics. | Implement the same connector contract and conformance suite. A periodic export must state its freshness ceiling. Reject unsupported access semantics rather than claim equivalent coverage. |

## 4. Shared operational behavior

Workers use per-connection queues and independent quotas. Honor `Retry-After`; use bounded exponential backoff with jitter for transient failures. Do not retry permanent auth/permission failures as ordinary network errors. Place irrecoverable payloads in a dead-letter queue with sanitized diagnostics and a replay tool.

Keep `event_id`, `source_version`, `observed_at`, `cursor` and `connection_generation` on work items. A new connection generation invalidates queued work from disconnected credentials. Webhook handlers validate provider signatures/timestamps, reject replays, acknowledge quickly and enqueue work. Never trust a webhook body as an authorization grant.

Separate queues for access revocations and large media jobs prevent a video backfill from delaying offboarding. Prioritize removal, then fresh changes, then historical backfill. Expose backlog age, last successful sync, last permission reconciliation, excluded resource count and source coverage to the administrator.

For resources with no complete permission API, choose one explicitly documented fallback: delegated live reads; customer-reviewed export into a deliberately restricted collection; or unsupported/quarantined. A broad administrator token followed by guessed team roles is not an acceptable fallback.

## 5. Conformance tests before a connector becomes supported

1. Initial backfill and resumed pagination produce the same inventory; a crash at any checkpoint loses no accepted event.
2. Duplicate/out-of-order notifications do not resurrect deleted content or overwrite a newer version.
3. Direct shares, inherited shares, nested groups, external guests, moved resources and removed members match the source's effective access.
4. Removing a user or revoking a resource prevents search, detail, snippet, answer, artifact, export and scheduled delivery access within the declared freshness contract.
5. Unknown permissions, invalid credentials and provider outages fail closed. A disconnected connector cannot continue ingesting queued content.
6. Rate-limit storms, expired cursors, webhook renewal failure and missed deletion events recover with measured bounded backlog.
7. Sensitive fields and prohibited media are absent from prompts, indexes, telemetry and unauthorized exports.
8. Connector version upgrade, schema change and rollback are tested against saved sanitized fixtures and a provider sandbox.

Store the resulting evidence with the connector release. Marketing should list the supported capability and limitations for the tested edition, not simply display the vendor's logo.
