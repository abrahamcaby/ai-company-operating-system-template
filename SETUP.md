# Set up Company OS with your AI assistant

This is the shared entry point for adapting the AI Company Operating System Template to a particular company. An assistant should act as an interviewer and implementation guide: learn the business, map its tools, identify missing data and capabilities, then help deliver and verify a bounded live workflow.

For a full company setup, begin with the [“Grill me about my company” discovery skill](skills/company-discovery/SKILL.md). It investigates clients, offerings, real processes and exceptions as well as tools, then produces an operating brief and process maps. The [deep discovery modules](docs/20-deep-company-discovery.md) supply follow-up questions. A demo-only or narrowly scoped request can take a shorter path.

**Today:** this repository contains a working fictional local demo, setup materials and production specifications. It does not contain working company sign-in, live connectors or production deployment modules. Guided setup identifies and helps implement those gaps; it must not present configuration questions as a finished installation.

## Start in any assistant

Paste the following into your company-approved assistant. A URL alone may only produce a summary; include the instruction to start setup.

```text
Help me set up this AI Company Operating System Template for my company:
https://github.com/abrahamcaby/ai-company-operating-system-template

Read README.md, SETUP.md and docs/19-guided-company-setup.md before starting.
Use SETUP.md as the setup procedure for this request. Tell me which files
you could actually read and what actions your environment can perform.
Use skills/company-discovery/SKILL.md to grill me about our business,
clients, processes and tools, one question at a time. Reuse prior answers.
Build a tailored connection and deployment plan, then guide or implement
the next authorized step and verify it. Save progress in an approved
private workspace so we can resume. Never ask me to paste API keys here.
Distinguish working demo features, missing engineering and verified live
connections. Start with the first discovery question in SETUP.md.
```

If the assistant cannot open the repository, download or attach this file, [the phase guide](docs/19-guided-company-setup.md), the README and the blank [templates](templates/README.md). Continue discovery from the available material and identify any missing guide needed for the next phase. Do not grant broad company-data access just to read this public template.

For a coding agent, create a company-owned copy of the template, clone/open that copy as its project and give the same setup request. Keep company-specific records in an approved private location even if the software repository is public. The template's default `AGENTS.md` and `CLAUDE.md` provide setup routing; the explicit prompt remains the portable fallback.

## Instructions for the assistant facilitating setup

### 1. Establish your working mode

Confirm what you can actually read, write, run and access. Do not imply that a chat subscription supplies cloud accounts, source permissions or background jobs.

| Available environment | What you can do now | How to handle the next boundary |
|---|---|---|
| Chat with no repository or browsing access | Interview using supplied files; draft a tailored plan and progress record | Ask for the specific missing public guide or a workspace-enabled handoff when needed; never claim to have inspected unread files |
| Chat with repository browsing | Read accessible guides, research selected providers and produce concrete setup instructions | Give the responsible owner one verifiable action at a time; owner reports are not independently observed tests |
| Coding agent with a local checkout | Initialize private worksheets, inspect code, run the fictional demo, implement scoped changes and tests | Use authorized tools and the company's approved development environment; absence of source/cloud credentials is a real boundary |
| Agent with approved company/source/cloud tools | Inspect permitted configuration, implement selected adapters, provision within approved scope and run staging checks | Respect budgets and authority, use scoped identities, keep evidence and verify actual results before advancing |

Report relevant limitations once, then keep making useful progress. A lack of one tool must not prevent independent planning or implementation. Do not ask the user to repeat authorization that already covers the action.

### 2. Start with three discovery topics

If the user has already answered these, summarize the answers and ask only for missing details. In deep discovery, start with the first question and follow its useful branches before moving on; do not ask the whole list at once unless the user prefers a batch:

1. **What does your company sell or deliver?** Then explore whom it serves, who will use Company OS first, and the first two or three questions or workflows it should help with. Ask these follow-ups separately. Give examples only when helpful, such as sales-call conversion, customer handoff or tutoring progress.
2. **Which tools currently hold the information for those workflows?** Start with their names and categories: company files, communication, meetings/recordings, CRM or operational/learning system. “We do not record this yet” and “I do not know” are useful answers.
3. **Are you aiming to explore the demo, prepare an implementation plan, or build a live pilot—and who can help with company IT and deployment?** Ask whether they already use AWS, Azure, another cloud or managed services; do not make them select a stack before understanding the need.

Then give a short understanding of the company, a tentative first workflow and the next question. Use the discovery skill to investigate clients, actual process steps, exceptions and missing context before finalizing the plan. Do not dump the entire inventory or a long purchasing checklist into the first reply. Do not invent answers to make progress appear complete.

### 3. Interview adaptively and preserve decisions

Use [deep discovery](docs/20-deep-company-discovery.md) for the business interview and [the phase guide](docs/19-guided-company-setup.md) for implementation. Investigate client segments, current processes, workflow evidence, source owners, identity and permissions, recordings, data organization, outcome definitions, infrastructure, budget and operational support. Ask one question at a time during deep discovery; use up to three focused questions if the user prefers batches. Explain why a detail matters. Let the user answer in plain language, accept uncertainty, and assign unanswered technical questions to a named role.

Reuse existing systems where they satisfy the requirements. Recommend one concrete starting path with alternatives only where a decision matters. Inventory broadly but connect only the sources required by the chosen pilot. No company needs every logo or service mentioned in this repository.

Treat claims such as “we have Salesforce” or “we use Azure” as starting information. Follow up on the specific objects, accounts, permissions, owners, recording availability and runtime access needed for the selected workflow. Do not equate an application login with a working API connection.

### 4. Keep a private setup workspace

Use an existing approved private workspace when provided. Otherwise, in a local checkout, offer the included initializer as the next useful action and run it when local execution is authorized:

```bash
python3 setup_company.py
```

It creates these blank planning files in `.company/`, preserves existing files and makes no network requests:

- `company-profile.md`: business, workflows, source inventory, boundaries and hosting decisions.
- `process-map.md`: actual process steps, handoffs, tools, exception paths and responsibilities.
- `discovery-notes.md`: answer checkpoints, reporting sources, corrections and unresolved questions.
- `setup-progress.md`: stage, decisions, questions, evidence, blockers and the exact next step.
- `connection-plan.md`: a separate connection card for each required provider and data scope.
- `pilot-acceptance.md`: user journeys, expected allowed/denied results and operational acceptance.

An explicit `--directory /approved/private/path` selects another working folder. The initializer requires Python 3.11+ and does not configure the application, grant permissions, connect APIs or deploy services. `.company/` is excluded from Git and Docker context, but may still be readable to local users, backups or assistant tools; use company-approved storage and processing rules. Never put secrets, recordings or raw customer data in these worksheets.

Without filesystem access, provide updated worksheet text for the user to save in the approved location. State that it has not been saved automatically. Ask for the prior progress record when resuming in a different assistant; do not rely on private chat memory being portable.

Use phase statuses `planned`, `in_progress`, `blocked`, `verified` and `not_applicable`. Record evidence separately as `not_run`, `reported_by_owner` or `observed`. A completed questionnaire, successful command exit or owner's report alone does not prove live permissions or production readiness. Mark a phase verified only when its required evidence has been reviewed and its gate has passed; record who verified it and when.

### 5. Turn discovery into concrete steps

For each chosen source, create a connection card that identifies the exact business purpose, required objects, data owner, administrator, edition/API availability, access model, capture/sync method, adapter implementation status and verification steps. Resolve service choices using [tools and APIs](docs/12-tools-apis-and-subscriptions.md), [deployment paths](docs/13-deployment-paths.md) and the relevant provider's current official documentation.

Do not invent an OAuth scope, callback URL, UI button, deployment command or environment variable. Confirm these against the actual adapter and deployed environment. If the provider adapter or production service does not exist, explicitly create an implementation task with inputs, owner and acceptance tests. Do not label an unbuilt connection as something the user can activate by entering a key.

For each next step, provide: **purpose, responsible person, prerequisites, exact action, expected result, verification method and progress update**. Keep steps small enough that a nontechnical owner can hand a specific task to IT. Where you can act within the user's authorization, do the work rather than only listing instructions. Where you cannot, provide the precise handoff and continue independent work.

When a decision would add cost, expose data, expand permissions, affect production or create an external change, use the user's existing authorization and the host's policy. Resolve missing scope or approval before the dependent action; present a concrete, reviewable change rather than a vague request to proceed. Secret values belong in the company's secret manager or the provider's own authentication flow, never in chat, public issues, screenshots or commits.

### 6. Verify a complete workflow, then hand over

Progress through: **discovery → data readiness → chosen architecture → missing implementation → staging connections → authorized end-to-end pilot → measured results and operated handoff**. The [phase guide](docs/19-guided-company-setup.md) supplies the gates. A local demo is a separate useful milestone, not proof of any later gate.

For a query workflow, demonstrate source ingestion or controlled live access, readable evidence, correct entity links, permitted retrieval, denied retrieval and a cited answer. For a pattern question, add defined outcomes and a reproducible comparison. For a closed loop, add reviewed action, actual delivery evidence and later measurement. Use [the outcome guide](docs/18-company-query-and-learning-loop.md) for sales and tutoring recipes.

Before saying the company service is live, verify company sign-in and offboarding, source revocation/deletion, persistent state, allowed/denied users, runtime independence from the builder's laptop, recovery, monitoring, costs and the named operator. Keep blocked gates visible. If the session ends early, deliver a usable handoff; do not call incomplete engineering “setup complete.”

End each working session with four short items: **what changed, what was verified, what remains blocked, and the next concrete step**. Update the private progress record with the same facts and a resume prompt.

## Assistant instruction compatibility

Repository instruction discovery applies when the tool actually opens the checkout; a pasted URL is not the same thing. Codex uses [AGENTS.md](https://learn.chatgpt.com/docs/agent-configuration/agents-md). Claude Code can import shared guidance through [CLAUDE.md](https://code.claude.com/docs/en/memory). Cursor supports [project rules and AGENTS.md](https://cursor.com/docs/rules). Configuration and higher-priority instructions can affect loading, so confirm the setup guide was read. Ordinary ChatGPT or Claude chat should use the explicit prompt and accessible files above. None of these instruction files creates a company connection or overrides the assistant's authorization controls.
