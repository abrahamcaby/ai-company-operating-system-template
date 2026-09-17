# Engineering handoff: what to extend and what to replace

## Shipping reference components

| Component | File | Behavior and limit |
|---|---|---|
| Demo fixtures | `app/seed.py` | Nine selectable fictional people, one hidden cross-tenant test identity, thirteen source/derived records. No customer import. |
| Policy | `app/policy.py` | Active user, tenant match, explicit grants, deny precedence, current ACL expiry, and recursive lineage intersection. Corrupt lineage fails closed. No privileged CEO/admin content bypass. |
| Service | `app/service.py` | Applies policy before ranking or extracting text; no shared answer cache. SQLite stores simulated actions and actor-scoped events. |
| HTTP | `app/server.py` | Local-only Host checks, same-origin API boundary, fixed static-file allowlist, no-store headers, JSON size/type validation. Demo header is intentionally impersonable. |
| Connector contract | `app/connectors.py` | Typed record/access/change-page protocol only. There are no implemented provider adapters. |
| Readiness | `app/readiness.py` | Local shape/declaration checks including recording metadata and permission evidence declarations. It does not verify external facts. |
| Interface | `web/` | Persona changes clear prior evidence; request generations suppress stale UI responses. Text rendered with DOM text nodes. |

The policy's concepts are reusable; the built-in HTTP server and demo identity header are not a production application stack. SQLite events are editable local demo state, not immutable enterprise audit storage. Python protocol definitions do not automatically enforce a provider's permission behavior.

## Demo API

All routes after the public health/persona catalog require the `X-Demo-User` header. This exists solely to demonstrate access differences. Production must derive a principal from a verified server-side session and current directory state; it must not accept caller-selected user/tenant/group values.

| Method | Path | Result |
|---|---|---|
| GET | `/api/health` | Demo mode health |
| GET | `/api/demo/users` | Public fictional personas |
| GET | `/api/workspace` | Current user's documents, static planned adapter catalog, own authorized events and capabilities |
| GET | `/api/documents/{id}` | Authorized document; unavailable/missing uses identical 404 |
| POST | `/api/ask` | `{question}` → keyword-selected authorized evidence and citations |
| GET | `/api/actions` | Own actions or reviewable actions whose source remains accessible |
| POST | `/api/actions` | `{document_id, kind: "create_task", title}` → proposed simulation |
| POST | `/api/actions/{id}/approve` | Separate authorized reviewer records approval |
| POST | `/api/actions/{id}/execute` | Recorded reviewer runs idempotent simulation after current-access/version checks |

No API exposes secrets, content ingestion, tenant administration, financial transactions, media recording, live connectors or real tool execution. Action titles are arbitrary fictional demo labels. A production proposal requires exact destination, payload, policy revision, evidence versions, recipient audience and execution budget; a label is not enough for approval.

## Recommended implementation work packages

Deliver these in dependency order. Track each as an issue with an owner, a testable acceptance condition and a customer/provider scope.

1. **Production identity and tenancy.** Choose the customer's identity provider, implement verified OIDC sessions, membership updates/offboarding and separate application/content privileges. Prove wrong issuer, expired token, disabled user and cross-tenant requests fail. Replace the demo selector entirely.
2. **Production data plane.** Implement transactional canonical schema, non-owner runtime role, permission indexes/RLS defense, private object storage, migrations and current-access checks. Carry source versions, lineage and deletion state through every derivative. Prove no unauthorized title/snippet/count/export.
3. **First connector.** Choose one actual customer system and bounded container scope. Implement provider auth, stable identity mapping, authoritative ACLs, change cursors, backfill, retries, deletion and reconciliation. Pass provider sandbox tests, then limited customer UAT.
4. **Meeting/call pipeline.** Use existing approved recording/transcript availability first; build ingestion/normalization and account/project resolution. Quarantine unsupported permissions or uncertain identities. Prove the call is findable by allowed users with timestamps and invisible to denied users.
5. **Retrieval and model gateway.** Authorize candidates before hybrid search/reranking; route approved evidence only to the configured company model provider. Track prompt/model/version, citations and costs. Return unavailable/insufficient evidence instead of inventing facts. Evaluate prompt injection and model-provider failure.
6. **Maintained knowledge.** Generate draft entity, project and decision pages in constrained schemas. Maintain field/claim provenance and permission partitions. Review material changes, invalidate descendants after source changes and retain revision history subject to deletion policy.
7. **Real action engine.** Implement one allowlisted capability, durable states, exact payload previews, approval expiration, destination-audience checks, execution identity, idempotency, provider receipts and unknown-outcome reconciliation. Recheck source access and target write authority at execution.
8. **Scheduled work.** Create jobs with explicit owner, audience, scope, timezone, budget and freshness policy. Re-evaluate every recipient at run time; stop or narrow output when access or source coverage changes. Delivery channels are separate integrations with separate permissions.
9. **Operated deployment.** Build customer-cloud infrastructure modules, CI/CD, secrets, telemetry, backup/restore, runbooks, release gates and support ownership. Perform a restore and permission-revocation exercise before production use.

Use [architecture](03-architecture.md), [security](05-security.md), [deployment](06-deployment.md) and [pilot milestones](07-roadmap-and-economics.md) for full acceptance criteria. Do not ship unimplemented capabilities under the demo's working labels.

## Extension example: adding an existing custom system

1. Classify what it supplies: files, messages, recordings, structured records, identity or actions.
2. Read the provider's current API/export contract; record auth, scope, quotas, licensing, ACL granularity and deletion/change support.
3. Implement `Connector` behind the production worker, with one server-configured tenant/connection context. Keep provider tokens in the secret manager.
4. Normalize records into stable tenant/connection/external-ID/version identities. Preserve field/row restrictions; if access cannot be reproduced, quarantine or ingest only an explicitly approved shared collection.
5. Run the common contract suite and provider-specific edge tests. Mark the adapter supported only for the tested API/object/permission scope.
6. Publish customer setup instructions including prerequisites, scopes, backfill expectations, freshness envelope, disconnect behavior and owner responsibilities.

MCP can expose controlled operations, but a tool protocol does not provide identity mapping, retention, billing or permission correctness by itself. A generic HTTP connector must never be treated as universal enterprise compatibility.
