# Security and release boundary

This repository is a local fictional-data demonstration and an enterprise build specification. The demo persona selector and `X-Demo-User` header intentionally allow impersonation. They are not authentication. Never expose this demo to the internet or load company data into it.

Only localhost Host values are accepted, no cross-origin API access is configured, SQLite state is local, and actions are simulated. These are useful demonstration boundaries, not production security claims.

Production requires the gates in [security design](docs/05-security.md) and [deployment](docs/06-deployment.md): verified identity, tenant isolation, source-authoritative access, revocation, secret management, threat testing, deletion and restore procedures, and an operational owner. Nothing here is a SOC 2, ISO 27001, HIPAA, GDPR, or other compliance certification.

If you publish this repository, enable GitHub private vulnerability reporting in repository security settings before inviting external use. Report sensitive issues through that channel; until it exists, contact the repository owner privately rather than putting secrets or customer data into a public issue.
