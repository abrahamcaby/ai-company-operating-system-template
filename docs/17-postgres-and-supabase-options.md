# PostgreSQL, Supabase and managed database options

**Status: production design and procurement guide, checked September 17, 2026.** These are implementation choices, not installed integrations. The current demo uses SQLite and fictional evidence. Read this alongside [deployment paths](13-deployment-paths.md) and [storage and lifecycle](14-data-storage-and-lifecycle.md).

Use [platform options and hybrid stacks](15-platform-options-and-hybrid-stacks.md) to place the selected database alongside Vercel, workers and existing AWS/Azure services.

## 1. Choose a database foundation, then choose surrounding services

PostgreSQL is the database engine. Supabase is a platform built around PostgreSQL. Amazon RDS, Azure Database for PostgreSQL and Neon are alternative ways to obtain a managed PostgreSQL service. They are not five required purchases.

| Choice | What it supplies | Appropriate starting situation |
|---|---|---|
| PostgreSQL operated by the company | A relational database the operator installs and maintains | An experienced team already operates databases and wants that responsibility |
| Supabase hosted platform | A PostgreSQL database with integrated Auth, Storage, Realtime, APIs and other services | A small implementation team wants several application backend capabilities together |
| Amazon RDS for PostgreSQL | Managed PostgreSQL within the customer's AWS environment | AWS governance, networking and database operations are already established |
| Azure Database for PostgreSQL | Managed PostgreSQL within the customer's Azure environment | Azure governance and operations are already established |
| Neon | Managed PostgreSQL with a database branching workflow | A team wants a managed database and separately chooses the other application services |

Supabase provisions a full PostgreSQL database for each project and builds its other services around it. RDS and Azure offer managed PostgreSQL, while Neon's branching can support isolated development workflows. These services have different limits, administration models and supporting features; confirm the selected plan and region. [Supabase database](https://supabase.com/docs/guides/database/overview), [RDS PostgreSQL](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/CHAP_PostgreSQL.html), [Azure PostgreSQL](https://learn.microsoft.com/en-us/azure/postgresql/overview), [Neon branching](https://neon.com/docs/get-started-with-neon/workflow-primer)

For Company OS, choose **one authoritative application database** for source metadata, permission mappings, approved knowledge, saved suggestions, approvals and execution receipts. Existing CRM, accounting and project tools remain authoritative for their own business records. An analytics replica or rebuildable search index may be justified later; avoid creating two competing Company OS databases by default.

## 2. Three practical configurations

### A. Start with hosted Supabase

Proposed arrangement: Vercel hosts the employee interface and suitable application endpoints; Supabase provides the application database and selected backend services; Trigger.dev or another worker system runs ingestion and processing. Use n8n only where its connectors and workflows save useful integration work. Choosing all these products is optional.

Before implementation, decide whether Supabase Auth integrates with company sign-in or another approved identity component handles sessions. Decide whether retained files use Supabase Storage or an existing private S3/Blob store. Record who controls each account, which service can read each data class, and which region handles each processing step. None of these products automatically imports the company's source permissions.

**Hosted Supabase remains a separately managed service.** Buying it while also using AWS does not place its project inside the customer's AWS account or private network. Treat connections between providers as explicit network and data flows. Supabase publishes project region choices; align the database with the application and worker locations where appropriate, then verify other services' processing and logging locations separately. [Supabase regions](https://supabase.com/docs/guides/platform/regions)

### B. Keep an existing RDS or Azure PostgreSQL database

Use the customer's managed PostgreSQL service for Company OS, private S3 or Blob for retained objects, and existing company identity. Put application APIs and workers where they have an approved route to those resources. Vercel, Trigger.dev and n8n can still be considered for selected components, subject to the connectivity and processing boundaries in the deployment plan.

There is no need to add Supabase solely because the system uses PostgreSQL. Application engineers can implement the required API, permissions and storage integration against the existing services. If Supabase-specific capabilities are desired, evaluate a migration or a separately engineered self-hosted stack. **Changing a connection string does not attach the hosted Supabase platform to an arbitrary existing RDS database.** Supabase's documented RDS path transfers data into a Supabase database. [RDS-to-Supabase migration](https://supabase.com/docs/guides/platform/migrating-to-supabase/amazon-rds)

### C. Operate Supabase inside company infrastructure

Self-hosted Supabase is an option for a capable operator on approved AWS, Azure or other infrastructure. It is a collection of services, not a single database container. Plan ingress/TLS, database maintenance, object storage, service secrets, authentication delivery, upgrades, monitoring, backups and recovery.

Supabase documents Docker-based self-hosting and assigns availability, scaling and operational responsibilities to the operator. Its local development stack is not a hardened production deployment; hosted platform features and self-hosted features also differ. Do not promise managed backups, platform administration features or equivalent support merely because the software starts successfully. [Supabase self-hosting](https://supabase.com/docs/guides/self-hosting)

Reusing a separately managed database underneath selected self-hosted services requires explicit compatibility and lifecycle engineering. Evaluate required roles, schemas, extensions and replication privileges with the database owner. This repository does not provide or validate that arrangement.

## 3. Store readable context and saved work deliberately

Use the selected database for structured records: stable source IDs, source URLs, version/time markers, owner, account/project links, permission references, ingestion state, provenance, suggestions and approval status. Store readable transcript/document versions in approved private object storage when retention allows it. Keep timestamped passages linked to both the original source and the retained version.

A saved suggestion should have its author or generating job, supporting source versions, intended audience, expiry/review state and a separate execution record. Approval is a database state transition with an audit event; execution occurs through the authorized action service. A database row marked “approved” is not permission for a general workflow to send messages or change records arbitrarily.

Choose full-text search and, where useful, an approved embedding/vector extension or search service. Embeddings are another retained derivative, not a substitute for readable evidence. The same deletion and access rules must cover text, vectors, summaries, caches and saved results. Provider search features do not determine who is allowed to see a passage.

## 4. Enforce employee permissions across every access path

Map company identities and source ACLs into explicit organization, group, project and item access records. A team label alone cannot express a privately shared call or restricted personnel file. Retrieve only evidence the current user can access, and recheck permission freshness before generating or delivering an answer. If several sources support an artifact, its permitted audience must respect every included source until an authorized publishing process approves a different audience.

PostgreSQL row-level security (RLS) can enforce row access inside the database. Configure grants and policies together. For ordinary user-serving queries, use a least-privilege role that is neither the table owner nor a role allowed to bypass RLS; privileged owners/superusers have different behavior. Pass trusted user context through a carefully designed API, and test pooled connections for identity leakage. [PostgreSQL row security](https://www.postgresql.org/docs/current/ddl-rowsecurity.html)

With Supabase, secure exposed tables and views, and test both allowed and denied operations for every role. Filtering a search result after retrieving unrestricted rows is insufficient: restricted text must not reach the model, worker logs or user response. Custom search functions and vector queries need the same authorization contract. [Supabase RLS](https://supabase.com/docs/guides/database/postgres/row-level-security)

Supabase secret keys and legacy `service_role` keys bypass RLS. Keep them out of browsers and repositories, and restrict privileged jobs. **A key being server-side is not itself authorization:** the API still must validate the caller, action and source access. Prefer user-scoped access or a narrow database role for user requests; isolate ingestion/admin powers. [Supabase API keys](https://supabase.com/docs/guides/getting-started/api-keys)

Private object access needs its own controls, including short-lived download authorization after the same source-permission checks. Supabase Storage uses policies on its storage metadata; those policies still need to reflect Company OS permissions. [Storage access control](https://supabase.com/docs/guides/storage/security/access-control)

## 5. Connections, backups and migration

Select database connections for the actual runtime. A persistent worker and many short-lived web requests have different pooling needs. Supabase documents transaction pooling for serverless connections and currently requires disabling prepared statements for that mode. Confirm the exact driver's behavior, pool size, TLS, network support and migration connection before launch. Never copy a database owner credential into every service. [Connection methods](https://supabase.com/docs/guides/database/connecting-to-postgres)

Back up databases and retained objects separately. Supabase database backups cover storage metadata, **not the actual objects stored through its Storage API**; restoring a database cannot recover a deleted object. Verify selected-plan recovery coverage and test an isolated restore of both kinds of data. [Supabase backups](https://supabase.com/docs/guides/platform/backups)

A provider migration is a delivery project, not just a SQL export. Inventory database versions/extensions, roles/grants/RLS, auth identities and sessions, storage objects and policies, realtime subscriptions, hooks/functions, secrets, URLs and operational jobs. Rehearse restore, reconcile counts and source IDs, prove permissions, coordinate writes at cutover, and retain a rollback plan. Supabase's PostgreSQL migration guide specifically requires additional attention to roles/privileges and RLS. [PostgreSQL migration](https://supabase.com/docs/guides/platform/migrating-to-supabase/postgres)

Before restored data becomes available, reapply current revocations, tombstones and retention decisions. Use synthetic or explicitly sanitized development data. A convenient database branch is still a data copy and needs its own access and deletion policy.

## 6. Procurement and handover checklist

The delivery owner records company-controlled billing/admin accounts; database and object providers; region and transfer boundaries; production/non-production isolation; identity integration; credential owners and rotation; connection and storage limits; backup and restore objectives; support contacts; export procedures; and budget alerts. Estimate database compute, storage, backups, object operations, egress and operational support separately from model and transcription charges.

Acceptance requires a real call-to-evidence flow, a saved suggestion, an authorized approval, denied access for another employee, source revocation propagation, a timed restore and a documented operator handover. A personal AI subscription may help an engineer build this; the chosen runtime services, company credentials and operating responsibilities remain separate.
