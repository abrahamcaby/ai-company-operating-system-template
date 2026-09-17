# AI Company Operating System Template documentation

Start with the [overview](00-overview.md) for the product's purpose, current demonstration and remaining implementation work. The [repository README](../README.md) explains how to run the local fictional demo. Architecture and platform guides describe a proposed production service; they do not claim that its connectors or cloud resources are already implemented.

## Reading paths

| Reader or task | Suggested sequence |
|---|---|
| Business sponsor evaluating the idea | [Overview](00-overview.md) → [team experience](02-product-and-teams.md) → [roadmap and economics](07-roadmap-and-economics.md) |
| Company preparing its information and calls | [Data readiness](08-data-readiness-and-delivery.md) → [tools and APIs](12-tools-apis-and-subscriptions.md) → [storage and lifecycle](14-data-storage-and-lifecycle.md) |
| Engineer building the first live workflow | [Implementation handoff](10-implementation-handoff.md) → [architecture](03-architecture.md) → [integration contracts](04-integrations.md) → [security](05-security.md) |
| IT team selecting deployment services | [Deployment paths](13-deployment-paths.md) → [platform and hybrid options](15-platform-options-and-hybrid-stacks.md) → [databases](17-postgres-and-supabase-options.md) → [jobs and automation](16-jobs-and-automation-options.md) |
| Security or operations reviewer | [Security](05-security.md) → [storage and lifecycle](14-data-storage-and-lifecycle.md) → [deployment operations](06-deployment.md) → [validation record](11-validation.md) |
| Person sharing or demonstrating the template | [GitHub and demo guide](09-github-and-demo.md) → [implementation handoff](10-implementation-handoff.md) → [validation record](11-validation.md) |

## Complete guide index

| Guide | What it answers | Primary audience |
|---|---|---|
| [00 · Overview](00-overview.md) | What is this template, what works, and how would a company adopt it? | Everyone |
| [01 · Concept and source ideas](01-concept.md) | How do the personal operating-system and maintained-wiki ideas translate to a company? | Sponsors, product owners |
| [02 · Product and teams](02-product-and-teams.md) | What should employees, departments and leadership see and do? | Sponsors, team leads, designers |
| [03 · Architecture](03-architecture.md) | How do evidence, identity, maintained context, retrieval and actions fit together? | Architects, engineers |
| [04 · Integration contracts](04-integrations.md) | Which source tools are candidates, and what must every adapter prove? | Integration engineers, source owners |
| [05 · Permissions and security](05-security.md) | How do tenant boundaries, source access, revocation and action authority work? | Security, IT, engineers |
| [06 · Deployment and operations](06-deployment.md) | What must be installed, monitored, restored and handed over? | Platform teams, operators |
| [07 · Roadmap and economics](07-roadmap-and-economics.md) | What is a bounded first engagement, and how should staffing and cost be estimated? | Sponsors, delivery leads |
| [08 · Data readiness and delivery](08-data-readiness-and-delivery.md) | How do tools, customer calls and messy records become usable, authorized context? | Source owners, delivery teams |
| [09 · GitHub and demonstration](09-github-and-demo.md) | How is the repository shared, and how should the fictional demo be presented? | Maintainers, implementation partners |
| [10 · Engineering handoff](10-implementation-handoff.md) | Exactly what exists in code, and what must be extended or replaced? | Engineering leads, contributors |
| [11 · Validation record](11-validation.md) | What has been checked, and what remains unverified? | Reviewers, maintainers |
| [12 · Tools, APIs and subscriptions](12-tools-apis-and-subscriptions.md) | Which accounts, external tools, developer tools, credentials and bills are needed? | Sponsors, IT, implementers |
| [13 · Deployment paths](13-deployment-paths.md) | How does delivery start from scratch or fit into existing AWS or Azure? | Platform teams, delivery leads |
| [14 · Storage and lifecycle](14-data-storage-and-lifecycle.md) | Where do data and suggestions live, who can read them, and when are they removed? | Data owners, security, engineers |
| [15 · Platform and hybrid options](15-platform-options-and-hybrid-stacks.md) | How can Vercel, Supabase, jobs and automation work with existing clouds? | Architects, platform teams |
| [16 · Jobs and automation](16-jobs-and-automation-options.md) | When should Trigger.dev, n8n or another runtime handle background work? | Automation and platform engineers |
| [17 · PostgreSQL and Supabase](17-postgres-and-supabase-options.md) | Which database services fit, and what do permissions, backups and migration require? | Database and application engineers |

## Templates to use during delivery

- [System inventory](../examples/system-inventory.csv): tools, owners and source responsibilities.
- [Context intake](../examples/context-intake.md): business questions, audiences and workflow expectations.
- [Readiness manifest](../examples/readiness-manifest.json): fictional example for the local declaration checker.
- [API access register](../examples/api-access-register.csv): source/API permissions and account ownership.
- [Data retention register](../examples/data-retention-register.csv): storage classes, access, deletion and recovery decisions.
- [Stack decision register](../examples/stack-decision-register.csv): selected services, processing boundaries and operating responsibilities.

Keep customer-completed copies in the customer's private environment. The public repository should retain reusable templates and fictional examples. Consult the [security boundary](../SECURITY.md), [attribution notice](../NOTICE.md) and [contribution guidance](../CONTRIBUTING.md) when adapting or sharing the project.
