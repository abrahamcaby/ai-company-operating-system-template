# Jobs and automation: Trigger.dev, n8n and cloud-native alternatives

**Status: architecture and delivery guidance, verified against vendor documentation on September 17, 2026.** These integrations are not implemented in the demo. This guide explains what a production builder must select, configure and test. Read it alongside [deployment paths](13-deployment-paths.md), [integrations](04-integrations.md) and [storage and lifecycle](14-data-storage-and-lifecycle.md).

Company OS needs reliable work outside an employee's browser: collect a recording, wait for transcription, refresh permissions, produce a cited draft and request review. The company can buy that runtime as a managed service or operate it inside AWS, Azure or another approved environment. Its personal AI subscription does not provide this shared runtime.

For the full Vercel/Supabase/AWS/Azure combinations and network choices, start with [platform options and hybrid stacks](15-platform-options-and-hybrid-stacks.md).

## 1. Choose the job that each tool owns

| Option | Suggested Company OS responsibility | People maintaining it |
|---|---|---|
| Trigger.dev | Engineering-owned tasks: ingestion, extraction, transcript processing, scheduled briefs, retries and model pipelines | Application engineers |
| n8n | Visual workflows connecting business systems: event collection, routing, notifications and approved handoffs | Trained operations builders with engineering review |
| Both | n8n collects an event; the core API authorizes and dispatches a durable task; completion returns a reference for a permitted notification | Named owner for each boundary |
| Existing orchestration platform | Keep the company's supported workflow engine and implement the same contracts | Existing platform team |

These are recommended divisions of responsibility, not restrictions on either product. Choose one initially unless there is a clear need for both. A visual connector does not automatically import a source's access rules, preserve transcript timestamps or match a call to the correct CRM account. Those remain explicit requirements of the [integration contract](04-integrations.md).

Trigger.dev supports task runs and configurable retry attempts; waitpoint tokens allow a task to resume after an external event. Use this for transcription completion or review notification. A completed waitpoint only resumes work: Company OS must independently verify any approval and authority to execute. Keep callback URLs secret because a Trigger.dev waitpoint callback can complete without an API key. [Runs](https://trigger.dev/docs/runs), [waitpoint API](https://trigger.dev/docs/management/waitpoints/create).

## 2. Managed services can work with AWS and Azure

**AWS example:** keep Company OS records in RDS PostgreSQL and recordings in S3. Host the core API in the customer's AWS account. A managed Trigger.dev task or n8n workflow calls a narrowly scoped API, which checks the workload identity and returns only permitted information. The website can be hosted separately. This architecture is a proposed combination, not a preconfigured integration in this repository.

Trigger.dev currently documents AWS PrivateLink connectivity from its tasks to customer resources through an internal Network Load Balancer and endpoint service. It is a Pro/Enterprise feature. This supplies a private network route; task execution remains in Trigger.dev's environment. Connections are organization-scoped, so isolate production from preview/staging with application credentials and network design rather than assuming the connection itself separates environments. [Trigger.dev private networking](https://trigger.dev/docs/private-networking/overview).

**Azure example:** keep the core API, PostgreSQL and Blob Storage in the company's approved Azure environment. A managed workflow can call an approved authenticated endpoint if that data flow is allowed. Otherwise place processing inside the customer's environment using self-hosted orchestration or Azure-native jobs. Do not assume the documented AWS PrivateLink offering also provides an Azure private connection; establish the supported route before purchase.

For either cloud, list four locations separately in the data-flow record:

1. Where the application and workflow definitions are administered.
2. Where task code executes and can access plaintext.
3. Where inputs, outputs, checkpoints and logs are stored.
4. Where models, transcription and other downstream services process information.

A database remaining in AWS or Azure does not keep data inside that boundary if an outside worker fetches the transcript. Prefer opaque artifact IDs and on-demand authorization. Where temporary download references are necessary, make them short-lived, audience-appropriate and unlogged; expire and reissue after a long wait. References reduce exposure but do not erase the data-processing boundary.

## 3. What self-hosting actually requires

### Trigger.dev

Trigger.dev offers Docker Compose and Kubernetes deployment guides. Its self-hosted architecture separates the web application/control services from the supervisor and task runners. The current comparison excludes Cloud checkpoints, automatic scaling and warm starts from self-hosting. Budget for the resources consumed by long waits, and test recovery behavior for the selected version instead of assuming Cloud behavior. Operators own security, uptime and upgrades; pin compatible platform and CLI versions. [Self-hosting overview](https://trigger.dev/docs/self-hosting/overview).

The Kubernetes guide describes PostgreSQL, Redis, ClickHouse, object storage and a container registry, with external-service configuration. It recommends an external registry for production. Select compatible managed dependencies where supported, separate application and orchestration database credentials, and validate backups, certificates, networking and image access. AWS EKS or Azure AKS are candidate homes for the documented Kubernetes route; matching the customer's cluster policies still requires deployment engineering. [Kubernetes guide](https://trigger.dev/docs/self-hosting/kubernetes). The [Docker guide](https://trigger.dev/docs/self-hosting/docker) is useful for evaluation but explicitly does not cover a complete production deployment.

### n8n

For a production queue-mode design, plan for the main process, worker processes, shared PostgreSQL, Redis, and ingress routing. Workers need access to the same database and broker. Share the instance encryption key securely across main, workers and webhook processors. Distributed queue mode is not supported with SQLite. Multi-main high availability is a separate Enterprise feature; adding workers alone does not provide it. The queue guide warns against filesystem binary storage in queue mode. [Queue-mode documentation](https://docs.n8n.io/deploy/host-n8n/configure-n8n/scaling/enable-queue-mode).

Keep recordings in Company OS object storage and pass IDs through n8n whenever possible. If n8n itself must persist binary data, current documentation provides S3 and Azure Blob external storage on self-hosted Business/Enterprise plans, not Community or n8n Cloud. Binary data needs the documented object lifecycle policy. n8n's external execution-data storage has different pruning rules, so do not apply a blanket deletion rule across both. [External storage](https://docs.n8n.io/deploy/host-n8n/configure-n8n/scaling/use-external-storage).

n8n encrypts stored credentials using its instance encryption key. Back up the key through the customer's secret-management process separately from the database and test recovery; a database backup alone is insufficient. [Encryption-key configuration](https://docs.n8n.io/deploy/host-n8n/configure-n8n/basic-configuration/configuration-examples/set-a-custom-encryption-key).

## 4. A complete call-to-suggestion workflow

The following is the proposed implementation contract:

1. An approved recording provider emits a completion event. Verify its signature, establish the tenant and connection, and record a stable event ID. Polling is an alternative when the source supports it.
2. Resolve source permissions, meeting owner, recording policy, account/project association and transcript availability. Quarantine missing or conflicting metadata. The recorder, meeting license and transcription API are separate services; neither orchestration product records every call automatically.
3. Create one durable ingestion job. Store the source revision, workflow version, correlation ID, idempotency key and expected output. Retry transient failures with bounded backoff; send unresolved failures to an owned review queue.
4. An authorized worker obtains only the required artifact, transcribes if needed, preserves speakers/timecodes, and stores the approved transcript version in private storage. Commit its permissions before making it searchable.
5. Generate a cited draft under the intended user's or team's effective access. Save its evidence dependencies, model/prompt versions, uncertainty and review state. Scheduled executive briefs require the recipient's current permissions too.
6. Notify the reviewer with an access-checked link. Keep restricted transcript content out of broadly visible channels. Record the review in Company OS; waiting for a reply is not an authorization system.
7. If a CRM update or task creation is proposed, create a separate action proposal. The execution service rechecks approval, expiry, current source access, target permissions and the exact payload immediately before writing. Record the provider's receipt and reconcile uncertain outcomes before retrying.

**When using both products, assign one retry owner per operation.** n8n may retry delivery of an event to the core API; the API deduplicates it and returns the same job ID. Trigger.dev then owns processing retries. n8n must not separately rerun the same CRM write because it has not received a callback. Store an application-level operation ledger and provider idempotency key where supported. A task framework's idempotency window is not a permanent exactly-once guarantee for external effects. [Trigger.dev idempotency](https://trigger.dev/docs/idempotency).

Both runtimes should invoke the core's policy and action APIs through scoped workload identities. Do not issue a general company administrator token to a workflow. Staff allowed to edit workflows or inspect executions may see secrets or business data indirectly; treat orchestration administration as privileged access.

## 5. Stored data, editions and delivery model

Company OS remains the governed record of evidence, saved suggestions, approvals and execution receipts. Orchestrators store workflow definitions and execution state; they can also retain payloads, outputs, logs and credentials. These are additional copies requiring their own access and retention inventory.

For n8n, configure which successful, failed and manual executions are saved and set pruning deliberately. Its pruning excludes running/waiting and annotated executions, so examine those separately. Test error paths: an exception can expose content even when successful-run logging is minimal. [Execution-data management](https://docs.n8n.io/deploy/host-n8n/configure-n8n/scaling/manage-execution-data). Trigger.dev's current self-hosting table says log retention does not automatically expire; a customer needs a supported, tested deletion/retention strategy before ingesting sensitive information. [Self-hosting limits](https://trigger.dev/docs/self-hosting/overview#limits).

Do not assume free n8n self-hosting includes company governance. Its Community comparison excludes projects, SSO, external secrets, workflow/credential sharing, Git-based version control and other paid features. Confirm the exact plan for the required RBAC, identity and operational controls before procurement. These administrator permissions still do not enforce original CRM/file permissions inside Company OS. [Edition comparison](https://docs.n8n.io/deploy/host-n8n/community-edition-features).

Distinguish **a company deploying its own internal OS** from **a provider hosting a product for many client companies**. n8n's license examples allow internal company synchronization and consulting on company instances; they distinguish app backends that collect end-user source credentials. [Official license explanation](https://github.com/n8n-io/n8n-docs/blob/main/docs/privacy-and-security/sustainable-use-license.md). Its licensing FAQ says hosting client workflows and credentials requires an Enterprise license, and embedding its UI/workflows requires an embedding agreement. Settle the applicable commercial terms with n8n before selling that architecture; self-hosting and hiding the editor do not establish permission. [Licensing FAQ](https://support.n8n.io/article/can-i-use-your-license-for-my-use-case).

## 6. Alternatives and acceptance

If the customer already operates another system, retain it when it meets the same requirements:

| Candidate | When to evaluate it |
|---|---|
| Temporal Cloud or self-hosted Temporal | Complex durable application workflows and an engineering team to own workers. Temporal explicitly separates its coordinating service from customer-deployed workers. [Production deployment](https://docs.temporal.io/production-deployment) |
| AWS Step Functions | An AWS-centered estate needing service orchestration and long-running human-interaction workflows. Select the appropriate workflow type and validate external effects separately. [AWS overview](https://docs.aws.amazon.com/step-functions/latest/dg/welcome.html) |
| Azure Durable Functions | An Azure-centered estate needing code-defined stateful orchestration and managed workflow state. [Microsoft overview](https://learn.microsoft.com/en-us/azure/durable-task/durable-functions/durable-functions-overview) |

Before release, demonstrate duplicate-event deduplication, worker failure/recovery, provider throttling, expired artifact links, revoked source access during a wait, and an uncertain external-write result. Confirm one business action occurs, or that an unresolved outcome is quarantined. Restore the orchestration database and its required secrets in isolation; verify execution retention and source deletion across every copy. Handover must identify the workflow owner, runtime operator, failed-job responder, monthly cost owner and tested upgrade/rollback procedure.
