---
name: company-discovery
description: Interview a company in depth about its business, clients, tools and current processes, then turn the answers into attributable context and a tailored Company OS setup plan. Use for company onboarding or requests to grill the owner about the business.
---

# Grill me about my company

Build an accurate operating picture before recommending connections or automation. This is discovery for the AI Company Operating System Template, not permission to access company systems. Honor narrower requests; do not restart discovery for a demo-only request, bug fix or already-scoped implementation task.

## Load the relevant context

1. Read [SETUP.md](../../SETUP.md) for working mode, private artifacts and delivery boundaries. Reuse the approved private company profile, discovery notes and setup progress; initialize blank worksheets through the documented helper when useful and authorized.
2. Use the relevant modules of [deep company discovery](../../docs/20-deep-company-discovery.md), progressively. Do not dump or ask every question in the bank.
3. Read the [delivery playbook](../../docs/19-guided-company-setup.md) when discovery can support the first tailored connection and implementation plan.

If files are inaccessible, identify the missing public material rather than implying it was read. An ordinary chat assistant can follow this skill when the user explicitly supplies it. The repository's AGENTS.md/CLAUDE.md route supported coding agents here; do not promise a universal slash command or automatic skill installation.

## Interview as an investigator

Begin with what the company does, whom it serves and what it wants to improve. Reuse prior answers and relevant approved documents. Select the most consequential unanswered area next. **Ask one question at a time by default**, preferably following a concrete recent, anonymized example through the business. Use a small batch only if the user prefers it.

Probe answers until they can inform a design:

- “We use a CRM.” Which system, for what objects and process steps, maintained by whom, and what remains outside it? Explore these as successive follow-ups.
- “We serve enterprises.” Distinguish buyer, user, purchased problem, client segments and how delivery or access changes between them.
- “Onboarding is automated.” Walk through the last onboarding from trigger to completion, then investigate owners, tools, approvals, manual work, failure paths and completion evidence.
- “We want better outcomes.” Establish the measured outcome, definition owner, baseline, time window, authoritative source and unknowns.

Explore actual workflows before desired workflows. Separate what normally happens from exceptions, a reported belief from supporting evidence, and current practice from a proposed improvement. Ask who can resolve uncertainty. Challenge apparent contradictions respectfully and preserve both claims until an owner resolves them; never silently choose one and call it a fact.

Focus depth where an answer changes the required context, connections, audience, workflow or acceptance measure. Do not pursue irrelevant financial/personnel detail or block independent progress because a noncritical fact is unknown. Assign unknowns to an owner and continue the useful branch.

## Checkpoint every answer

When writing is available in an approved private workspace, append each material answer to `discovery-notes.md` with a capture ID, date, question, faithful nonsecret answer, reporting source, evidence basis and allowed audience. Read back the saved entry to verify persistence. If an answer contains unnecessary sensitive material, retain a minimized summary and private evidence reference instead. Tell the user when the record is a paraphrase.

Keep the original statement and append later corrections with a superseding reference. Maintain a running synthesis that distinguishes owner-confirmed reported facts, tentative ideas, assistant proposals, evidence-backed observations and unresolved questions. Owner confirmation of an interview statement is not proof that an API or control works.

Without file tools, return a compact checkpoint for the owner to save and state that it is not saved automatically. Never claim durable memory from the conversation alone. On pause or stop, save or provide the last checkpoint and next exact question, then honor the user's request.

## Produce usable company context

Maintain these private artifacts instead of burying discovery in chat history:

- `company-profile.md`: business operating brief, offerings, client segments and buying roles, terminology, priorities, actual systems and owners, audiences and constraints.
- `process-map.md`: one repeated map per important workflow, including trigger, steps, system of record, inputs/outputs, decision rights, handoffs, exceptions and success evidence.
- `discovery-notes.md`: interview evidence, linked corrections, open questions and module checkpoints.
- `setup-progress.md`: coverage, unresolved contradictions, decisions, owners and the next question or action.
- `connection-plan.md`: required data/API capabilities tied to actual process steps and business questions, separating existing integrations from missing adapters.
- `pilot-acceptance.md`: useful question/action journeys, expected allowed/denied behavior and measured results.

Give durable claims source or reporting-owner references, dates, evidence state, audience and review triggers. Publish only owner-reviewed, appropriately scoped context into the company's maintained knowledge; do not silently promote guesses or temporary ideas into canonical company facts. Filled worksheets stay in approved private storage, not in the public template.

At the end of each module, summarize your understanding, surface a consequential gap and invite correction. Offer an interim readout after several rounds. Let the user resume later or continue with documented unknowns where the next work does not depend on them.

## Continue from discovery to delivery

Discovery can support a first implementation plan when there is an owner-confirmed business description, meaningful client segmentation, at least one end-to-end current process, its actual tools/data/owners, intended users and access boundaries, a testable first result, and explicitly owned unknowns. Broader company discovery can continue alongside that bounded pilot.

Present the operating brief and process maps. Explain the setup implications: which context must be maintained, which connections serve which steps, which capture/data gaps must be fixed, which permissions differ, what must be built, and how the workflow will be judged. Link recommendations to the answers that justify them.

Carry that readout into SETUP.md and the delivery playbook. Continue authorized implementation or provide exact administrator/builder handoffs. Do not end with only a questionnaire or claim a completed installation from an interview. The progression is **understand the company → organize context → design the first workflow → connect/build → verify → measure and improve**.
