# Guided setup for your company

Use this playbook with an AI assistant and a named company owner to turn the template into a scoped implementation, then a verified live pilot. Begin with [SETUP.md](../SETUP.md). An assistant that can only chat can conduct discovery and prepare a handoff; an assistant with authorized repository and deployment tools can also implement and verify the agreed work.

**The repository currently supplies a fictional local demo and a production blueprint. It does not contain live provider adapters, company sign-in, real model calls or production infrastructure.** A company-specific plan must include building or integrating those components. Pasting a link does not grant account access, install software, connect tools or provision services.

## How the assistant should run the conversation

Use the [company-discovery skill](../skills/company-discovery/SKILL.md) for full company onboarding. Ask one question at a time by default, explain why it matters, and adapt to the answer; use small batches only if the user prefers them. Investigate clients, actual process steps and exceptions through [deep discovery](20-deep-company-discovery.md) before selecting integrations. Offer reasonable defaults for reversible choices and let the owner correct them. Do not ask a business owner to invent OAuth scopes or cloud network settings.

Reuse facts already supplied and record decisions. Do not repeatedly ask for the same approval. Continue authorized document work, code changes and checks while an unrelated administrator action is pending. Stop only the dependent work when a required decision or permission is missing.

At every checkpoint show: what is complete, the evidence, the next small action, its owner, and any blocker. End a working session with a saved next step, so another person or assistant can resume without repeating discovery.

### Keep company answers private and portable

Create working copies of these blank templates in the ignored `.company/` directory, or an explicitly approved private company store:

| Working artifact | Start from | Purpose |
|---|---|---|
| `.company/company-profile.md` | [Company profile](../templates/company-profile.md) | Business, use cases, systems, owners, audiences and constraints |
| `.company/process-map.md` | [Process maps](../templates/process-map.md) | Current work, systems, responsibilities, handoffs and exceptions |
| `.company/discovery-notes.md` | [Discovery notes](../templates/discovery-notes.md) | Interview checkpoints, provenance, corrections and next questions |
| `.company/setup-progress.md` | [Setup progress](../templates/setup-progress.md) | Phase, decisions, evidence, blockers and next actions |
| `.company/connection-plan.md` | [Connection plan](../templates/connection-plan.md) | One connection card per selected source, model or destination |
| `.company/pilot-acceptance.md` | [Pilot acceptance](../templates/pilot-acceptance.md) | Expected answers, permission checks and operating acceptance |

The optional `python3 setup_company.py` helper initializes these blank planning files while preserving existing files. It does not connect accounts or configure a live system. Use its explicit `--directory` option only for an approved private location.

Confirm the files are ignored before writing company details. An ignore rule prevents normal Git tracking; it is not encryption or access control. Use an approved private workspace and retention policy. If the assistant cannot write files, provide nonsecret content for the owner to save privately and identify that limitation.

Never put API keys, access tokens, client secrets, passwords, recordings or real customer records in chat or the public repository. Store runtime credentials in the selected secret manager; record only a secret reference and owner. Keep sensitive evidence in the approved private system and link to it from the working artifacts. Use synthetic examples in public issues and commits.

### Use evidence-based status

| Status | Meaning |
|---|---|
| `planned` | A choice or task is documented; access and implementation have not been demonstrated. |
| `in_progress` | Work has begun, but the acceptance evidence is incomplete. |
| `blocked` | A specific missing decision, entitlement, implementation or permission prevents this step; name the owner and next action. |
| `verified` | A named test or direct inspection demonstrates a precisely stated result, with date, environment and evidence reference. |
| `not_applicable` | The agreed pilot excludes this item; record the reason and owner. |

Record the evidence basis separately: `not_run`, `reported_by_owner` or `observed`. A reported result names who reported it and when, but is not sufficient by itself to mark a check verified. An observed result needs the test or inspection evidence, not just an assertion by the assistant.

Track status per component and acceptance check. A successful OAuth login verifies authentication only; it does not verify ingestion, employee authorization or deletion handling. A green fictional demo proves no live connector behavior. Recheck evidence after relevant changes or expiry.

## Phase 1 — Understand the company and choose a first result

After the opening questions in SETUP.md, resolve any remaining business details one at a time, or in a small batch if requested. Select from the following and reuse answers already recorded:

1. What does the company do, who does it serve, and roughly how many people would use the assistant?
2. What is one question or recurring workflow that would make the first version valuable?
3. Where do the evidence and the outcome currently live, and who owns those systems?

Then resolve the first use case before expanding the inventory. Ask for the intended user, their decision, the period they care about, the current manual process and a measurable acceptance condition. Record uncertain answers as unknowns rather than guessing.

| Company answer | Next questions and minimum evidence |
|---|---|
| “Find answers in our files” | Which approved library, who may read it, what makes an answer current, and which source passages should it cite? |
| “Compare sales wins and losses” | Which call recorder and CRM, how are calls linked to opportunities, what counts as won/lost/open, and when do outcomes mature? |
| “Understand tutoring improvement” | Which lesson records and assessments, how are sessions linked to learners, what is a comparable baseline/follow-up measure, and who may see each learner's data? |
| “Summarize company progress” | Which teams, reporting period, authoritative metrics and source owners; what is excluded from each audience? |
| “Take actions for us” | What exact operation, destination and payload; who can propose, approve and execute; what proves the action happened? |
| “Everything, across the company” | Map the broader roadmap, then select one bounded workflow with named owners, usable evidence and a testable result. |

For pattern questions, use [the query and learning-loop guide](18-company-query-and-learning-loop.md). Searching a few transcripts cannot establish a population-level result. Define the outcome, joins, comparison and later measurement before promising a learning loop.

**Checkpoint:** the profile contains one pilot result, its users, data owners, explicit exclusions and success condition. Broader company coverage is a roadmap item, not an implied first-day capability.

## Phase 2 — Inventory what exists and what must be obtained

Ask what the company already uses for identity, files, communication, calls, CRM, delivery/projects and relevant outcomes. Add accounting, HR, media or other systems only where the use case needs them. Capture the actual product, edition, company account owner and available administrative contact; “we use Microsoft” is not enough to select an API.

Next ask about existing infrastructure, approved model providers, data locations, operating budget and the team that will maintain the service. Inventory current AWS/Azure services and managed platforms before proposing purchases. Use [tools, APIs and subscriptions](12-tools-apis-and-subscriptions.md) as a capability checklist, not a list of subscriptions to buy.

| Starting position | Setup route |
|---|---|
| No infrastructure or engineering owner | Run the fictional demo, prepare a private implementation brief, and assign a builder/operator before live company data. |
| Existing AWS or Azure environment | Ask the platform owner which identity, database, storage, jobs, secrets and networking services can be reused. |
| Managed-service preference | Evaluate web hosting, PostgreSQL/storage and durable jobs as separate needs; consider Vercel, Supabase and Trigger.dev or alternatives where requirements fit. |
| Existing PostgreSQL or warehouse | Keep suitable governed data services; document authorization and query boundaries rather than copying everything into a new database. |
| Existing n8n or integration platform | Reuse approved orchestration where it fits; verify credential ownership, workflow access, execution logs and retention. |
| Strict private-network or residency needs | Have the platform/security owner determine permitted hosting, inference and data movement before selecting vendors. |

Each route still needs company identities, application authorization, operated storage, implemented integrations and acceptance checks. See [deployment paths](13-deployment-paths.md) and [platform combinations](15-platform-options-and-hybrid-stacks.md). Do not force Kubernetes, a graph database, multiple model vendors or a new recorder without a demonstrated requirement.

**Checkpoint:** record one proposed deployment route, reused services, missing capabilities, responsible people and estimated cost categories. Distinguish the builder's AI subscription from separately provisioned runtime model access and hosting.

## Phase 3 — Make evidence and company context usable

Walk one real business event through its current lifecycle with the owner: where it is captured, how it is identified, where its outcome is recorded, who can read it, and what happens when it is corrected or deleted. Inspect approved samples in their private source; do not request a bulk data dump into chat.

For each source, establish a stable record ID, company/account/project or learner/session relationship, event time, source revision, owner, classification, access rules, retention and deletion behavior. Preserve original evidence separately from normalized readable text and reviewed knowledge. Track ambiguous entity matches for review instead of joining by names alone.

Build the company context needed for the pilot: business description, products/services, team responsibilities, vocabulary, metric definitions, decision rights, current priorities and relevant procedures. Give each item an owner, authoritative source, audience and review date. Context is versioned company data, not one assistant's private memory.

### If calls or lessons are required

1. Check whether an approved existing meeting, phone or tutoring system supplies recording/transcript exports or APIs for the actual company plan.
2. If capture is absent, choose an approved capture method and assign the business owner to establish the applicable notice, consent and retention process. Do not silently record participants.
3. Define meeting/session IDs, participants, account/opportunity or learner/course links, timestamps, language, speaker labels and recording/transcript locations.
4. Verify readable transcripts with timecodes and source access. If audio is the only evidence, plan approved transcription and its processing location, costs and quality review.
5. Check an authorized sample against the recording. Flag gaps, uncertain speakers, unmatched records and missing outcomes; do not convert missing evidence into a negative outcome.
6. For lessons or sensitive calls, explicitly separate instructor/sales, leadership, customer/guardian and administrative audiences.

Follow [data readiness and delivery](08-data-readiness-and-delivery.md) and [storage and lifecycle](14-data-storage-and-lifecycle.md). A governed export can support a bounded first pilot when live APIs are unavailable, provided permissions, refresh, provenance and deletion can be maintained. It must be labeled an import, not a live connection.

**Checkpoint:** a reviewed private sample is readable, correctly linked and permissioned; missing capture or outcome collection has an owner and implementation task. If those facts cannot be established, keep that source blocked.

## Phase 4 — Turn each selected connection into an actionable card

Create one card in the connection plan per source, model service, identity integration and action destination. The assistant should research current official provider documentation for the exact product and edition before giving setup instructions. Record document URLs and the date checked. If research or administrative access is unavailable, record the unresolved point and its owner; never invent console paths, scopes or API availability.

Every connection card must specify:

- **Purpose and scope:** pilot question, required objects/fields, allowed containers, expected volume and explicit exclusions.
- **Ownership:** company account, source administrator, business/data owner and runtime credential owner; separate employee delegation from service access.
- **Prerequisites:** product edition, API/export entitlement, required administrator role, approved processing location and any additional cost.
- **Authentication:** supported method, application registration owner, exact documented minimal permissions, consent/grant requirements and renewal/revocation process.
- **Callback and events:** if OAuth/webhooks apply, the implemented staging/production callback routes, exact registered URLs, validation/signature method and approved network exposure. Mark these not applicable where appropriate.
- **Implementation:** adapter status, repository component or tracked work item, supported object types, ACL/identity mapping, pagination, quotas, retries and backfill strategy.
- **Lifecycle:** cursor/checkpoint, expected freshness, reconciliation, source correction/deletion propagation, disconnect behavior and downstream invalidation.
- **Credential storage:** approved secret-manager reference and runtime identity; never the credential value.
- **Verification:** an allowed sample, a denied identity, an update, a revocation/deletion, expected receipts and the evidence location.
- **Immediate next step:** the exact human or assistant action, owner, status and blocker if any.

Implement and inspect an OAuth callback before asking an administrator to register its URL. A URL copied from a generic example is not an application's working callback. Validate staging separately from production, and keep tokens out of browser-delivered code and logs.

Present the card to the relevant owner in plain language: “This connection needs access to this library for this purpose; this administrator performs this step; this check will prove it works.” Request only the missing action. Company authorization to implement the pilot does not grant arbitrary access to unrelated systems or audiences.

**Checkpoint:** each selected connection has a bounded implementation and verification path. “Supported by vendor API” and “implemented in this template” remain separate statements.

## Phase 5 — Confirm permissions and the operating boundary

Map company identity to application membership, source identities, teams and resource grants. List the pilot personas and the sources, fields and operations each should be able to use. Leadership can have broad approved access; a CEO title or application-admin role is not a source-data bypass.

Test derived information as well as original files: titles, search snippets, counts, transcripts, joined outcomes, summaries, saved suggestions, historical answers and notifications. A stored result does not become broadly shareable because an assistant produced it. Define how revocations invalidate caches, descendants and scheduled delivery.

Separate read/query authority, proposal authority, approval authority and execution authority. For live writes, define allowed operation, destination, audience, exact payload, spend/volume limit, expiration and execution identity. Use required company review gates; reuse existing authorization when it covers the concrete next step instead of repeatedly asking for blanket permission.

**Checkpoint:** the owner approves the private access matrix and acceptance examples. Unsupported source permission semantics block ingestion of that scope; do not replace them with a broad service token.

## Phase 6 — Demonstrate, implement and deploy in distinct steps

First offer the local fictional demo using the [README quick start](../README.md). It helps the company inspect the intended experience without providing business data or external credentials. Document that its selectable demo identities, SQLite state and simulated actions cannot serve real employees.

Translate the selected pilot into engineering work using [the implementation handoff](10-implementation-handoff.md): production identity, data plane, actual adapters, ingestion, model/retrieval service, governed analytical queries where needed, maintained knowledge, and any allowed action engine. Reuse tested company services where appropriate. Assign an owner and acceptance evidence to each work package.

| Assistant capability | Useful work it can complete |
|---|---|
| Conversation only | Interview, compare options, produce private plans and owner-specific checklists, inspect supplied nonsecret evidence, and prepare the builder handoff. |
| Writable coding workspace and command tools | Inspect actual code, implement the scoped components, add meaningful tests, and prepare reproducible deployment configuration. Read-only repository browsing supports inspection and planning only. |
| Authorized provider/cloud access | Inspect configuration, perform covered setup actions, deploy the agreed environment, and collect direct verification evidence. |
| Missing or denied access | Mark the dependent step blocked and give the responsible person exact instructions plus the nonsecret result needed to resume. |

Build staging before a live pilot. Establish the company-owned repository, billing and service identities; provision the chosen runtime/data services; configure private secrets and company sign-in; apply migrations; deploy the implemented services; register verified callbacks; ingest only the approved sample; then run acceptance tests. Use [deployment guidance](06-deployment.md) for operational responsibilities.

Do not present the supplied Docker files or a successful hosting deployment as a completed enterprise product. Record which components were actually built and exercised. A job scheduler, model account or OAuth grant is only one part of the working system.

**Checkpoint:** staging runs the implemented workflow against bounded authorized evidence, with monitoring and explicit failure behavior. Remaining work is visible; the service is not declared production-ready from a successful page load.

## Phase 7 — Verify one complete live loop

Populate the pilot acceptance artifact with company-specific questions and expected behavior before testing. Keep sensitive inputs and results private. Include an ordinary user, an authorized reviewer, a denied user and an offboarded or revoked identity.

| Acceptance area | Evidence required |
|---|---|
| Connected evidence | A real approved source object appears with correct identity, version, readable content, lineage and freshness. |
| Useful answer | A defined question returns supported facts and openable citations; missing evidence produces an honest gap. |
| Patterns and outcomes | If selected, approved joins and metrics reproduce the eligible population and result; uncertainty and outcome maturity are visible. |
| Access | Denied and cross-company requests reveal no restricted content, metadata or derived result; revocation affects saved outputs and deliveries. |
| Source lifecycle | A changed/deleted source updates or invalidates downstream material within the agreed envelope. |
| Action, if selected | An authorized exact proposal reaches required review, executes once, and has a destination receipt or explicit uncertain-outcome reconciliation. |
| Learning loop | A reviewed finding leads to a recorded change, later measurement and an accountable keep/revise/stop decision. |
| Operations | Failure/retry handling, monitoring, budget controls, backup restore and credential rotation are exercised at the agreed pilot scope. |
| Independence | Company sign-in and scheduled work continue after the original builder closes their laptop; company staff can manage access and incidents. |

Mark each check with its status, evidence basis, test date and evidence reference. External effects must be tested only in the authorized scope. If later outcome measurement takes weeks, the loop remains incomplete until that evidence exists; report a working pilot and its scheduled measurement separately.

**Checkpoint:** the business owner accepts the demonstrated scope, named limitations and operating plan. Expansion to another team or source requires its own data and permission checks.

## Phase 8 — Hand over, resume and expand

Deliver the private company profile, connection cards, deployment record, access matrix, acceptance evidence and remaining backlog. Include operator contacts, support hours, incident route, release/rollback procedure, restore instructions, credential rotation and offboarding. Record costs and service ownership so the original builder is replaceable.

For each new team, conduct the relevant discovery questions, connect only what its use case needs, and test permissions on shared and derived data. Maintain reviewed company knowledge with source lineage, owners and review dates. Retire lessons when later results contradict them.

At the end of every session, save this resumption note in setup progress:

1. Current phase, agreed pilot scope and selected architecture.
2. Completed work and the precise evidence supporting each verified claim.
3. Decisions, private artifact locations, unresolved assumptions and blockers with owners.
4. The next three actions, their owners, required access and expected proof of completion.
5. Outstanding review/measurement dates and changes that require revalidation.

A resuming assistant reads those artifacts and the actual repository state first, confirms any expired or changed facts, and continues at the next incomplete step. It must not infer that a connection exists from a plan, a checked box, a past conversation or this playbook itself.
