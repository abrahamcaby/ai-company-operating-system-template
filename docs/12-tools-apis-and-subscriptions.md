# What you need: tools, APIs, accounts and AI subscriptions

This guide is for the person asking, “What do we actually need to obtain, install, connect and pay for?” The same product design can start from a new company environment or fit into existing AWS, Azure or other infrastructure. Select one appropriate service for each required capability; the examples are alternatives, not a shopping list to buy in full.

**Current release boundary:** the included demo runs locally with Python, fictional records and no external APIs. The production services below are requirements to implement and operate. Buying their subscriptions does not activate unbuilt connectors or make the demo a production deployment.

Read this first, then choose a path in [deployment paths](13-deployment-paths.md). Use [storage and lifecycle](14-data-storage-and-lifecycle.md) to decide what the company will retain.

The [platform selection guide](15-platform-options-and-hybrid-stacks.md) also covers Vercel, hosted/self-hosted Supabase, PostgreSQL providers, Trigger.dev, n8n and hybrid combinations with existing AWS or Azure. They are alternative implementations of the capabilities below; purchasing all of them is unnecessary.

## 1. Can someone start with just a personal AI subscription?

**For building and exploring: yes, an AI coding assistant can help create code, tests, documentation and deployment configuration. The supplied demo does not even require that subscription to run.** The builder still needs a computer and the local tools described below. Real customer information needs the company's approved development and data-handling arrangements.

**For running this shared company service: a personal subscription alone is not the operating setup.** The proposed product needs its own runtime, storage, employee identities, source-system access and model capacity. Those can be paid for and operated directly by the company or provided through a managed service agreement. They do not come into existence merely because the developer has an AI assistant.

For the OpenAI example, Codex supports ChatGPT subscription sign-in and API-key sign-in. API-key use is charged through the OpenAI Platform account rather than included ChatGPT credits. This design uses separately provisioned company model access for the deployed application. [Official authentication and billing distinction](https://learn.chatgpt.com/docs/auth).

| Situation | What works | What must be added |
|---|---|---|
| One builder exploring the idea | Local fictional demo; optional personal coding assistant | No external runtime services for the supplied demo |
| One builder preparing a customer pilot | Use the assistant to implement the scoped product, review changes and prepare deployment | Company-owned accounts, approved data scope, real authentication, supported adapters, operated hosting and acceptance tests |
| Employees using the custom Company OS app | Browser and company sign-in; the server makes permitted model/tool requests | Backend model billing/capacity and source entitlements; employees do not each need a personal ChatGPT account for this architecture |
| Trusted automation inside an enterprise AI workspace | An alternative runtime may use that platform's supported enterprise service identities | Eligible plan, workspace policies, runtime integration and company-owned identities; verify feature/contract fit |
| Company requiring private inference | An approved self-hosted model can replace an external generation API | Model-serving infrastructure, compute, patching, capacity and quality evaluation; this is not cost-free hosting |

Enterprise Codex automation is a distinct option worth evaluating: official documentation describes workspace service accounts on pay-as-you-go plans, with their own access and configured integrations. API Platform project service accounts have separate access and billing. This is an alternative integration path, not something implemented by this repository, and it does not remove the need for Company OS data storage and application authorization. [Workspace service accounts](https://learn.chatgpt.com/docs/enterprise/service-accounts).

For the recommended custom application, create the model project under company ownership, use an appropriate project service identity, and keep runtime credentials in the secret manager. The company should be able to rotate them and continue operating when the original builder leaves. Use administrative credentials only for provisioning/administration, not normal employee requests. [API project service-account reference](https://developers.openai.com/api/reference/resources/admin/subresources/organization/subresources/projects/subresources/service_accounts).

A practical transition is: **personal development environment → company-owned repository and accounts → isolated staging → scoped customer pilot → operated production**. Acceptance includes closing the developer's laptop and confirming that scheduled work, sign-in and authorized queries continue independently. Treat that as a real operational test.

## 2. External business tools: reuse what the company already has

Connect a category only when a selected workflow needs it. For example, a customer handoff pilot may begin with files, CRM and customer-call transcripts; adding payroll would be unnecessary scope.

| Tool category | What it contributes | Examples or substitute | Needed when |
|---|---|---|---|
| Company directory / identity provider | People, groups, sign-in and offboarding | Existing Entra ID, Okta or compatible company identity service | Every real multi-user deployment |
| Company files / knowledge | Policies, operating context, project files, approved presentations | SharePoint/OneDrive, Google Drive, Box, existing document system, governed import | Shared knowledge is in scope |
| Communication | Approved channel/thread decisions and working context | Teams, Slack or an existing communication API | Channel context is part of the workflow; private messages can remain excluded |
| Meetings / customer-call capture | Recordings, transcripts, timecodes and meeting metadata | Existing Zoom, Teams, Meet, licensed sales recorder; authorized written notes if recording is unsuitable | Meeting or call evidence is in scope |
| CRM | Account/contact IDs, opportunities, stage and ownership | Salesforce, HubSpot, existing CRM or approved structured export | Customer/deal workflows |
| Delivery / project management | Work items, delivery owner, milestones, acceptance and blockers | Jira, Asana, ClickUp, existing project system | Sales-to-delivery or operational workflows |
| Accounting / ERP | Defined financial reports and reconciled values | QuickBooks, NetSuite, Xero or an existing ERP/reporting service | Finance-approved questions; ordinary knowledge search does not require it |
| Media / asset management | Original assets, rights, expiry and permitted reuse | Existing DAM, private object storage or approved file library | Media retrieval or reuse |
| HR / People | Approved policies and separately restricted People records | Existing HRIS and private People workspace | Deliberately selected People workflows; do not ingest by default |
| Notification destination | Delivers alerts or links to reviewed outputs | Existing email/channel provider | Notifications are enabled; the in-app queue can come first |

An existing license may not include the API, transcript, export or administrative capability required by the adapter. Have the source owner verify the exact account edition and granted scopes. A user's ability to open a tool in a browser does not prove an application can fetch that same record, and an application administrator token does not prove an employee may read everything it fetches.

The [connector catalog](04-integrations.md) contains provider-specific references and permission limitations. The [capture playbook](08-data-readiness-and-delivery.md) explains how to make recordings and transcripts available before asking AI to use them.

## 3. Runtime services the deployed product needs

These are functional requirements for the proposed architecture. A managed provider may bundle several, and a company can reuse compatible existing services after checking isolation and capacity.

| Capability | What it does | Initial production direction | Who owns it |
|---|---|---|---|
| Application hosting | Runs the website, API and background workers after laptops close | Managed container services; separate API and workers | Platform/IT |
| Relational database | Stores identities, permission metadata, source versions, knowledge metadata, saved drafts and workflow states | Managed PostgreSQL | Platform + application team |
| Private object storage | Holds selected approved evidence copies, normalized transcripts and generated artifacts | Customer-controlled object store with encryption and lifecycle rules | Platform + data owners |
| Search | Finds authorized text and optional vector matches | PostgreSQL full-text plus a supported vector option initially; separate engine only if needed | Application team |
| Durable queue / scheduler | Resumes ingestion, refreshes knowledge and runs approved recurring jobs | Managed queue plus durable job state and scheduler | Application/platform |
| Identity integration | Verifies employee sessions and current membership | Existing company identity provider plus application integration | Identity administrator |
| Secret manager / key management | Protects connector credentials, database secrets and encryption keys | Existing approved cloud secret/key service | Security/platform |
| Model runtime | Generates summaries, answers and structured suggestions | Company-approved model API, existing model gateway or private endpoint | AI/application owner + procurement |
| Monitoring / audit / backups | Detects failures and provides recovery evidence | Existing monitoring stack, protected audit sink and tested backup service | Operations/security |
| Networking / domain / certificates | Provides a stable internal or approved external HTTPS address | Existing ingress, DNS, certificates and private connectivity | Network/platform |

A graph database, a dedicated vector database, a new meeting recorder, a paid automation platform, fine-tuning, Kubernetes and multiple model vendors are all **optional**. Add them only for an identified requirement. Maintained company memory is application data; it does not require fine-tuning a model on every company document.

For a managed-service implementation, Vercel can supply web hosting, Supabase can supply PostgreSQL and selected backend services, and Trigger.dev or another workflow engine can supply durable processing. n8n can add visual integration workflows where appropriate. Existing RDS or Azure PostgreSQL can remain the application database without adding Supabase. See [database choices](17-postgres-and-supabase-options.md) and [jobs and automation](16-jobs-and-automation-options.md) for responsibilities, credentials, retention and plan requirements.

## 4. What people install or need access to

| Person | Tools or access | Purpose |
|---|---|---|
| Ordinary employee | Supported browser and company sign-in | Use the deployed service; no terminal, cloud console or personal model key |
| Business/data owner | Existing source-tool admin/owner access as appropriate; private intake templates | Select records, define authoritative context, verify data quality and approve audiences |
| Local demo reviewer | Python 3.11+, browser, downloaded repository; Git optional | Run `python3 -m app.server`; no provider key or package installation |
| Developer | Git, editor, supported language runtime; optional AI coding assistant | Implement/review code and run checks |
| Container builder | Docker-compatible build tooling or an approved remote builder; registry access | Build and publish reproducible images; verify local Docker files before relying on them |
| Cloud deployer | AWS CLI or Azure CLI for the chosen cloud, approved cloud role, selected infrastructure tool | Provision and configure the production components once implemented |
| Infrastructure maintainer | Existing Terraform/OpenTofu, AWS CDK/CloudFormation or Azure Bicep workflow; choose one approach | Reviewable environment definitions, drift/change management and protected state |
| Release operator | GitHub Actions, Azure DevOps or existing CI/CD; scoped deployment identity | Build, test, scan, stage and promote reviewed releases |
| Operations owner | Monitoring, incident route, cost visibility, restore access and runbooks | Keep the service healthy and recover it |

Cloud CLIs and infrastructure tools are engineering tooling. Do not require every employee to install them. An AI assistant can help operate those tools under the engineer's authorized controls, but the cloud permissions and ongoing bills still belong to the operating organization.

## 5. APIs and credentials: what is actually required?

An API is an application's interface. An API key, OAuth grant and cloud role are different ways of authorizing access. There is no single “company API key” that safely grants access to every system.

| API / interface | Required for | Credential / approval pattern | Minimum readiness evidence |
|---|---|---|---|
| Employee identity | All production employee access | App registration and verified sign-in; directory provisioning or a controlled lifecycle feed | Issuer/audience/redirects validated; allowed, denied and disabled-user tests |
| Generation model | Real generated answers, summaries and suggestions | Company model project, service identity/API credential or supported workload identity | Approved endpoint/model, billing/capacity, allowed data classes, budget and failure test |
| Embeddings | Optional semantic retrieval | Approved model endpoint or local embedding service | Model/version/dimensions pinned; source ACLs enforced around the index |
| Transcription | Calls lack suitable provider transcripts | Approved speech API or private transcription worker | Recording policy, readable timestamps/speakers, language/quality tests and retention settings |
| Document / file APIs | Selected source files | Delegated OAuth or scoped application access, selected containers | Content, identity, inheritance, change and deletion behavior verified |
| Messaging APIs | Selected channels/threads | Workspace-installed app or approved delegated access | Membership/guest handling, edits/deletions and quota plan |
| Meeting / recording APIs | Automated call artifact retrieval | Provider application and approved recording/transcript scope | Correct meeting/recording IDs, permissions, ready-state events or polling |
| CRM APIs | Account/deal context | Customer's supported OAuth/application integration | Object, record and field access; ID mapping; modified/deleted/merged records |
| Project APIs | Delivery/work-item context | Scoped project integration | Project/issue/task restrictions; owner and milestone mapping |
| Accounting APIs | Approved financial reports | Dedicated Finance-approved integration identity | Legal entity, report/field permissions, currency/period definitions; read-only pilot |
| Cloud infrastructure APIs | Deployment and runtime access to storage/queues/secrets | Engineer's scoped deployment role and separate workload identities | Correct account/subscription, region, network and least-privilege resource access |
| Notification / write APIs | Sending alerts or executing approved changes | Separately enabled destination/write scopes | Exact target/payload approval, audience check, idempotency and outcome verification |
| Webhooks / polling | Keeping source changes current | Signature-verified provider callbacks or scoped read credentials | Replay handling, renewal, missed-event reconciliation and documented latency |

For an OpenAI-backed implementation, the Responses API supplies generation; embeddings and transcription are separate capabilities to configure only if needed. The repository currently calls none of them. Model and source choices remain replaceable through the application contracts. [Text generation](https://developers.openai.com/api/docs/guides/text), [embeddings](https://developers.openai.com/api/docs/guides/embeddings), [file transcription](https://developers.openai.com/api/docs/guides/speech-to-text).

Signing into the app with a Microsoft or Google account does not itself authorize access to SharePoint, Drive, mail, meeting recordings or CRM data. Source integrations need their own approved grants and effective-user access checks. Similarly, hosting on AWS does not require changing a customer's Microsoft identity or Salesforce CRM; hosting and business-tool choices are separate.

Record every interface in the [API access register](../examples/api-access-register.csv). Include its owner, purpose, credential type, scopes, source account, tested permission limitations, quota, secret **reference**, renewal/expiry, and revocation test. Never enter credential values in that register or commit the customer-filled copy to this public repository.

## 6. What leaves the company environment?

The company controls its application database and selected evidence stores in the proposed dedicated deployment. Approved excerpts may still be sent to a model/transcription provider, and connected business tools already hold their own records. Record each processing location and service boundary.

For OpenAI, application-state storage and abuse-monitoring retention are separate controls. Setting `store: false` does not establish universal zero retention; endpoint features, caching and eligibility for additional controls matter. Review the chosen endpoint/model and organization configuration, including any exceptions, before sending customer data. [OpenAI data controls](https://developers.openai.com/api/docs/guides/your-data).

The storage plan must distinguish original evidence, readable derivatives, saved suggestions and provider processing. See [the data lifecycle matrix](14-data-storage-and-lifecycle.md) for what gets saved, where, who can open it, and what happens when access changes or data is deleted.

## 7. Separate the bills and ownership

Budget separately for developer tools; application hosting/database/storage; generation/embedding/transcription; source-system licensing/API access; and implementation/support. A developer's personal assistant plan is only one possible development expense. Do not assume it covers employee usage, recordings, source vendors or cloud operations.

Existing AWS/Azure contracts may cover some infrastructure procurement, but confirm actual capacity, quotas, regions and allocated cost centers. Cloud credits and existing enterprise agreements do not imply unlimited model or source API usage. Use the [economics worksheet](07-roadmap-and-economics.md) for the cost categories and replace illustrative assumptions with the selected provider's actual rates.

Before production, the customer should own or have a documented operating agreement for: repository, cloud resources, domain, identity app, model account/project, source apps, secrets, retained data, backups and incident response. Identify who can export the data, rotate credentials and operate the service if the original developer is unavailable.
