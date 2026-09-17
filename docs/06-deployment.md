# Deployment and operations plan

**The only runnable deployment in this repository is the localhost demo described in the README.** The production topology and runbooks below are an implementation specification. They are not an already tested Terraform module, production container image or one-click installation. Customer credentials and documents must not be added to the demo.

For a starting-from-scratch, existing AWS or existing Azure setup sequence, read [deployment paths](13-deployment-paths.md). The [tools and API checklist](12-tools-apis-and-subscriptions.md) explains required accounts and the personal-subscription boundary; [storage and lifecycle](14-data-storage-and-lifecycle.md) defines retained data and suggestions.

For Vercel, Supabase/PostgreSQL, Trigger.dev and n8n—including combinations with existing AWS/Azure—read [platform options and hybrid stacks](15-platform-options-and-hybrid-stacks.md). Managed components can fit within any ownership model below; their processing boundaries must be recorded separately from the location of the main database.

## 1. Deployment choices

| Mode | Appropriate use | Ownership and tradeoff |
|---|---|---|
| Local fictional demo | Product review, permission examples, early discovery | No real authentication or external connections; no customer data |
| Customer-cloud single tenant | Default production direction for customers with an IT/cloud owner | Customer owns cloud account, source apps, identity provider and API bills; delivery team operates under a documented access agreement |
| Provider-operated dedicated tenant | Customer wants managed operations but isolated resources | Separate deployment/data boundary; provider operates backups, upgrades and support, with region and access terms agreed |
| Multi-customer SaaS | Future scale after dedicated deployments prove the product | Requires tenant onboarding, hard isolation, per-tenant encryption/quotas, billing, deletion and incident blast-radius testing |
| Restricted/private model environment | Customer's data processing policy prohibits approved external API calls | Requires compatible local model, embedding/transcription quality tests, accelerator capacity and an operational owner |

Keep the application portable through OCI containers, PostgreSQL migrations, object-storage and queue interfaces, OIDC/SCIM, and replaceable model/connector adapters. Infrastructure-as-code modules should implement the customer's chosen cloud. A cloud migration still needs identity, networking, storage, queue and model policy validation; portability is not a promise of zero migration work.

## 2. Reference production topology

Deploy in one agreed region, with database high availability and application replicas appropriate to the customer's availability target. Separate development, staging and production accounts/projects or equivalent strongly isolated environments. Use synthetic data in development. Production-derived test fixtures require an explicit sanitization process and owner.

| Need | AWS candidate | Azure candidate | Google Cloud candidate |
|---|---|---|---|
| API / application workers | ECS on Fargate | Container Apps | Cloud Run services/jobs or worker pools, as applicable |
| Relational metadata/search | RDS PostgreSQL | Azure Database for PostgreSQL | Cloud SQL for PostgreSQL |
| Private objects | S3 | Blob Storage | Cloud Storage |
| Durable work | SQS plus workflow state in database or dedicated engine | Service Bus plus persistent workflow state | Pub/Sub / Cloud Tasks plus persistent workflow state |
| Secrets and keys | Secrets Manager / KMS | Key Vault | Secret Manager / Cloud KMS |
| Metrics / logs | CloudWatch plus chosen telemetry backend | Azure Monitor plus chosen telemetry backend | Cloud Monitoring/Logging plus chosen telemetry backend |

These are candidate mappings, not equivalent defaults or validated regional configurations. Confirm region support, networking, message delivery semantics, data retention and cost in the selected account. Container platform documentation: [Amazon ECS](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/Welcome.html), [Azure Container Apps](https://learn.microsoft.com/en-us/azure/container-apps/overview), [Cloud Run](https://docs.cloud.google.com/run/docs/overview/what-is-cloud-run).

Separate runtime identities and queues for: API reads; connector synchronization; parsing/embedding; scheduled compilation; optional write execution; migrations; backup and restore. Grant access only to needed secrets and data paths. Do not give the browser cloud credentials or source refresh tokens.

## 3. Network and access contract

- Public ingress terminates TLS at the application edge. Only the authenticated application and minimal verified webhook receivers are externally reachable. Apply request-size, rate and timeout limits.
- Databases, queues and object stores use private access where supported. Disable public object access. Media playback and exports use an authorization proxy or tightly scoped short-lived links created only after authorization.
- Egress uses the customer's approved proxy/NAT or private endpoint path. Allow only configured source APIs, identity endpoints, model providers and necessary observability destinations. Restrict arbitrary fetches in parsers and model tools.
- Prefer cloud workload identities over long-lived cloud keys. Keep source OAuth refresh tokens in the secret manager with per-connection access and rotation. Document every outward data flow, including embedding and transcription.
- Administrative access uses company identity, MFA, least privilege and audited temporary elevation. Production shell/database access is exceptional and recorded. No shared developer account.
- An environment without public webhook ingress can use supported polling or a narrow ingress relay; publish the changed latency/freshness contract. Do not expose the database to accommodate a connector.

## 4. Implementation deliverables before first real install

The delivery team must supply the following; they are not completed by this starter:

1. Production authentication integration and server-side session enforcement replacing the demo identity selector.
2. Production API/server build, immutable container images, software inventory, automated dependency/security checks and an authenticated health/readiness design.
3. Reviewed schema migrations with tenant constraints, permission indexes, RLS policies and separate runtime/migration roles.
4. Durable queue/workflow integration, secret manager adapter, object storage adapter and model gateway with budgets.
5. At least the selected pilot connectors, each with manifest, provider sandbox evidence and permission/revocation tests.
6. Infrastructure modules for the chosen cloud, remote protected state, networking, alerts, backups and secrets references.
7. CI/CD workflow that builds once, scans, signs where supported, deploys to staging, runs gates and promotes the same image digest.
8. Restore, rollback, deletion and incident exercises with customer-approved owners and evidence.

Recommended production configuration keys include `TENANT_ID`, `REGION`, `OIDC_ISSUER`, `OIDC_CLIENT_ID`, `SESSION_KEY_SECRET_REF`, `DATABASE_SECRET_REF`, `OBJECT_STORE`, `QUEUE_ENDPOINT`, `MODEL_ROUTE_POLICY`, `CONNECTOR_ALLOWLIST`, `ACL_FRESHNESS_POLICY`, `AUDIT_SINK` and `BUDGET_POLICY`. Values referring to secrets resolve at runtime; secrets never belong in Git. The demo does not implement these settings.

## 5. First customer deployment sequence

| Step | Owner | Completion evidence |
|---|---|---|
| Define pilot and data scope | Sponsor + domain/data owners | Three concrete workflows, selected source containers, excluded classes, intended users, baseline measurements; use [readiness intake](08-data-readiness-and-delivery.md) |
| Establish operating agreement | Customer IT/security + delivery lead | Hosting region, named operators, model routes, budget, incident contacts, retention, recovery targets and support access |
| Provision isolated environments | Platform engineer | Reviewed infrastructure plan, applied state, private storage/database, environment-specific identities, no production secret reuse |
| Configure identity | Customer identity administrator | Test users/groups provisioned, disabled-user test, guest policy, session revocation and source identity mappings |
| Deploy base services | Delivery engineer | Pinned image versions, successful migrations, healthy services, quota enforcement and audit ingestion |
| Connect narrow source scopes | Source administrator + connector engineer | Exact granted scopes, connection owner, test account, successful permission comparison and revocation tests |
| Backfill and review | Data owners + connector engineer | Coverage report, excluded/quarantined items, index count reconciliation, freshness limits and approved first knowledge artifacts |
| Run acceptance tests | Pilot users + security/reliability owners | Golden question set, access denial matrix, adversarial source test, budget test and restore exercise |
| Open the pilot | Sponsor + delivery lead | Named cohort, training, support channel, feedback ownership and documented stop conditions |

Rollout should allow a source, capability or user cohort to be disabled independently. Start read-only. Enable an action class only after its exact preview, approval, execution and verification paths pass staging and customer acceptance.

## 6. Operational targets and alerts

Agree targets per customer before signing a production SLA. The following are proposed initial engineering targets for a pilot, not measured current performance:

| Signal | Initial target / action |
|---|---|
| Application availability | Measure against a proposed 99.5% monthly pilot objective; use a higher contracted target only after architecture and operations support it |
| Authorized search latency | p95 below 3 seconds on the agreed corpus/concurrency; answer generation tracked separately by model route |
| Content freshness | Source-specific target such as 15 minutes for supported events; show actual source coverage and timestamps |
| Permission freshness | Hard expiry per source/class; alarm and fail closed before exceeding the approved limit |
| Queue backlog | Alert when oldest revocation job exceeds 30 seconds; content backlog threshold based on freshness contract |
| Connector health | Alert on auth failures, missed webhook renewals, exhausted quotas, invalid cursor and reconciliation drift |
| Model quality/cost | Track citation validity, abstention, human corrections, tokens, transcription minutes and spend per accepted workflow |
| Backup/recovery | Proposed RPO 1 hour and RTO 4 hours for pilot; validate with a timed exercise before relying on these figures |

Record metrics by tenant, connection, capability and version without logging confidential text. Only authorized administrators can see sensitive operational metadata. Alerts need an owner and a clear response; a dashboard alone is not operations.

## 7. Routine and failure runbooks

### Source token revoked or permission sync stalled

1. Mark the connection degraded and stop new jobs using invalid credentials.
2. Expire affected permission snapshots according to policy; deny resources whose current access cannot be proven. Cancel dependent scheduled deliveries and optional actions.
3. Show a coverage notice to authorized users without revealing restricted content. Notify the named source administrator.
4. Restore authorization through the source's supported flow, verify source tenant/scopes and increment the connection generation.
5. Reconcile permissions and deletion state before resuming retrieval; then catch up content and rebuild affected artifacts.

### Model outage or budget limit

1. Stop retries that exceed the request deadline/budget. Return an explicit unavailable status while preserving authorized source search where possible.
2. Use a fallback route only if it is approved for the same tenant, region, content class and purpose.
3. Keep pending approved actions unexecuted if a prerequisite is missing; do not regenerate a materially different payload under an old approval.
4. Report route errors, cost and backlog, then replay only idempotent jobs after service is healthy.

### Deploy and roll back

1. Use expand/contract migrations so the previous image can run during rollout. Back up before a destructive migration and test restoration in staging.
2. Deploy a canary with synthetic authenticated probes plus authorized-source fixture checks. Never use a privileged probe that bypasses the user policy being tested.
3. Compare error rate, authorization denials, latency, queue processing and cost to the release baseline.
4. On failure, stop new action workers, roll the application image back and retain queued work. Do not blindly reverse a migration or external side effect.
5. Reconcile any actions in `executing`/`unknown`, then resume when policy/schema compatibility is confirmed.

### Restore from a backup

1. Declare a restore incident and record the intended recovery point. Disable incoming actions and connector ingestion; preserve current audit and deletion ledgers in a protected location.
2. Restore database and required object versions into an isolated environment. Use credentials that cannot send external messages or perform writes.
3. Replay deletion, tombstone, hold and revocation records newer than the backup. Reconcile active identities, source access, connection state and secret references; do not trust old sessions or permissions.
4. Validate tenant boundaries, sampled object hashes, source version references, policy revisions and accounting-report definitions. Rebuild indexes from authorized current metadata if needed.
5. Reconcile workflow state against external systems using idempotency keys. An action that ran after the backup must not run again.
6. Test disabled-user and deleted-resource access, source coverage and recovery-point loss. Record elapsed time and any gap from RPO/RTO.
7. Open read traffic first, then synchronization, then separately approved action workers. Obtain the designated incident commander's release decision and retain the exercise/incident report.

Perform scheduled restore exercises and repeat after material storage, policy or workflow changes. A successful backup job does not prove recovery works.

## 8. Customer handoff and exit

Deliver deployment state ownership, version inventory, connector manifests, identity mappings, runbooks, recovery evidence, on-call contacts, cost dashboard, known limitations and upgrade policy. Confirm the customer can rotate credentials, disable the service and export approved knowledge without a particular employee's account.

For exit, stop schedules/actions, export authorized company-owned artifacts with provenance, revoke source/model credentials, disable identities, apply retention/deletion policy and document residual backups and their expiry. Keep only contractually permitted audit evidence. GitHub remains the distribution channel for code and generic configuration; it is not a storage location for customer transcripts, source documents or secrets.
