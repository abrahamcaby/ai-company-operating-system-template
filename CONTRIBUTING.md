# Contributing

Keep the default demo dependency-free and fictional. Run `python3 -m unittest discover -s tests -v` before proposing changes. For every new data surface, test unauthorized reads, cross-tenant reads, revoked membership, missing ACLs, and derived evidence restrictions.

A connector is not complete until its permission semantics, deleted records, retries, pagination, schema drift, rate limits and account disconnection are tested in an authorized provider sandbox. Never replace source permissions with a broad department label to make an integration appear to work.

Keep public source code and customer deployment state separate. No credentials, recordings, transcripts, customer exports or raw model traces in commits. Use synthetic fixtures. Update the implemented/planned table in README for every shipped capability.

Do not claim production readiness or compliance from passing the local demo tests. Document actual provider and production evidence separately.
