# Deployment paths: starting fresh, existing AWS, or existing Azure

**Status: implementation and delivery guide.** The repository runs a local fictional-data demo. The production services, cloud modules, authentication and connectors described here must be built and validated; this is not a turnkey cloud installer. Use [deployment and operations](06-deployment.md) for the production contract and [tools, APIs and subscriptions](12-tools-apis-and-subscriptions.md) for procurement. Use [storage and lifecycle](14-data-storage-and-lifecycle.md) for data storage decisions.

These paths can incorporate managed products. See [platform options and hybrid stacks](15-platform-options-and-hybrid-stacks.md) for Vercel + Supabase + Trigger.dev, optional n8n, and Vercel with an AWS- or Azure-hosted core. That guide specifies responsibilities, network choices and the difference between retaining a file in the company cloud and processing it in an external service.

## 1. Choose the operating model

| Company situation | Starting path | Accountable operator |
|---|---|---|
| No existing cloud environment or platform team | A: establish company accounts, then use managed cloud services or contracted dedicated hosting | Named company owner plus delivery partner |
| Existing AWS organization and platform team | B: deploy inside its approved AWS environment | Customer platform team or agreed managed operator |
| Existing Azure tenant/subscription and platform team | C: deploy inside its approved Azure environment | Customer platform team or agreed managed operator |
| Managed application stack or hybrid cloud | Follow A, B or C for ownership, then select the [managed components](15-platform-options-and-hybrid-stacks.md) and their processing boundaries | Named application owner plus owners of each cloud/provider account |
| Another approved cloud or on-premises environment | Map the same identity, container, database, object, queue and model contracts to that environment | Team responsible for that platform |

Default to a **dedicated customer deployment** with separate production and non-production resources. Preserve existing identity, network, monitoring and billing arrangements where practical. Kubernetes is optional; this design can use managed containers. Companies can connect a mixture of Microsoft, Google and other business tools regardless of the hosting cloud.

A personal AI subscription can help an individual understand, develop and review the software. It is not the company's hosting account, persistent database, source-system authorization or shared model API account. The local demo needs no AI subscription. Production needs its own hosting, organization-owned model service or private inference, and operational ownership. Employees use their browser and company sign-in; they do not each need a personal coding-assistant subscription.

## 2. What people need before delivery starts

| Role | Tools and access needed |
|---|---|
| Business sponsor and data owners | Browser; selected workflows; source inventory; recording/capture policy; budget and retention decisions |
| Employee | Browser, company identity, assigned groups and access to appropriate source records |
| Engineer trying this demo | Git or downloaded source; Python 3.11+; browser; optionally Docker with Compose instead of local Python |
| Production application engineer | Company GitHub organization or approved source-control mirror; approved editor; language runtimes; container build tooling locally or in CI; API development/test accounts |
| AWS platform engineer | AWS CLI, federated company login, approved infrastructure tool such as Terraform/OpenTofu or AWS CDK/CloudFormation; delegated deployment permissions |
| Azure platform engineer | Azure CLI, company login, approved infrastructure tool such as Bicep or Terraform/OpenTofu; delegated deployment permissions |
| Identity/source administrator | Rights to register applications, grant required OAuth scopes/admin consent, configure groups and enable licensed API/recording features |
| Operator | Monitoring and incident tools; authorized restore access; runbooks; escalation contacts; cost dashboard |

Use the customer's existing infrastructure tool. Installing every listed tool is unnecessary. Cloud administrator access does not automatically permit reading SharePoint, Slack, a CRM or call recordings: each source requires its own authorized connection and scope review. Production CI needs its own deployment identity; developers should not supply a shared personal cloud key.

## 3. Path A — a company starting from scratch

1. **Name owners and choose hosting.** Assign a business sponsor, technical operator, billing owner and source owners. Choose company-owned AWS/Azure, an approved managed-service combination, or a delivery partner's dedicated environment. Managed delivery must identify whose account holds data, who pays each bill, support access, export/deletion terms and how the customer takes over.
2. **Establish company accounts.** Create or confirm the company domain, identity provider, GitHub organization, cloud billing account and two accountable administrators. Enable strong administrator authentication and recovery. Keep ownership independent of an employee's personal AI login or credit card.
3. **Set boundaries before buying services.** Choose region, environments, first users, three pilot workflows, source containers, permitted model providers and retention. Estimate documents, call minutes, storage, concurrent users and sync frequency. Use the [data-readiness playbook](08-data-readiness-and-delivery.md) to identify missing capture and disorganized source permissions.
4. **Select a small managed foundation.** Follow Path B or C for containers, managed PostgreSQL, private object storage, a queue, secrets and monitoring. Start with company sign-in and one documents source plus one meeting/CRM workflow. Purchase recording/transcription only where existing tools cannot provide usable exports or APIs.
5. **Fund the production build.** Implement the missing services listed in [the handoff](10-implementation-handoff.md), then provision through reviewed infrastructure definitions. A hosted copy of the current demo is not a real-data pilot.
6. **Prove a complete flow and hand it over.** Demonstrate a permitted call becoming a timestamped transcript, account-linked evidence, cited summary and reviewed task suggestion. Show that another user without access cannot retrieve any derivative. Exercise credential rotation, restore and a disabled employee before inviting the cohort.

**Acceptance artifacts:** organization/account register; signed operating responsibilities; private source inventory; approved data-flow diagram; deployment record; demonstrated call-to-knowledge flow; permission test report; restore report; monthly budget and support contact. The company should be able to keep operating if the original builder leaves.

## 4. Path B — fit into existing AWS

Use the customer's landing zone, account structure, identity federation, naming/tags, security controls and approved regions. Establish whether this is a new workload account or an approved isolated environment within an existing one; do not create an unmanaged account alongside its organization.

| Responsibility | Candidate AWS service |
|---|---|
| API and connector/processing workers | ECS services/tasks on Fargate; approved load balancer and TLS edge |
| Container images | ECR |
| Metadata, permissions, suggestions, approvals and search | RDS PostgreSQL; approved extensions only |
| Versioned transcripts, files and permitted media | Private S3 buckets |
| Work delivery and failed jobs | SQS queues and dead-letter queues; workflow state in PostgreSQL |
| Credentials and encryption | Secrets Manager and KMS |
| Operations | CloudWatch plus the existing security/audit destination |
| Employee access | Existing company identity provider integrated with application login |

The selected services support [managed PostgreSQL with backups and point-in-time restoration](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/CHAP_PostgreSQL.html), [object storage](https://docs.aws.amazon.com/AmazonS3/latest/userguide/Welcome.html) and [durable message queues](https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/welcome.html). Availability, retention and recovery settings still require deliberate configuration.

1. **Collect environment inputs.** Record account IDs, region, network/subnets, DNS zone, certificate process, approved egress route, identity issuer, key policy, logging destination, resource quotas and recovery objectives.
2. **Prepare private delivery configuration.** Write/review the AWS infrastructure modules and separate staging/production parameters. Configure protected remote infrastructure state with access controls and recovery. Establish GitHub Actions OIDC trust restricted to the intended repository and deployment environment; apply production environment rules. [GitHub's AWS OIDC guide](https://docs.github.com/en/actions/how-tos/secure-your-work/security-harden-deployments/oidc-in-aws) explains temporary credentials without stored long-lived AWS keys.
3. **Provision network and durable services.** Create or attach approved private subnets, security groups, database, buckets, queues, secrets, keys and alerts. Confirm DNS and outbound connectivity to SaaS/model endpoints; a private subnet alone does not provide that connectivity. Configure relevant VPC endpoints or approved NAT/proxy routes.
4. **Deploy separated identities and workloads.** Build and scan the production image, push to ECR, apply migrations with a restricted migration identity, then deploy API and workers. Give each worker only its required resources. The [ECS task role](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/task-iam-roles.html) governs application access; the separate [execution role](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/task_execution_IAM_role.html) supports platform duties such as image pull and configured logs/secrets.
5. **Wire company services.** Configure sign-in and source identity mapping; register scoped source applications; resolve secret references at runtime. Select an approved model endpoint independently of compute hosting. AWS hosting does not require every source or model to be hosted on AWS.
6. **Stage, restore, then release.** Reconcile source counts and access, test stale permissions/deletion, measure queue retries and cost, restore database/objects into isolation, and promote the tested image digest. Hand production operations to the named owner.

**Acceptance artifacts:** approved architecture and applied infrastructure revision; account/resource inventory; IAM and source-scope matrix; successful federated CI deployment; model connectivity evidence; ingestion/revocation results; backup and timed restore evidence; alarms with responders; release/rollback record.

## 5. Path C — fit into existing Azure

Use the customer's Entra tenant, subscription governance, naming/tags, resource groups, approved regions, virtual network and cost policies. A resource group helps organize resources; it is not by itself a complete application data-isolation boundary.

| Responsibility | Candidate Azure service |
|---|---|
| API and sustained workers | Container Apps |
| Scheduled or event-triggered finite work | Container Apps Jobs |
| Container images | Azure Container Registry (ACR) |
| Metadata, permissions, suggestions, approvals and search | Azure Database for PostgreSQL Flexible Server |
| Versioned transcripts, files and permitted media | Private Blob Storage |
| Work delivery and failed jobs | Service Bus queues and dead-letter handling |
| Credentials and keys | Key Vault |
| Operations | Azure Monitor/Log Analytics plus existing security tooling |
| Employee access | Existing Entra application sign-in or another approved identity provider |

[Container Apps](https://learn.microsoft.com/en-us/azure/container-apps/overview) hosts containers, while [Jobs](https://learn.microsoft.com/en-us/azure/container-apps/jobs) provide finite executions. The storage choices are [managed PostgreSQL](https://learn.microsoft.com/en-us/azure/postgresql/overview), [Blob object storage](https://learn.microsoft.com/en-us/azure/storage/blobs/storage-blobs-introduction) and [Service Bus messaging](https://learn.microsoft.com/en-us/azure/service-bus-messaging/service-bus-messaging-overview). Confirm selected service tiers, region and network features during design.

1. **Collect environment inputs.** Record tenant/subscription IDs, resource groups, region, virtual network/subnets, private DNS, ingress rules, policy assignments, identity administrator, allowed services and quotas.
2. **Prepare infrastructure and federation.** Write/review Bicep or the existing infrastructure tool's definitions. Use private environment parameters and protected state where the tool requires it. Configure GitHub-to-Azure workload federation and scoped deployment roles following [GitHub's Azure OIDC guide](https://docs.github.com/en/actions/how-tos/secure-your-work/security-harden-deployments/oidc-in-azure). Keep production deployment rights separate from employee sign-in.
3. **Provision durable resources and routes.** Create the container environment, registry, PostgreSQL, Blob, Service Bus, Key Vault and monitoring. Select private endpoints/network integration where supported and required; validate private DNS, image pulls, health probes and approved SaaS/model egress from the actual runtime.
4. **Deploy application and job identities.** Assign managed identities and narrow resource roles; test every permission. [Container Apps managed identities](https://learn.microsoft.com/en-us/azure/container-apps/managed-identity) support identity-based service access. Use it where the target supports it; SaaS OAuth refresh tokens still belong in Key Vault. Configure database identity/roles explicitly when using Entra database authentication.
5. **Deploy and connect.** Build/scan images, push to ACR, run migrations, deploy API/workers/jobs and configure company sign-in. Register source integrations with their actual administrators. Choose an approved model deployment, region, authentication method and quota separately; an Azure subscription does not establish model capacity or permission by itself.
6. **Validate and hand over.** Run the same permission, ingestion, deletion, cost, restore and rollback tests as AWS, then release to the named cohort.

**Acceptance artifacts:** resource/subscription inventory; applied deployment revision; Entra and managed-identity role matrix; private-network/DNS evidence; federated CI run; source/model connectivity evidence; backup/restore report; alerts, release record and operator handoff.

## 6. Shared delivery rules and recurring obligations

**Repository boundary.** Publish reusable application code, generic infrastructure modules when implemented, fictional examples and documentation. Keep customer-specific configuration, infrastructure state, inventories and evidence in access-controlled customer locations. Infrastructure state can contain sensitive values. Commit only secret references; never tokens, private keys, recordings, transcripts or customer knowledge. A private deployment repository still needs secret scanning and controlled CI logs.

**Network boundary.** Allow authenticated application ingress and minimal verified webhook receivers. If inbound webhooks are disallowed, use supported polling or an approved relay and document freshness. Allow runtime egress to configured identity, source, model and telemetry endpoints. A private database and an external model API are separate data-flow decisions; record what content leaves the cloud region.

**Persistent state.** Containers are replaceable. Store metadata, suggestions, review status, execution receipts and workflow checkpoints in the database; retain permitted evidence in private object storage. Apply source-derived permissions and retention to these stored results. Queue retention is not the archival plan. Restore must reconcile newer deletions and revocations before users regain access; follow [the restore runbook](06-deployment.md#restore-from-a-backup).

**Ongoing responsibility.** Assign owners for backups/restores, source credentials, connector changes, identity lifecycle, model budgets, patches and incidents. Budget separately for compute, database, objects, queues, network/private endpoints, logs/backups, model usage, transcription/recording licenses, CI and support. Existing cloud commitments may help with billing, but additional workload usage still has a cost. Review actual spend and coverage after the pilot and periodically thereafter.

The delivery is accepted when a named team can operate, restore, update and offboard the service with company-owned access and documented evidence.
