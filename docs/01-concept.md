# From a personal AI OS to a company operating system

This is a proposed product design for a company-owned application. It is not a claim that the accompanying starter implements every capability described here. The product brings approved company knowledge, current business records, and controlled work into one interface, with a different authorized view for each person.

## What the source ideas contribute

Nate Herk describes the Four Cs of an AI OS: context, connections, capabilities, and cadence. His AIS-OS repository provides local operating manuals, setup and maintenance skills, and an emphasis on proving that information can be found and workflows actually run. The supplied video transcript shows how he combines business knowledge, meetings, media, and connected tools into a personal working environment. The repository identifies the Four Cs framework as Nate Herk's trademark; attribution belongs with the framework. [Nate Herk's AIS-OS](https://github.com/nateherkai/AIS-OS)

Andrej Karpathy's LLM Wiki proposes maintaining an interlinked synthesis alongside raw sources: information is organized when it arrives, useful answers can become durable knowledge, and periodic checks surface stale or conflicting claims. Its source/wiki/schema separation offers a useful starting pattern. It is an idea for a personal knowledge base, including a possible team use case, rather than a specification for identity, access control, or production operations. [Karpathy's LLM Wiki](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f)

These sources are inspiration, not runtime instructions or copied implementation. The supplied transcript's model claims and installation walkthrough do not establish enterprise requirements. Everything below is our proposed enterprise extension.

## The product promise

A person should be able to ask, “What changed, what matters, and what should I do next?” and receive an answer supported by material they are permitted to use. They should be able to open the original evidence, resolve uncertainty with the owner, and request a controlled action in the relevant business tool.

The company owns the deployment, identities, connector configuration, retained data, workflow definitions, and business model-provider relationship. Employees sign in through company identity. A founder's account, laptop, or personal AI subscription is not the production service boundary. A model is a replaceable service behind the application, with company-approved credentials, usage limits, and processing arrangements.

The application becomes an operating layer over existing systems. CRM remains responsible for opportunities; accounting remains responsible for ledger entries; project tools remain responsible for work items. The OS combines their context and routes work back to them. That reduces the need to maintain conflicting duplicate records.

## Translating the Four Cs

The column labels below use Herk's attributed framework; the enterprise requirements are our design proposals.

| Dimension | Proposed company implementation | Acceptance evidence |
| --- | --- | --- |
| Context | Owned company, team, account, project, and policy pages with review dates, source references, and publication states | An employee can find the current policy and identify its owner and effective date |
| Connections | Approved adapters with scoped access, identity mapping, source permissions, freshness status, and deletion handling | A revoked document disappears from retrieval and affected derived answers |
| Capabilities | Versioned workflows with declared inputs, allowed tools, limits, accountable owners, and approval requirements | A requested task produces a reviewable result and a recorded destination outcome |
| Cadence | Scheduled or event-triggered workflows with explicit audiences, budgets, retry rules, and quiet behavior when unchanged | A scheduled brief reaches only its intended audience and records its source coverage |

## Two forms of knowledge, one permission boundary

Use a compiled wiki for durable understanding: product definitions, decision histories, approved process explanations, account context, and recurring themes. Use current retrieval for changing facts: opportunity stage, invoice status, latest meeting, ticket state, project date, and cash position. The answer service chooses sources according to the question and states the relevant “as of” time.

For example, “Why is the Atlas renewal at risk?” can use an approved account page to explain the relationship, CRM to establish the current deal stage, a project record for a dependency, and timestamped meeting evidence for the customer's stated concern. The explanation should distinguish a reported concern from a verified cause. If the accounting connection is stale, the answer must not present an old balance as current.

The compiled layer is a derivative of evidence, not an authority that can silently overrule it. Each claim needs provenance, source version, effective time where known, last verification time, owner, and a state such as proposed, approved, disputed, or superseded. A policy becomes approved through the policy owner's process; a model finding the same sentence in several meetings does not make it company policy.

Compile within access boundaries. A summary combining restricted meeting notes and a public company page remains restricted to people allowed to read the supporting material. Do not create one unrestricted “company brain” and ask the model to hide sensitive sentences afterward. A broadly published summary requires deliberate owner review and an explicit publication decision. Source deletion, access revocation, or supersession must invalidate dependent summaries, embeddings, graph edges, cached answers, and future exports according to the retention design. Already downloaded files cannot be reliably recalled; control their audience before export.

## What “central” means

The central system holds identity-aware indexes, source links, entity relationships, approved knowledge, workflow state, and audit history. It may retain normalized source content where permitted and useful. It does not need to copy every recording, mailbox, finance table, or media file into one storage bucket.

For large media, retain authorized metadata, transcript segments, and time references; load or stream the original through its authorized source when needed. A text transcript and a thumbnail can disclose sensitive content, so both need the recording's applicable restrictions. For finance, obtain governed records and validated measures rather than asking a language model to invent arithmetic from narrative notes. A metric should show its definition, period, currency, and authoritative owner.

Link entities with stable source identifiers. Two companies named “Atlas” are not automatically the same account. Proposed matches can go to a steward for review. A relationship graph helps users explain connections, but must omit unauthorized node names, edges, counts, and tooltips. A useful search result and evidence panel matter more than a decorative graph.

## Boundaries that make the product credible

- The CEO receives a broad, explicitly granted business view. This does not imply access to every private conversation, personnel record, investigation, or privileged legal matter.
- IT administrators can manage connectors, identities, budgets, and system health without automatically reading underlying business content. Exceptional support access is separately scoped and audited.
- A private draft stays private until its author shares it. Workgroup knowledge does not silently become company-wide memory.
- External content can contain instructions. Ingestion treats them as data, and no source text can grant permissions or authorize an action.
- Automated work runs as a designated principal with an owner. It cannot inherit an absent executive's unrestricted context or distribute a private answer to a public channel.
- Sensitive writes use explicit workflow gates. Approving a draft is separate from authorizing payment, changing compensation, exporting a customer list, or publishing externally.

The first release should prove these boundaries on a narrow set of sources and workflows. Claims such as “connect everything,” “knows the whole company,” or “enterprise-ready” should follow demonstrated coverage and operating evidence, not lead the product description.
