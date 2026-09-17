# Product experience, teams, and adoption

The following is a proposed product experience, except for the section explicitly describing the current fictional demo. Team names define useful default views; production permissions must come from company identity, source access, explicit grants, and resource policy. A person can belong to several teams. Changing the visible workspace must not grant additional access.

## The shared experience

Every user receives a home view with their priorities, relevant changes, pending approvals, and scheduled work. Search and questions share an evidence panel: source owner, original link, relevant passage or recording time, freshness, and known gaps. Project and account pages connect only the records visible to that user. Users can save useful work to a named audience, and see that audience before publication.

A workflow panel shows the intended destination, proposed changes, approver, and current state. Useful states include drafted, awaiting approval, running, completed, failed, and canceled. “Completed” requires confirmation from the destination system. If a source is unavailable, the product shows which part of the answer is incomplete. If access is denied, it avoids exposing the restricted item's title or existence through detailed error text.

Users can correct a claim, report a bad answer, request a review, or identify the owner of an approved page. Feedback creates a review item with evidence. It does not rewrite the underlying source without that source's normal authority.

## Team and user views

| View | What the person comes to do | Typical authorized evidence | Scope and controls |
| --- | --- | --- | --- |
| CEO / executive | Review performance, strategic decisions, material risks, and cross-team commitments | Approved leadership metrics, executive meetings, business reviews, financial summaries, portfolio status | Explicit leadership scope; private HR, legal, and personal content requires its own grant |
| Sales | Prepare for a customer meeting, understand deal history, draft follow-up, identify missing commitments | Assigned CRM accounts and opportunities, authorized sales recordings, enablement files, relevant project records | Account/team scope; approved pricing only; review before customer communication or material CRM changes |
| Customer success | Prepare renewal reviews, connect support issues to commitments, track onboarding | Assigned accounts, support tickets, success plans, handoff notes, customer meetings | Customer portfolio scope; do not expose another customer's material or internal restricted negotiation notes |
| Operations / project management | Identify blockers, reconcile status, track owners and dependencies | Project tasks, delivery plans, approved meeting decisions, team channels, operating procedures | Project/team scope; proposed task creation and due-date changes carry evidence and an owner |
| Marketing | Find approved messages and media, understand recurring customer themes, prepare content | Brand library, campaigns, approved research, publication rights metadata, shareable customer insights | Approved media and audience scope; customer recordings are not automatically reusable testimonials |
| Finance | Explain governed results, investigate exceptions, prepare close follow-ups | Accounting records, approved reporting models, purchasing records, authorized contract terms | Entity/ledger and field restrictions; numeric calculations use validated queries; payment authority remains separate |
| People / HR | Answer policy questions, coordinate onboarding, maintain restricted HR processes | Published employee policies, onboarding checklists, explicitly permitted HR records | Published policies available broadly; compensation, performance, and case records have narrower scopes |
| IT / security | Manage identity, connector health, source coverage, budgets, incidents, and audit requests | Configuration, operational metadata, access reports, scoped security evidence | Administrative role does not imply content access; support sessions require separately authorized scope |
| Employee | Find current policies, prepare meetings, locate expertise, complete assigned work | Company-published knowledge, own projects and meetings, granted team spaces | Personal drafts and preferences remain private; no access to colleagues' private assistant history |
| Guest / partner | Collaborate on a specifically shared deliverable or project | Explicitly shared project artifacts and approved published answers | Named scope, expiry, limited tools and export; no company-wide people search or inherited internal access |

Menus can hide irrelevant work, but the server must enforce the same access rules for search, chat, recordings, links, exports, notifications, and direct requests. A user receiving a link must be authorized independently. A shared conversation cannot preserve evidence that its current readers are no longer allowed to access.

## Representative workflows

| Workflow | Inputs and reasoning | Output and responsible person |
| --- | --- | --- |
| Weekly executive brief | Approved metric definitions plus current CRM, project, finance, and leadership records; compare against the prior reporting period | Evidence-backed changes and decisions needed; chief of staff reviews distribution and missing coverage |
| Customer meeting preparation | Account identifiers connect CRM history, authorized call transcripts, open support issues, and delivery milestones | A meeting brief with time-linked customer statements and unresolved questions; account owner decides next steps |
| Meeting to action | Authorized recording or transcript, attendee context, project records, and existing actions | Proposed decisions and assigned tasks; meeting owner confirms interpretation and task owners before write-back |
| Sales to delivery handoff | Agreed scope, approved contract facts, CRM records, discovery calls, and delivery plan | A shared handoff with commitments, exclusions, risks, and open questions; sales and delivery owners sign off |
| Project risk review | Current tasks plus relevant team discussion and meeting decisions | Candidate risks with evidence and confidence; project owner confirms status and any escalation |
| Approved content reuse | Rights metadata, published product facts, brand assets, approved customer evidence, and campaign plan | A draft asset and usage rationale; marketing owner reviews accuracy, rights, and destination |
| Finance exception review | Governed ledger/report queries, purchasing data, authorized invoices, and agreed thresholds | Exception list with reproducible figures and record links; finance owner investigates and approves follow-up |
| New employee onboarding | Published policies, role/team context, granted project pages, and onboarding tasks | A role-specific checklist and cited answers; People owns policy accuracy and manager owns assignments |

The first workflows should be useful without broad autonomous write access. A workflow can save a reviewed brief or prepare proposed tasks before it earns permission to perform repeatable, low-risk actions. Incoming transcripts do not authorize messages, task assignment, or a change in an accounting system.

## What the current fictional demo shows

The starter uses “Meridian Works” and a fictional Atlas renewal. It provides nine persona views: CEO, Sales, Finance, People, IT, employee, Operations, Customer Success, and Marketing. Its evidence queries select fixture text by keyword; they do not call a language model or live service. Connector tiles describe planned adapters. Recording references are text examples, not playable customer recordings or a recording feature.

1. Open the CEO view and find company priorities, the all-hands, the Atlas CRM snapshot, approved finance figures, and the leadership review. The restricted People case is not part of this audience.
2. Open Sales and search for Atlas. The CRM record and fictional call evidence describe a security addendum and a requested implementation owner. These are fixture statements; the UI is not reconciling a live forecast.
3. Compare Customer Success with Sales. Customer Success can access the handoff and sales evidence supporting the compiled Atlas brief. Sales alone cannot read that combined brief when it lacks access to the handoff source. This illustrates why an apparently company-wide derived page still needs every source permission.
4. Propose a task using permitted evidence, move it through the review steps using an eligible approver, and execute the approved proposal. Execution is simulated inside the starter; it creates no task in an outside project tool.
5. Open Finance, People, and IT in turn. Finance sees the cash snapshot; People sees its restricted synthetic case; IT sees its connector runbook and management view. IT administration does not reveal business recordings or the People case.

The persona selector is a demonstration convenience, not company sign-in. There is no guest persona UI or interactive source-revocation UI in this starter. Policy checks and the pilot acceptance script must cover revoked evidence and access boundaries. A passing fixture test is evidence about the local policy example, not proof that a live provider's revocation has propagated.

## Target pilot story after production implementation

Repeat the Atlas narrative with authorized pilot data after implementing identity, adapters, ingestion, model access, and operational controls. The account owner prepares a cited meeting brief; Operations reviews a proposed task; a destination-system receipt confirms successful creation. Finance verifies figures against its reporting source. A guest receives only an explicitly published project scope. An administrator checks connector health without content access.

Finally, revoke the test meeting's source access and verify that search, transcripts, compiled pages, cached answers, future exports, and subsequent workflow runs lose that evidence within the agreed revocation objective. Previously downloaded files cannot be reliably recalled. Test direct links and a second user as well as search. This is a planned acceptance script, not functionality exposed by the current demo UI.

## Ownership and adoption

Start with one company workspace, two collaborating teams, a small approved corpus, and three concrete questions those teams already struggle to answer. A proposed initial wedge is customer handoff and project follow-through because it joins meetings, files, CRM, and tasks around a visible outcome. Keep finance and HR expansion separate until their owners approve the required access model.

| Accountable role | Ongoing responsibility |
| --- | --- |
| Executive sponsor | Outcome, funding, priorities, and decision on broader rollout |
| Product owner | Workflow usefulness, feedback triage, adoption, and roadmap |
| IT / platform owner | Deployment, identity, reliability, connector lifecycle, backup, and incident response |
| Data/source owner | Approved scope, authoritative records, retention requirements, and access changes |
| Knowledge steward | Review disputes, stale pages, entity matches, and publication requests |
| Workflow owner | Allowed actions, approvers, success criteria, budgets, and handling failed runs |
| Team champion | Real examples, onboarding, support, and measured workflow feedback |

Establish a baseline before a pilot: preparation time for the chosen workflow, time spent finding evidence, handoff rework, and missed commitments. During the pilot, measure whether people successfully complete those tasks, whether citations support the answers, how often answers need correction, freshness coverage, denied-access behavior, and cost per completed workflow. Track weekly repeat use by the target roles; raw message volume is a weak proxy for business value.

Proposed rollout gates are evidence-based: source owners approve the corpus; permission tests pass; the selected workflows work on real authorized records; employees can identify sources and report mistakes; failed connector and recovery paths are exercised; and accountable owners agree that the measured benefit warrants expansion. Wider autonomy requires its own workflow evidence. No fixed number of installed connectors substitutes for those gates.

The shareable repository should let a company evaluate the story with fictional data, understand the permission model, inspect the deployment and connector plan, and distinguish working code from proposed capabilities. That is the foundation for a credible company conversation.
