# AI Company Operating System Template

This project provides a working demonstration and an implementation blueprint for a company-owned AI knowledge and workflow service. Its intended purpose is to connect the context already spread across a company's communication, meetings, files, CRM, projects and financial systems, then make that context useful to each employee within their permissions.

For a guided path, give your company-approved assistant the [setup prompt](../SETUP.md). It should interview you about your business and existing tools, identify the necessary connections and missing implementation, then work through a tailored plan with private saved progress and verification gates. The [step-by-step playbook](19-guided-company-setup.md) supports both a nontechnical owner working with IT and a coding agent with an authorized workspace.

A sales representative could prepare for a customer call using authorized account history. A delivery lead could review commitments from the call alongside project progress. Leadership could review approved business summaries across teams. The existing systems remain authoritative: the accounting platform owns financial records, the CRM owns opportunities, and the project tool owns delivery status.

The production goal also includes a queryable company second brain that connects activity to outcomes. A sales leader could compare recorded sales behavior across won and lost opportunities. A tutoring company could compare lesson observations with measured student progress. That requires reliable links, agreed metrics and analytical queries in addition to connected tools. Findings should lead to reviewed changes whose later results become maintained company knowledge. The [company query and learning-loop guide](18-company-query-and-learning-loop.md) specifies this proposed capability; the current demo does not perform outcome analysis.

## What you can use today

The repository includes a local application with nine fictional employee personas, thirteen fictional records, evidence search, source previews and team-specific views. Server-side rules demonstrate tenant boundaries, explicit denials, source permissions and the intersection of permissions when several sources contribute to one record. Neither a CEO nor an IT administrator automatically receives access to every record.

The workflow demonstration supports a task proposal, approval by another authorized person, access rechecks and simulated execution. It stores demo proposals and events locally. The evidence preview uses deterministic keyword matching; it does not call a language model or write to outside tools.

Also included are tests, a CI workflow, local container configuration, an adapter contract, customer intake templates, a readiness declaration checker and detailed product, engineering and delivery guides. The [validation record](11-validation.md) distinguishes verified behavior from checks still outstanding. Run this demonstration only with fictional data on your own computer: its persona selector deliberately allows impersonation and is not company sign-in.

## What a real deployment still requires

Production identity, live source adapters, recording ingestion, transcription, model-generated answers, durable jobs, shared storage and cloud infrastructure are implementation work. The template makes that work explicit; importing the repository into a hosting service does not complete it. The [engineering handoff](10-implementation-handoff.md) specifies what to extend or replace.

“Adaptable to different companies” means a common integration contract with separately implemented and tested adapters. Select the adapters for the customer's actual tools and prove their behavior. A connection that can download documents must also support a reliable way to determine who may read them, track changes and remove stale or deleted content. The [integration guide](04-integrations.md) describes candidate systems and acceptance requirements.

## Why company ownership matters

A personal AI subscription can help someone design, build and maintain the software. It does not supply the shared application's hosting, persistent database, source permissions or company operating responsibilities. Employees should sign in through company identity; runtime services should use company-approved accounts, credentials, infrastructure, billing and support ownership.

An individual employee leaving the business must not take its operating context or automation with them. Company administrators need to manage access, budgets, retention, backups and incident response. The model provider is a replaceable runtime service under an approved processing arrangement. The [tools and subscriptions guide](12-tools-apis-and-subscriptions.md) separates development assistance, employee access, business-source APIs and production service costs.

## Prepare the information before connecting it

Start with one useful workflow, such as turning a recorded customer call into a cited account update and proposed follow-up. Inventory the source systems, owners, business identifiers and permissions. Establish an approved recording route through an existing meeting/recording provider or governed export. Confirm the company's recording procedure, then require readable transcripts with speakers, timestamps, source links and access metadata.

Keep original evidence versioned. Link calls to the correct account and project; send uncertain matches for review. Produce readable summaries with provenance, owners and review dates. A summary, search index or saved suggestion must not widen its source audience. Test denied access and source revocation as well as successful retrieval. The [data readiness playbook](08-data-readiness-and-delivery.md) takes this process through customer handover.

Production storage is a deliberate choice: retain authorized evidence or references, maintained knowledge, saved suggestions, approvals and execution history in approved private services. Suggestions need review state and citations; accepting a suggestion does not by itself authorize an external action. Customer data, transcripts and secrets stay outside the public repository. See [storage and lifecycle](14-data-storage-and-lifecycle.md).

## Choose a deployment starting point

| Company situation | Candidate approach |
|---|---|
| New build with approved managed services | Vercel for the interface and suitable endpoints, Supabase/PostgreSQL for selected backend services, Trigger.dev for jobs, and optional n8n workflows |
| Existing AWS | Reuse company identity and operations with an API, RDS PostgreSQL, S3 and approved workers |
| Existing Azure | Reuse the tenant and operations with an API, Azure PostgreSQL, Blob Storage and approved workers |
| Hybrid delivery | Use Vercel for the interface while keeping the policy API, database and files in AWS or Azure |

These are proposed configurations, not deployed integrations. Choose by processing permissions, existing skills, operating cost and recovery needs; document every service that receives company data. Follow the [deployment paths](13-deployment-paths.md) and [platform options](15-platform-options-and-hybrid-stacks.md), then fund a bounded pilot with clear acceptance evidence and an accountable operator.

The [documentation index](README.md) provides reading paths for sponsors, implementers and IT reviewers.
