# Deep company discovery: understand the business before configuring tools

Use this interview when a company wants Company OS tailored to how it actually works. It expands discovery in [SETUP.md](../SETUP.md) and [the guided setup playbook](19-guided-company-setup.md). The objective is a company-confirmed operating picture, a small set of valuable workflows and the evidence needed to build them. It is not a questionnaire to send all at once.

An AI assistant should be curious, specific and willing to challenge vague answers respectfully. It should learn the company's clients, offerings, processes, decisions and vocabulary before recommending an architecture. A list of software subscriptions is not an understanding of the company.

## How to conduct the interview

1. Read the existing private profile and progress record. Reuse prior answers and approved decisions; ask only about missing, ambiguous, contradictory or materially changed details.
2. In deep discovery, ask **one focused question at a time** and wait for the answer. If the user prefers a faster batch, ask no more than three related questions per round. Start with the business and the desired result; follow a concrete example before broadening the inventory.
3. Explain the reason for an unfamiliar question in one short sentence. Offer relevant examples, but do not lead the owner into adopting an invented process.
4. After each topic, reflect back the specific understanding and the remaining uncertainty. Invite correction without asking for a redundant approval at every step.
5. Probe answers that change the design. Accept `unknown` where the respondent is not the owner, assign the question to the right role, and continue independent discovery.
6. Preserve every nonsecret question and answer in the private discovery notes, including corrections. Distinguish the respondent's answer from the assistant's interpretation. On a pause or session boundary, save the next question and a resume note.
7. Stop discovery when the bounded readiness gate below is met. Do not make the company document its entire business before it can test one useful workflow.

The user can choose a short first pass, a deep interview for one workflow, or a broader operating review. Recommend the deep interview for the proposed pilot first, then extend it where shared data or handoffs affect the result. The assistant should keep a topic coverage list rather than forcing a fixed number of rounds.

### Opening sequence

If these facts are not already known, ask the first question below, then adapt after the answer. Do not ask the sequence all at once unless the user chooses batch mode:

- “What does your company sell or deliver?”
- “Who are the customers for that offering?”
- “What makes a customer relationship successful here?”

Once the business is clear, ask which recurring decision or process the assistant should improve. Follow that with a request for a recent anonymized example, then trace the people and tools involved one step at a time.

Then follow the answer. For a sales question, learn the offer and buying journey before requesting CRM configuration. For a tutoring question, learn the learning goals and assessment process before selecting a recording API. For an internal knowledge question, identify real employee questions and authoritative owners before proposing a new database.

## Maintain a private, structured record

Use an approved private workspace; the default local working folder is the ignored `.company/`. Follow [the setup privacy rules](19-guided-company-setup.md#keep-company-answers-private-and-portable). Do not request credentials, private customer files or identifiable transcripts in chat. Ask for aliases, nonsecret descriptions and approved private evidence references.

| Artifact | What discovery adds |
|---|---|
| [Company profile](../templates/company-profile.md) | Business model, offerings, clients, roles, vocabulary, priorities, constraints and source inventory |
| [Discovery notes](../templates/discovery-notes.md) | Each question and answer, evidence basis, corrections, checkpoints and the next question |
| [Process map](../templates/process-map.md) | A repeatable map for each selected process: triggers, steps, owners, handoffs, evidence, exceptions and outcomes |
| [Connection plan](../templates/connection-plan.md) | Only the sources and destinations actually needed by the selected workflows; exact technical requirements are researched later |
| [Setup progress](../templates/setup-progress.md) | Topic coverage, confirmed decisions, assumptions, contradictions, outstanding owner questions and resumption steps |
| [Pilot acceptance](../templates/pilot-acceptance.md) | Concrete questions, expected results, allowed/denied users and the proof needed for a useful live pilot |

Duplicate the process-map sections for each important process, or save clearly named copies such as `.company/processes/customer-handoff.md` inside the private workspace. Record the relationship to the company profile instead of maintaining conflicting copies of the same fact.

Use the shared statuses `planned`, `in_progress`, `blocked`, `verified` and `not_applicable`. Record the evidence basis separately as `not_run`, `reported_by_owner` or `observed`. A business owner can confirm the interview readout while a source connection remains untested. Verifying that a definition was approved does not verify that historical records follow it.

At each topic checkpoint, show a short synthesis and invite corrections. Promote confirmed business facts into the company profile or process map with their discovery-note references; keep unconfirmed interpretations visibly labeled. Corrections supersede earlier answers without silently rewriting the interview history. Required deletion or removal of an accidentally disclosed secret takes precedence over preserving an answer; retain only an appropriate nonsecret correction/removal note.

## Adaptive question bank

Choose the questions that resolve the next meaningful uncertainty. This bank is for the facilitator; do not paste it as a mass questionnaire. Skip answered or irrelevant sections, record why a topic is outside scope, and return to it only if a later dependency requires it.

### 1. Company, offering and economics

Understand what the company promises and the work required to fulfill that promise:

- What are the main products, services or programs? Which are standardized, customized, recurring or one-time?
- Who is the buyer, who uses the service, who pays and who measures success? Are these different people or organizations?
- How is the offering priced: subscription, per user, per session, fixed project, usage, outcome or another basis? Which exceptions or discounts matter to the pilot?
- What event creates a commitment to deliver? What event counts as booked, invoiced, paid, delivered, renewed or refunded?
- Which constraints determine capacity or profitability: staff time, seats, inventory, tutor availability, delivery deadlines or something else?
- What strategic priorities or company-specific differentiators should the assistant preserve when making suggestions?

Ask for approved ranges or structural rules rather than confidential price lists or customer financials when those values are unnecessary. Keep similarly named metrics separate; “revenue” may refer to several distinct business events.

**Record:** offering definitions, business units, customer roles, commercial lifecycle, important constraints and the owners of authoritative definitions.

### 2. Client segments and the buying journey

Map how different customers enter, buy, receive value and leave:

- Which client segments behave differently enough to change the workflow? What defines a segment in actual records?
- How do prospects or learners arrive: referrals, marketing, outbound, partners, applications or an existing account?
- What are the real steps between first contact and commitment? Who qualifies, evaluates, approves and signs off?
- What information is handed from sales/admissions to onboarding or delivery, and what commonly gets lost?
- How does the company know the customer received value? Who notices dissatisfaction, cancellations, refunds or a stalled account?
- Which segment has a different journey, purchase cycle, service level or permission boundary? Does the first pilot include it?

For business-to-business services, distinguish account, contact, opportunity, contract and project. For tutoring, distinguish buyer/guardian, learner, tutor, enrollment, lesson and assessment. Use the company's vocabulary, and map it to stable records later.

**Record:** a short lifecycle for the pilot segment, entry/exit events, accountable roles, key records and excluded journeys.

### 3. Walk through the actual process

Ask the owner to describe a recent ordinary case with identifiers removed. Walk it forward one step at a time rather than accepting a department-level summary:

- What triggered the work? Who noticed it, in which tool, and what exactly did they do next?
- What input did they need? Where did it come from, and what did they do if it was missing?
- Which judgment, rule or approval changed the path? Who could make that decision?
- What record, message or other output proved the step was complete? Where was it saved?
- Who received the handoff, how were they notified, and how did the sender know it was accepted?
- What are the normal wait times, volume and recurring deadlines? Where are reminders or spreadsheets filling a gap?

Build a step table in the [process-map template](../templates/process-map.md) while interviewing. The first pass describes what people actually do, including work outside official systems. Capture the desired process separately so the assistant does not mistake an aspiration for current behavior.

Then request one difficult or unsuccessful case: an unqualified lead, missed session, failed payment, reassigned owner, incomplete brief, disputed assessment, cancellation or equivalent. Ask where it branched, who recovered it, what was recorded and how the outcome differed.

**Record:** trigger, finish condition, each actor/tool/input/output, decision points, ownership transfers, timing, workarounds and at least one relevant exception path.

### 4. Tools, ownership and hidden handoffs

Investigate software through the work it supports:

- Which exact tool and workspace holds each step's authoritative record? Is another tool merely a copy, notification or report?
- Who owns the business data, who administers the account and who maintains the workflow? Are they the same person?
- What is manually copied between tools? Which fields or identifiers survive the handoff, and what becomes free text?
- Which scheduled exports, integrations, forms or automation workflows already move the information? Who sees failures?
- Does the work also happen in inboxes, spreadsheets, private channels or a person's notes? Is that material eligible for company use?
- What happens when an employee changes role or leaves? Which accounts or integrations depend on that individual?

Do not ask for API scopes or make the company buy new tools at this point. Record edition/API availability as unknown where needed; an administrator can verify it during connection planning. A personal login proves neither application access nor permission to disclose its contents to coworkers.

**Record:** system of record per object/field, business/admin owners, existing flows, manual transfers, stable IDs and dependencies on individuals.

### 5. Context, policies and unwritten knowledge

Find what an experienced employee knows that a new assistant would otherwise miss:

- Which procedures, service promises, playbooks, lesson standards or decision rules guide this work? Where is the current approved version?
- Which terms have a company-specific meaning? What do “qualified,” “active,” “complete,” “improving” or “at risk” mean here?
- What exceptions do experienced staff handle from memory? Who can explain or approve the rule?
- Which document wins when a slide deck, chat message and operating procedure disagree? Who resolves the conflict?
- Which current priorities, constraints or commitments must answers take into account? When should that context expire?
- What must always go to a human even when the assistant has relevant evidence?

Distinguish approved policy, a manager's preference, a historical practice and a proposed change. Store reviewed context with an owner, authoritative source, version, audience and review date. Do not turn one interviewee's opinion into company policy.

**Record:** glossary, source hierarchy, policy owners, review cadence, missing context and decisions that require human judgment.

### 6. Evidence quality, recordings and entity links

Test whether the evidence exists in a usable form before promising answers:

- What is captured today, what is missing and what is only recorded for certain teams or customers?
- If recordings matter, which calls or lessons are recorded, under what approved process, and where are usable transcripts and timecodes stored?
- Are transcripts understandable enough for the selected analysis? Who can review speaker attribution, language errors or missing sections?
- What stable identifiers join the call to the opportunity, the lesson to the learner, or the project to the client? Who resolves uncertain matches?
- How are corrections, duplicates, deletions, access changes and late imports handled? How fresh does the answer need to be?
- Which outcomes are absent or inconsistently entered? Does “blank” mean unknown, pending, ineligible or something else?

Use a small approved private sample to check readability and linking. Track what can be observed directly versus what the owner reports. If capture is missing, define a prospective collection plan; do not invent a historical dataset. For sensitive calls or lessons, establish approved recording and audience rules before enabling capture.

**Record:** source coverage, quality gaps, naming/ID rules, capture process, reviewers, freshness requirements and a remediation task for each blocking gap.

### 7. Decisions, metrics and the learning loop

Move from “AI should find insights” to a defined decision and measurable result:

- What exact question should a permitted employee be able to ask? What would they do differently after a good answer?
- Which result distinguishes success from failure? Who owns its definition and authoritative data?
- What is the unit being compared: opportunity, client, learner-course, project or another entity? What time window and outcome maturity make the comparison fair?
- Which cohorts or segments should be compared, and which are too different to combine? What happens to open, missing or incomplete outcomes?
- How will a proposed improvement be reviewed, delivered and recorded? Who checks later whether it helped?
- What result would cause the company to stop, revise or retire the recommendation?

For sales, separate activities, closed-deal win rate, cohort conversion, bookings and collected cash. For tutoring, separate session engagement, assessment change and reported school grades. Ask which is actually measured instead of choosing a convenient proxy silently.

Use [the query and learning-loop guide](18-company-query-and-learning-loop.md) for analytical design. Record hypotheses as hypotheses; ordinary before/after differences do not prove a cause. A measured loop may remain pending after the query workflow is usable because later outcomes have not matured.

**Record:** decision, metric definitions, observation window, baseline, data dependencies, approved intervention owner, measurement date and success/stop criteria.

### 8. People, access and communication cadence

Determine who should learn what, when, and through which approved channel:

- Which roles need the first view: executives, managers, individual contributors, operations, clients or guardians? What question does each role ask?
- Which source, client, team, region, learner or financial fields must remain restricted? Are temporary staff or guests involved?
- Who can view a finding, propose a change, approve it and execute it? Does the destination have a broader audience than the source?
- Which meetings or reporting routines should the assistant support? What changes between an on-demand question, a weekly digest and an urgent alert?
- What freshness and delivery cadence are useful? What would create noise or disclose information to the wrong recipient?
- How are access reviews, role changes and offboarding handled today?

Inventory the reporting routine as part of the workflow: meeting purpose, participants, inputs, decisions, action owners and follow-up evidence. Do not assume every meeting needs a recording or every finding should be posted to a shared channel.

**Record:** role-to-question map, audiences, restrictions, action authority, cadence, delivery destinations and ownership of identity changes.

### 9. Constraints and opportunities

Only after the business map is sufficiently clear, resolve delivery choices:

- Which existing company systems, contracts, cloud services and support teams should an implementation reuse?
- What operating budget, timing, capacity, residency, retention or customer commitments constrain this pilot?
- Who can implement missing components and who will operate them after launch? What work is currently dependent on one person?
- Which problem has enough value, evidence and ownership to test first? Which attractive idea should wait because its data or authority is missing?
- What failure would make the pilot unacceptable, and what fallback should staff retain?

Rank candidate workflows using expected business value, evidence readiness, permission complexity, engineering effort, operational burden and reversibility. Show the reasoning; avoid a fabricated precision score. Recommend one bounded pilot and explain why it is a useful first step toward wider company coverage.

**Record:** chosen pilot, deferred opportunities, existing services to investigate, explicit constraints, accountable sponsor/builder/operator and outstanding architecture decisions.

## Probe vague answers and contradictions respectfully

| Answer or conflict | Useful follow-up |
|---|---|
| “Everything is in our CRM.” | “Walk me through the last handoff. Which record contains the call evidence, agreed scope and delivery acceptance? Where is anything missing?” |
| “Everyone needs access.” | “Which roles need which answers? Are pricing, personnel, learner or client-specific records treated differently today?” |
| “We want to automate onboarding.” | “What event starts it, what is the first action, and what proves onboarding is complete? Tell me about one case that needed an exception.” |
| “Our clients are all different.” | “Which differences actually change the steps, decisions or access? Let's map the most common path and one meaningful variation.” |
| “Our students improve.” | “Which comparable measure shows the change, when is it collected, and where are the baseline and follow-up linked to the same learner?” |
| “Sales owns the handoff,” but delivery disagrees | “What does each team consider accepted? Let's record both definitions and have the accountable owner resolve the boundary.” |
| A policy says one thing; a recent case shows another | “Is this an approved exception, an outdated policy or a process gap? Who can establish which behavior should guide the assistant?” |

Avoid accusatory questioning. Label the issue as an unresolved definition, source conflict or missing evidence. Preserve both versions with their owners and references. Do not silently choose the more convenient account or mark a conflict resolved because the interview moved on.

## The discovery gate: a confirmed business readout

Present a concise readout in the company's own vocabulary before detailed technical setup:

1. What the company offers, whom it serves and how the selected journey creates value.
2. How the pilot process works today: trigger, major steps, owners, handoffs, exception and finish condition.
3. What the company assistant should answer or help do, for which roles, using which evidence and outcome definitions.
4. What existing tools and context will support it, what data is missing and where permission boundaries apply.
5. Which assumptions or contradictions are still open, who owns each and whether it blocks the first pilot.
6. The proposed first workflow, measurable acceptance condition, exclusions and next small setup action.

Ask the business owner to correct or confirm the readout and selected scope. This is a factual alignment checkpoint, not a fresh request for permission to perform work already authorized. Record the owner's confirmation and any corrections. It does not authorize access to unrelated systems or substitute for technical verification.

Discovery is sufficient when a builder can understand the process without guessing its actors, evidence, important decision rules, outcome or audience; the sponsor agrees on a useful first result; and remaining unknowns have named owners and clear impact. Block detailed work only where the missing fact changes its safety or correctness. Continue independent preparation instead of seeking perfect information.

Then return to [guided setup](19-guided-company-setup.md): remediate data gaps, research the selected providers, prepare connection cards, implement missing services and verify a live workflow. Reopen only the relevant discovery topics when implementation reveals new facts.

## Pause and resume without starting over

Update the private discovery notes and progress record with topics covered, the current process-map location, confirmed definitions, unresolved conflicts, evidence checked and the next question. Record a next batch only if the user chose batch mode. Include owner referrals and any facts that will expire or need revalidation.

A resuming assistant reads these records, summarizes the current understanding briefly and continues from the first unanswered dependency. It should not repeat the full intake, treat a previous assistant's assumption as fact, or claim a live connection exists because a provider name appears in the profile.
