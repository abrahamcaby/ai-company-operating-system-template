# Validation record

Date: September 17, 2026. Scope: version 0.1 fictional local reference implementation.

## Executed checks

- **36 automated tests passed** on Python 3.12.14. The same suite also passed on the available system Python 3.9.6; the documented supported starting point is Python 3.11+.
- Policy tests covered tenant boundaries, explicit deny, CEO/IT access restrictions, inherited source intersection, missing/deleted/expired sources, cyclic lineage, malformed access metadata, disabled users, revocation and absence of restricted result metadata.
- Workflow tests covered separate-person approval, access and source-version changes, invalid capabilities, cross-tenant requests, current approver authority, idempotent simulation and actor-scoped event visibility.
- HTTP tests exercised the real localhost request boundary: unknown identities, cross-origin/Host rejection, malformed JSON, uniform unavailable-resource responses, static-file allowlisting, served HTML/JS/CSS, and an evidence query followed by proposal, approval and simulated execution.
- Readiness tests covered missing recording evidence, unknown connection, tenant mismatch, stale access snapshots, unverified declarations, malformed shape/timestamps and attempts to bypass call checks by omitting record type.
- JavaScript syntax check passed using Node.js. Python compilation passed.
- The example readiness manifest returned `declarations-complete`, meaning its fictional declarations satisfy the local checker. It is not proof of external connectivity or actual consent/access.
- Independent code review found malformed ACL and readiness-input issues; those were corrected and covered by regression tests.
- Documentation cross-links and package contents were checked before handoff.

## Checks not completed

- **Visual/browser interaction verification:** attempted twice, blocked because the browser tool could not verify its admin-enforced security policy. No alternate browser path was used to bypass that restriction. Responsive behavior, visual layout and complete keyboard/screen-reader operation therefore still need a browser review.
- **Container execution:** Docker/Compose configuration supplied, but no image build or container run verified in this environment.
- **GitHub CI:** workflow supplied, but no remote repository was created and no GitHub-hosted run occurred.
- **Production deployment:** no real identity provider, source system, model provider, cloud resources, recording pipeline, source ACL sync, customer data or external actions were connected or tested.
- **Enterprise controls:** no penetration test, load test, independent compliance assessment, provider sandbox certification, real disaster-recovery exercise or contractual SLA evidence.

## Manual UI acceptance checklist

Before using the demo in an important presentation, run it locally and verify:

1. All five navigation pages load at desktop and mobile widths without clipping.
2. Persona changes immediately remove prior-person evidence, counts, dialogs and query results.
3. Knowledge search/filter, source drawer and cited evidence links work by keyboard and pointer.
4. Sales → CEO proposal/approval/simulation shows the correct status and prevents self-approval.
5. People-only records remain absent from CEO and IT views; Finance evidence remains absent from employee view.
6. Error/empty/loading states are readable; tab focus and dialog dismissal are usable; browser console has no errors.

Passing these checks would validate the demonstration experience. It would not make the planned enterprise implementation complete.

## Documentation update 0.1.1

The September 17, 2026 follow-up adds tools/API/subscription requirements, fresh-start/AWS/Azure deployment paths, storage and saved-suggestion lifecycle, and two intake registers. No application code or test behavior changed. The 36-test result above remains the application baseline; it was not rerun for these documentation-only changes. Internal file links, heading targets, CSV shapes and release archive contents were checked. Provider-specific additions use current official documentation links; no cloud resources, accounts, credentials or APIs were provisioned.

## Documentation update 0.1.2

The next September 17, 2026 update adds managed-service and hybrid stack configurations, a PostgreSQL/Supabase guide, a Trigger.dev/n8n automation guide and an eight-row stack decision register. Provider-specific details were checked against linked official documentation; an independent review found no material deployment or permission overclaims, and workload-federation trust guidance was clarified.

- Checked 115 internal file/heading links with no missing targets.
- Validated all four CSV registers/inventories for consistent columns; the new stack register has eight component rows and fourteen fields.
- Confirmed all fifteen application, web and test files are byte-for-byte unchanged from the 0.1.1 release archive. The existing 36-test baseline was not rerun for this documentation-only update.
- Checked the 51-file release archive for integrity and excluded local databases, caches, credentials and development state.
- No Vercel, Supabase, Trigger.dev, n8n, AWS or Azure resources were provisioned or tested. Their integrations, infrastructure and operational acceptance remain future implementation work.

## Naming and documentation update 0.1.3

The project is named **AI Company Operating System Template**. The main README now explains company ownership and replication; a plain-language overview and documentation README provide capability summaries and audience-specific reading paths. The demo's title, navigation label and persona preference key were updated. The preference-key change starts a fresh saved persona selection in browsers that ran an earlier release.

- Checked 177 internal file/heading links with no missing targets and validated the CSV shapes.
- Confirmed all eleven backend and test files are unchanged from 0.1.2. The existing 36-test baseline was not rerun for the documentation and interface-label changes.
- JavaScript syntax validation passed after the title/preference-key changes. Browser verification remains unavailable because the browser tool could not verify its administrator-enforced policy.
- Reviewed publication contents for secrets, private paths and customer data; none were found in the 53 intended files. Local databases, caches and development state are excluded.
- No GitHub-hosted CI run has been verified for this release. The supplied workflow should be checked after publication.
