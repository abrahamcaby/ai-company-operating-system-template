# Delivery roadmap, economics and commercial scope

**Current state: fictional local demonstration plus an implementation blueprint.** The roadmap below is work to fund and execute. A 90-day pilot is a scoped validation milestone, not a promise of complete enterprise readiness or support for every vendor in the integration catalog.

## 1. A sellable first engagement

Offer a bounded company knowledge and workflow pilot: connect a small number of existing systems, preserve their access rules, answer a measured set of questions with evidence, and produce a useful recurring briefing. Start with one business process crossing teams, such as sales-to-delivery handoff, account renewal review, or project risk reporting. The broader company OS grows from proven use cases and a shared platform.

Specify the customer's chosen document source, communication/meeting source and business system. Define approved users and containers, expected volume, exclusions, model policy and acceptance measures. Sell the verified workflow outcome and deployment ownership. Do not sell an unsupported logo wall or an AI that autonomously operates the entire business.

Useful first deliverables:

- Company login and tested user/source identity mapping.
- Three narrowly scoped read-only integrations, or fewer when source permissions are difficult.
- Search and answers with citations, source freshness and “insufficient evidence” behavior.
- One or two compiled artifacts, such as an account brief and project decision log, with dependency permissions.
- One recipient-specific recurring briefing delivered in the authenticated application.
- An administrator view for coverage, permission health, usage and audit events.
- Customer-cloud deployment, a tested restore path, support ownership and handoff materials.

Defer raw media retention if approved transcripts are sufficient. Defer financial postings, automatic external emails, unrestricted agent execution and broad personal-message ingestion. Each adds a separate control and operational burden.

## 2. Ninety-day pilot plan

The schedule assumes a small dedicated engineering team, timely customer access and APIs that support the selected scope. Procurement, identity configuration, source API approval or incomplete customer records can extend it. [Data readiness and delivery](08-data-readiness-and-delivery.md) defines the intake and customer-side prerequisites.

| Period | Build and delivery work | Gate to continue |
|---|---|---|
| Days 1–14: discovery and foundations | Observe actual workflows; baseline time/quality; inventory sources; choose hosting/identity/model routes; threat model; implement production auth and domain contracts | Named sponsor/data owners; usable test access; confirmed data rights/retention; first question set; viable source ACL strategy; bounded paid scope |
| Days 15–35: identity and first connector | Deploy staging foundation, metadata/policy store, audit, queue; implement one document connector; backfill selected scope; add retrieval/citations | Direct/inherited/group/guest permission tests pass; offboarding/revocation measured; coverage reconciles; restore path demonstrated |
| Days 36–55: cross-system workflow | Add communication and selected business source as capacity permits; resolve customer/project entities; typed query adapters; compile first artifacts | Golden questions supported by correct evidence; restricted information absent from all surfaces; ambiguous identities/ACLs quarantined |
| Days 56–75: user pilot | Enable small cohort, recipient-specific briefings, admin health/cost views; instrument outcomes and feedback; test outages and adversarial content | Sponsor sees repeated workflow value; no unresolved high-severity access finding; costs within budget; operators can recover from expected failures |
| Days 76–90: acceptance and handoff | Fix highest-impact gaps; repeat release gates; timed restore; documented support and upgrade process; deliver next-phase proposal | Customer UAT accepted; named operator; readiness checklist complete; limitations explicit; expansion justified by measured outcomes |

Treat gates as decisions, not dates that override evidence. If a source cannot express sufficient permissions, narrow it, replace it, use delegated reads or exclude it. Do not compensate by making every pilot user an administrator.

## 3. After the pilot

| Stage | Scope | Evidence required |
|---|---|---|
| Next 3–6 months, depending on findings | Harden supported connectors; multi-environment upgrades; independent security testing; deeper observability; SCIM/group edge cases; deletion and retention automation; load/capacity testing | Repeatable customer install, tested access-change envelopes, documented service objectives, independent findings addressed, recovery evidence |
| Controlled action expansion | A few reversible task/CRM actions with destination checks and explicit approvals | Exact-payload approval, execution-time access checks, idempotency/reconciliation, failure compensation and customer sign-off |
| Finance and media expansion | Governed accounting report catalog, specialized ERP adapters, approved media lifecycle/transcription | Finance-owned definitions reconcile to source reports; media rights/provenance and derivative deletion verified |
| Multi-customer service, if demanded | Tenant lifecycle, metering, billing, regional routing and isolation testing | Security architecture for shared operations, noisy-neighbor controls, tenant deletion/restore proofs and support contract |

Some mid-market customers can stay on the dedicated deployment model indefinitely. A broad market does not require every customer to share one database or one model account.

## 4. Delivery team and responsibilities

A practical pilot team is a technical/product lead, a backend/security engineer, an integration/data engineer and a frontend/full-stack engineer, with fractional design, QA/platform and independent security support. One person may cover several roles for a smaller scope, but connector permissions, operations and product quality still require dedicated time. Budget additional specialists for ERP or regulated content requirements.

Customer participation is not optional: an executive sponsor, a process owner, identity/cloud administrator and data owners need regular availability. The customer controls source configuration, recording practices, access decisions and operational adoption. The delivery team supplies implementation and evidence; it cannot reconstruct missing project decisions or recording history by guessing.

## 5. A transparent cost model

All numbers below are **illustrative planning assumptions in USD, not provider quotes, current market prices or a proposed customer invoice**. Replace unit rates with approved provider quotes and pilot telemetry. Existing CRM/meeting/API entitlements, tax, legal review and dedicated GPU costs may be additional. Costs vary heavily with corpus size, retrieval depth, meeting volume, context length and required availability.

```text
Q = active_users × questions_per_workday × workdays
generation = Q × ((input_tokens × input_rate_per_million)
                 + (output_tokens × output_rate_per_million)) / 1,000,000
embedding = changed_tokens × embedding_rate_per_million / 1,000,000
transcription = newly_transcribed_minutes × transcription_rate_per_minute
monthly_total = generation + embedding + transcription + cloud_fixed
              + storage_and_egress + integration_licenses + operations
```

Example workload: a 1,000-person company with 200 active users, 10 questions per workday and 22 workdays generates **44,000 questions/month**. Assume 8,000 input tokens and 1,000 output tokens per question, rates of $2/million input and $10/million output, 100 million changed tokens embedded at $0.10/million, and 120,000 newly transcribed minutes at $0.01/minute.

| Component | Assumed calculation | Illustrative monthly amount |
|---|---|---:|
| Model generation | 352M input × $2/M + 44M output × $10/M | $1,144 |
| Embeddings for changed content | 100M × $0.10/M | $10 |
| Transcription | 120,000 minutes × $0.01 | $1,200 |
| Application/database/queue/monitoring | Planning allowance, to be replaced by a cloud estimate | $1,500–$3,500 |
| Storage and egress | Planning allowance based on actual retained media | $200–$1,000 |
| Total before licenses and operations | Sum above | **$4,054–$6,854** |

This example excludes retries, compilation, evaluations, long agent workflows and non-answer model calls; meter them separately before forecasting. Already available transcripts can reduce transcription cost. Raw recordings can dominate storage/egress. A stronger model or larger context changes the generation line; it does not necessarily change every other line.

When selecting [managed services or a hybrid stack](15-platform-options-and-hybrid-stacks.md), replace the cloud allowance with each chosen provider's current quote and observed usage. Include web hosting, database compute/storage, workflow execution and retained state, automation editions, private networking, SSO/governance features, backups, cross-provider egress and support. Self-hosted editions move operating work to the delivery team; they do not remove its cost. Record n8n's applicable internal-use or commercial delivery terms before pricing a customer offering. No provider prices are quoted by this example.

For sensitivity: doubling question volume doubles the generation portion under unchanged token assumptions. Doubling context length doubles only input token cost. Cutting the active user count does not halve fixed database/monitoring cost. Track cost per completed business workflow and per active user, not merely cost per token.

Controls to implement: per-tenant and per-workflow budgets; daily alert thresholds; job concurrency and token ceilings; cheaper approved routes for simple extraction; batching/deduplication; changed-content embedding; media retention policy; and a hard stop that leaves workflows in an explicit pending/unavailable state. Caching must respect per-user access and revision keys.

## 6. Build and ongoing operations budget

For planning this scope, allocate the equivalent of roughly **10–16 person-months of work** across engineering, product/design, platform and QA in this proposed scope. At an assumed fully loaded $15,000–$25,000 per person-month, the arithmetic is **$150,000–$400,000**, plus infrastructure, source vendor fees and independent security work. This is a scope-planning range, not a claim about prevailing salaries or a fixed bid. Reduce the pilot scope to fit smaller budgets; production integration and operations require sustained work.

Ongoing operations are a separate budget: connector API changes, auth failures, schema drift, customer permission changes, model evaluations, security updates, incident response and source-quality support. Assign named owners and estimate actual support hours. A low token bill does not imply a low total service cost.

For a commercial offering, separate a fixed discovery/readiness engagement, a bounded implementation/pilot fee, a recurring operations/support fee and metered/pass-through usage. Custom connectors and new action classes are separately scoped. The GitHub repository can demonstrate clarity and credibility while the paid value is installation, supported integrations, governed workflows, maintenance and accountability.

## 7. Success measures and stop conditions

Choose baseline and target with the customer before the pilot. Suggested measures are:

| Measure | How to collect it | Example acceptance condition to negotiate |
|---|---|---|
| Evidence quality | Human-reviewed representative question set with expected source references | At least 90% of answerable questions cite the correct supporting source; unsupported questions abstain |
| Permission isolation | Adversarial identity/resource matrix across search, details, saved artifacts and jobs | Zero unauthorized disclosures in the defined test suite; no unresolved critical/high access defects |
| Workflow value | Before/after time studies for a repeated task | A material reduction, such as 30%, without lower reviewer quality; report sample size and uncertainty |
| Adoption | Weekly active pilot users and repeat use of named workflows | Sustained repeat use, not one-time demo visits |
| Reliability | Source freshness, auth failures, queue age, recovery drills | Within the agreed source-specific service envelope |
| Economics | Cost per completed workflow plus operating effort | Within customer budget at measured and forecast volume |
| Knowledge maintenance | Owner review, correction and stale artifact handling | A named owner can correct a claim and see downstream artifacts become stale/rebuild |

Do not expand a pilot with unresolved access leaks, no operational owner, source content that is too incomplete to support the use case, persistent unsupported answers or no observed business benefit. Document the reason, narrow scope and retest. “More connectors” is not a substitute for a useful, trustworthy workflow.

## 8. What the repository should let a buyer verify

A prospective customer should be able to run the fictional demo, inspect permission behavior, understand the difference between implemented and planned capabilities, follow a realistic install plan, review the connector contract and see an honest cost model. The repo should explain what the customer must provide and how the implementation will be accepted.

Before presenting this as a production product, replace planned claims with release evidence: tested connectors, production authentication, infrastructure modules, recorded access tests, restore results, support policy and documented limits. Until then, position it as a working demonstration and an enterprise implementation blueprint.
