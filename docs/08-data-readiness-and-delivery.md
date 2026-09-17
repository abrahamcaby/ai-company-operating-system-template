# Getting a company's data, recordings, and delivery process ready

This is an implementation playbook for turning scattered company information into a controlled pilot. The repository's current application uses fictional data, keyword evidence queries, and a simulated task workflow. It does not record calls, ingest production exports, connect to business systems, or call an LLM. The steps below describe work that must be completed for a real customer deployment.

The implementation has two deliverables: a functioning company service and a repeatable operating process that keeps its information usable. Deploying an interface alone does not complete either one.

Before data intake, use [tools, APIs and subscriptions](12-tools-apis-and-subscriptions.md) to assign account/API owners, [deployment paths](13-deployment-paths.md) to choose a starting environment, and [storage and lifecycle](14-data-storage-and-lifecycle.md) to approve retention and saved-suggestion behavior.

## Start with the included templates

Use the [system inventory](../examples/system-inventory.csv) for the source assessment, the [context intake](../examples/context-intake.md) for owner interviews, and the [readiness manifest](../examples/readiness-manifest.json) as an example of recorded declarations. Copy templates into the customer's approved private workspace before filling in real details. Keep raw documents, recordings, transcripts, customer manifests, and credentials out of this public software repository.

From the repository root, run the fictional manifest check:

```sh
python3 -m app.readiness examples/readiness-manifest.json
```

The example returns `declarations-complete`. This means required declarations and their basic shape pass the local checker. It does **not** verify actual permissions, recording consent, connected services, transcript content, or production readiness. Values such as `"passed"` are declarations that a responsible person must substantiate elsewhere. The fictional 2099 access-expiry date is a sample convenience, not an operational setting.

For a customer's private manifest, pass its approved local file path to the same command. The checker reads that JSON file locally; it does not upload it, open linked evidence, ingest source content, or capture a call. Do not mark missing tests as passed merely to make the command succeed. The evidence-based scorecard below remains the go/no-go process.

## 1. Start with a working question and a source inventory

At kickoff, select one cross-team outcome and three questions that expose the needed information. A useful initial outcome is “sales and delivery agree on customer commitments before kickoff.” Example questions are: What did this customer request? What did we actually agree to deliver? Who owns the unresolved next steps? Use the [roadmap's scoped pilot](07-roadmap-and-economics.md) to select one document source, one communications source, and one business system initially; defer other inventory entries.

Ask the customer to nominate an executive sponsor, implementation owner, identity administrator, source-system owners, and two pilot-team champions. Record where each decision is made and who can approve access. These roles may share people; the responsibilities must still be explicit.

Complete one inventory row for every candidate source, including systems that will be excluded:

| Field | Example / purpose |
| --- | --- |
| Business domain and source | Customer commitments; CRM, calls, contract folder, project board |
| Authoritative record | CRM owns account identity; approved contract owns contractual scope; project board owns delivery status |
| Business owner and technical owner | Sales Operations and CRM administrator; include named backups |
| Pilot scope | Specific accounts, teams, folders, projects, channels, meeting types, and time range |
| Stable identifiers | Source tenant ID, record ID, meeting ID, account ID, opportunity ID, project ID |
| Access model | Users, groups, inherited permissions, restricted fields, external sharing, exceptional cases |
| Available access route | Supported API, approved export, webhook/change feed, permitted polling; capability still to verify |
| Change and removal behavior | Update versions, deletion notices, permission changes, reconciliation frequency |
| Content characteristics | Languages, file types, scanned pages, media hours, transcript availability, typical sizes |
| Freshness requirement | Proposed maximum age by use case; urgent status and reference policy need different limits |
| Processing and retention | Approved storage region, permitted processors, expiration rule, hold/deletion owner |
| Current gap and next action | No transcripts; enable pilot capture and validate one permitted call |

Do not select an authoritative source by whichever export arrived last. Write down disputed definitions and have the domain owner resolve them. A customer's verbal request, a salesperson's note, and an accepted contract clause are different kinds of evidence.

Begin with a small, representative sample, for example ten permitted customer calls, five account records, their relevant project records, and a few approved company policies. This is a proposed sample, not a universal minimum. Include a restricted item, a deleted item, an access change, an ambiguous account name, and an incomplete transcript so the pilot exercises failure cases.

## 2. Make customer calls available

Use an existing approved meeting or sales-recording product where possible. The company needs a host workflow and storage owner before it needs a custom recording bot. A meeting calendar invitation does not prove a call was captured, and a recording does not prove a usable transcript exists.

### Choose and validate one capture route

| Route | Setup to perform in the customer's environment | Evidence to hand to ingestion |
| --- | --- | --- |
| Zoom cloud recording | Verify the pilot host's entitlement and admin policy. Enable cloud recording and its audio-transcript setting for the approved scope. Run a permitted test meeting and wait for the transcript to finish. | Original recording ID/link, separate transcript artifact, host, participants where permitted, meeting time, actual source permissions |
| Microsoft Teams | Verify recording/transcription policy and host permissions. Start recording through the meeting controls and verify that transcription is available for the meeting. Locate the finished artifacts in the appropriate OneDrive/SharePoint location. | Meeting and storage item identifiers, recording/transcript references, organizer, actual file permissions, expiry |
| Google Meet | Verify an eligible Workspace edition, admin settings, and host controls. Start transcription and recording as required; check the resulting meeting artifacts rather than relying on captions alone. | Calendar/meeting identifiers, organizer, Drive recording/transcript references, actual file permissions |
| Existing sales-recording platform | If the customer already licenses one, have its administrator confirm which calls, transcripts, speakers, links, account associations, and access changes are available under the approved API/export entitlement. Test that route before adding another recorder. | Source call ID, complete transcript, permitted metadata, account association, source link and access evidence |
| Manual export pilot | The authorized owner exports a transcript and metadata into an approved private staging location. Keep the source ID, permissions, and retention attached. If only media exists, use an approved transcription process with the same restrictions. | Export manifest, original source reference/version, transcript, access snapshot and expiry, responsible uploader |

Zoom documents a separate VTT transcript for qualifying cloud recordings and distinguishes that feature from local recordings. The current help page lists cloud transcription requirements and language limitations; validate them for the pilot rather than assuming every host and language is supported. [Zoom cloud transcription settings](https://support.zoom.com/hc/en/article?id=zm_kb&sysparm_article=KB0065911)

Teams exposes recording under the meeting's recording/transcription controls; recordings use OneDrive or SharePoint, with location and permissions depending on the meeting type. The adapter must read the resulting storage permissions instead of inferring access from attendees alone. [Teams recording controls](https://support.microsoft.com/en-us/teams/meetings/start-stop-and-find-meeting-recordings-in-microsoft-teams), [Microsoft storage and permissions](https://learn.microsoft.com/en-us/microsoftteams/tmr-meeting-recording-change)

Google Meet documents separate transcription controls, eligible editions, and saved artifacts in the organizer's Drive. Its documentation now describes meeting-specific folders under “Google Meet”; identify artifacts by provider IDs rather than a hardcoded folder name. [Google Meet transcripts](https://support.google.com/meet/answer/12849897?hl=en), [Google Meet recordings](https://support.google.com/meet/answer/9308681?hl=en-GB)

These platform details were checked on September 17, 2026. The descriptions above are intentionally narrow; exact product entitlements and tenant settings require verification during installation. A commercial recording platform is optional. A governed manual transcript import can prove the first workflow while an adapter is built, but manual snapshots require explicit access expiry and revalidation.

### Define the company's recording procedure

The customer's designated policy owner decides the permitted meeting types, notice/consent process, prohibited capture situations, participant objection process, retention, access, and approved transcription processors. Configure and document that decision before the pilot. Platform notifications are not a substitute for the customer's requirements. This playbook specifies an operational process; it does not determine what recording is legally permitted in any jurisdiction.

The host checks the procedure before capture, uses the approved participant notice, and follows the agreed process if someone declines or sensitive material arises. If recording is inappropriate, use an authorized written meeting note marked as a human summary. Do not invent a transcript or bypass a disabled recording feature. Record the policy reference and available notice/consent evidence; do not have an LLM infer permission from silence.

Separate permission to retain a call for internal work from permission to reuse its content in marketing. A product demo, customer quotation, raw recording, and published testimonial can have different approved audiences and uses.

### Normalize a call into useful evidence

For each call, retain the original source and version; create a normalized transcript with segment start/end times, speaker labels, text, language, and parsing confidence where available. Keep uncertain speaker attribution explicitly unknown. Do not assign a person's identity from a name guess.

Associate the call with an account, opportunity, project, and meeting series using source identifiers or an owner-confirmed match. Domain matching can propose a candidate; it must not merge separate subsidiaries, agencies, or customers merely because they share a name. Store the mapping decision and its author. Leave unmatched calls in a review queue.

The call reviewer checks the opening, a middle sample, the closing, and every material extracted commitment against the source. Check names, numbers, dates, speaker switches, gaps, and time offsets. Preserve the original transcript and record corrections as a new version. Verify that evidence links open the permitted recording near the referenced segment; if deep linking is unavailable, show the source link and timecode without pretending it is a working playback link.

Extract four distinct outputs: customer requests, accepted decisions, proposed actions, and unresolved questions. Each item has evidence and a review state. “We would like delivery in October” is a request until someone with authority accepts it. Recording ingestion must not automatically create contractual commitments or send a follow-up message.

## 3. Give all sources a common contract

Use a versioned normalization schema, not an unstructured folder of text. All records need tenant/source identity, stable IDs, original location, owner, timestamps, classification, source permission evidence, and retention behavior. The example below is a proposed ingestion envelope, not a currently supported upload endpoint. Values and links are fictional.

```json
{
  "schema_version": "1.0",
  "tenant_id": "meridian",
  "source": {
    "system": "approved-meeting-provider",
    "connection_id": "pilot-meetings",
    "record_id": "meeting-2041",
    "artifact_id": "transcript-2041-v2",
    "version": "2",
    "url": "https://example.invalid/meetings/2041",
    "observed_at": "2026-09-17T16:00:00Z"
  },
  "kind": "meeting_transcript",
  "title": "Atlas renewal review",
  "owner_principal_id": "user:jordan",
  "occurred_at": "2026-09-16T15:00:00Z",
  "language": "en",
  "entity_links": [
    {"type": "account", "system": "crm", "id": "acct-atlas-001", "match": "owner_confirmed"},
    {"type": "opportunity", "system": "crm", "id": "opp-2026-091", "match": "source_link"}
  ],
  "access": {
    "classification": "restricted",
    "source_acl_version": "acl-19",
    "allow_principals": ["group:atlas-account-team"],
    "deny_principals": [],
    "verified_at": "2026-09-17T16:00:00Z",
    "valid_until": "2026-09-17T17:00:00Z"
  },
  "capture": {
    "policy_id": "customer-call-policy-v3",
    "authorization_evidence_ref": "private-audit-record-2041"
  },
  "retention": {
    "policy_id": "customer-calls-v2",
    "delete_after": "2026-12-15T15:00:00Z",
    "hold": false
  },
  "segments": [
    {"start_ms": 492000, "end_ms": 505000, "speaker_id": "speaker-2", "text": "Please confirm our implementation owner before renewal."}
  ],
  "quality": {"state": "reviewed", "reviewer_id": "user:jordan", "known_gaps": []}
}
```

The one-hour access expiry and retention date are examples, not recommended defaults. Set them through the customer's accepted freshness, access, and retention design. Hold flags come from authorized records-management processes. A matching JSON shape does not prove that an uploader has the authority to set its permissions.

An adapter must authenticate the source, map source users/groups to company identities, verify scope, and enforce the resulting policy. Unmapped or unverifiable permissions fail closed. Upserts use tenant, connection, record, artifact, and source version for duplicate control. Preserve source timestamps separately from ingestion timestamps. Treat moved, deleted, inaccessible, and temporarily unavailable records as distinct states; a temporary network failure is not evidence of deletion.

Retain originals only in the approved private data plane. Store derived chunks, summaries, indexes, and relationship edges with their dependency IDs. A permission change or deletion must invalidate affected derivatives. GitHub contains software, fictional fixtures, documentation, and empty templates; it is not the customer-data staging area.

## 4. Turn collected data into readable company context

Give users several predictable entry points rather than a wall of transcript files:

| Collection | Standard page contents | Accountable owner |
| --- | --- | --- |
| Company | Purpose, products, approved strategy, decision process, current priorities, terminology | Executive sponsor / Operations |
| Team | Responsibilities, contacts, tools, process, current goals, escalation route | Team lead |
| Account | Stable CRM link, participants, approved relationship context, open requests, commitments, evidence | Account owner |
| Project | Scope, owners, milestones, decisions, blockers, related account and meeting links | Project manager |
| Meetings and calls | Date, purpose, participants as permitted, transcript references, reviewed decisions and actions | Meeting owner |
| Policies and procedures | Effective version, owner, audience, exceptions, review date, authoritative file | Policy owner |
| Metrics and finance | Definition, period, currency/entity, reporting source, calculation reference, approved commentary | Finance / metric owner |
| Media | Original asset, approved uses, owner, rights/expiry, transcript or OCR where permitted | Asset owner |

Each page shows its status, owner, last reviewed time, source links, and known gaps. Search should make it clear whether a result is an original record, a draft synthesis, or approved guidance. A readable summary does not replace the evidence. Preserve conflicting statements and their dates until an owner resolves the conflict; do not average competing policies or quietly choose the newer conversation.

Create an owner interview queue for missing context. Ask one concrete question at a time: Which system owns this number? What does “implementation complete” mean? Who can approve a discount? Which handoff failure keeps recurring? What changed since this process document was approved? Save the owner's answer with the question, date, audience, and evidence references. Proposed ideas remain drafts; confirmed facts go to the appropriate owned page after review.

This is the practical way to capture expertise that has never been documented. It also avoids assuming that connecting more tools automatically creates a coherent account of how the business works. Employees need a simple correction route and owners need a manageable review queue.

## 5. Deliver the customer implementation as a project

| Stage | Work to complete | Reviewable exit artifact |
| --- | --- | --- |
| Discovery and scope | Confirm outcomes, pilot users, source inventory, risks, baseline measures, excluded domains, responsibilities | Signed pilot scope and source-owner list |
| Access and data preparation | Set up company identity, approved app registrations, permitted capture, source samples, stable mappings, context interviews | Access matrix, capture runbook, sample manifest, gap register |
| Installation and first ingestion | Provision the approved cloud environment, release build, storage, secrets, logging, backups, then implement/test selected adapters | Environment record, release identifier, successful scoped ingest, operating runbook |
| Workflow configuration | Set page templates, questions, freshness limits, tool permissions, approvers, audiences, budgets | Versioned workflow definitions and evidence-backed example outputs |
| User acceptance testing | Have actual pilot roles complete tasks and test denied access, revoked sources, stale data, failures, recovery, and duplicate events | UAT results with defects, owners, and acceptance decisions |
| Handoff and operation | Train owners/users, transfer operational access, confirm support and review cadence, exercise restoration and removal | Customer-owned credentials/configuration, trained owners, acceptance record, support plan |

The cloud deployment details are in the [deployment guide](06-deployment.md), with source contracts in the [integration plan](04-integrations.md). The proposed default is a single-tenant environment in the customer's cloud using managed compute, PostgreSQL, private object storage, a durable queue, company identity, and a model gateway. These production components remain implementation work. This playbook defines the customer inputs, verification, and ownership around that installation. A personal Codex account can help develop the software but is not the production runtime, scheduler, identity system, or support plan.

Hold a short weekly implementation review. Use one status page containing completed deliverables, next milestones, blockers with owners/dates, new decisions, scope changes, access/data gaps, spend, and UAT results. Record who accepted a tradeoff. Do not report an adapter as finished merely because it authenticated; it must demonstrate content retrieval, permission mapping, change handling, and removal behavior for its declared scope.

Before handoff, the customer should possess the deployment/release record, infrastructure and configuration sources, secrets ownership list without secret values, data-flow map, connector scopes, permission tests, backup/restore evidence, escalation contacts, and procedures to rotate credentials, pause a connector, offboard a user, delete a source, and export permitted knowledge. Name the support owner and incident route. Acceptance can be limited to the pilot scope; unbuilt integrations remain explicitly unaccepted.

## 6. Use a readiness scorecard with hard gates

Score each row 0 = missing, 1 = documented but unproven, 2 = demonstrated with retained evidence. The following is a proposed pilot gate: all critical rows must reach 2; other rows must reach at least 1 with a named owner and dated plan. Do not average away a failed critical control.

| Readiness item | Critical? | Evidence required for a 2 |
| --- | --- | --- |
| Business outcome and owners | Yes | Sponsor and source owners accept the scoped workflow and measure |
| Company identity and access | Yes | Real pilot accounts, group mapping, direct-link and cross-user denial checks |
| Recording/capture authority | Yes when capture is in scope | Approved procedure, enabled settings, and a permitted test with traceable artifacts |
| Authoritative sources and stable links | Yes | A reviewed sample resolves to the correct account/project and original evidence |
| Access revocation and deletion | Yes | Provider change propagates through retrieval, derivatives, caches, and future runs within the accepted objective |
| Data freshness and uncertainty | Yes | Stale/unavailable sources are visibly incomplete and do not silently drive a current answer or action |
| Controlled action execution | Yes when writes are in scope | Authorized approval, current permissions, duplicate protection, confirmed destination result, failure recovery |
| Deployment and recovery | Yes | Company-owned environment, safe secret handling, monitoring, and a completed restore exercise |
| Knowledge quality and ownership | No | Sample claims checked against evidence; disputed/missing context assigned to owners |
| User usefulness and support | No | Pilot users complete the chosen tasks and know how to report errors |
| Budget and ongoing ownership | No | Usage limits, cost reporting, renewal/support ownership, and operating cadence demonstrated |

If capture is excluded, document how authorized written notes enter the workflow and the limitations that creates. If writes are excluded, disable the production write paths rather than treating draft generation as proof of safe execution. When a critical gate fails, continue only the isolated work its failure does not compromise; for example, a synthetic-data demo can continue while production identity is unresolved.

## 7. Keep it useful after launch

An example cadence for the pilot:

- After each approved call: verify artifacts arrived, queue unmatched identities or accounts, draft evidence-linked notes, and ask the meeting owner to review material commitments.
- Daily: check connector failures, access-sync health, stale high-priority sources, failed workflows, and usage limits. Alert an accountable owner when action is needed.
- Weekly: review the selected customer handoff workflow, unresolved knowledge questions, corrections, recurring failures, and actual time saved. Publish only the agreed audience's brief.
- Monthly: review stale approved pages, access and connector scope, retention/deletion results, costs, and whether new workflows justify additional sources.
- On role change or departure: update identity and groups promptly, transfer ownership of workflows and source accounts, invalidate access, and verify scheduled jobs still have a valid accountable owner.

The delivery is complete for its agreed scope when people can perform the chosen work using current permitted evidence, owners can correct and maintain it, and the company can operate and recover the service independently of the person who built it.
