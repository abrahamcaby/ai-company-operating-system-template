# Publish the repository and demonstrate the product

Choose the account or organization that should own your copy of this template, then use one of the publication routes below. The suggested repository name is `ai-company-operating-system-template`. Publishing the repository shares source code and documentation; it does not deploy a production company OS.

For a customer deciding what to obtain or install, share [setup requirements](12-tools-apis-and-subscriptions.md), [AWS/Azure/fresh-start delivery paths](13-deployment-paths.md), and [data and suggestion storage](14-data-storage-and-lifecycle.md) alongside the demo.

For teams evaluating Vercel, Supabase/PostgreSQL, Trigger.dev or n8n, also share [platform options and hybrid stacks](15-platform-options-and-hybrid-stacks.md). It contains concrete combinations and links to the database and automation guides; the provider integrations remain planned implementation work.

## Prepare the software package

Work from the `ai-company-operating-system-template` folder, not the surrounding ChatGPT project directory or its synced `sources` directory. Include the application, fictional Meridian Works fixtures, tests, documentation, templates, license, attribution notice, and GitHub workflow files.

Customer-specific material belongs in a separate company-controlled environment. Keep credentials, source exports, recordings, transcripts, employee records, financial data, customer-filled manifests, and local databases out of this repository. Its ignore rules are a convenience, not an information-classification system: review the files you actually stage and publish.

Run the existing checks from the project root:

```sh
python3 -m unittest discover -s tests -v
python3 -m app.readiness examples/readiness-manifest.json
```

The second command checks fictional declarations, not real permissions or consent. For the prototype, publish claims supported by the runnable demo and tests. Keep production identity, live connectors, recording, LLM answers, cloud operations, and guest access labeled as planned work.

## Publish with GitHub Desktop

If the folder is not yet a Git repository, initialize it once from a terminal opened in `ai-company-operating-system-template`:

```sh
git init -b main
```

Then:

1. Sign in to GitHub Desktop. Choose **File → Add Local Repository**, select `ai-company-operating-system-template`, and add it. [GitHub's local-repository instructions](https://docs.github.com/en/desktop/adding-and-cloning-repositories/adding-a-repository-from-your-local-computer-to-github-desktop)
2. Review the Changes list and select only the intended software files. Enter an initial commit summary, then commit to `main`.
3. Choose **Publish repository**. Set the name to `ai-company-operating-system-template`, choose its owner, and add a description such as “Company AI OS: permission-aware demo and enterprise implementation blueprint.”
4. For a public software repository, clear **Keep this code private** after checking the intended files. Choose **Publish Repository**. [GitHub's publishing instructions](https://docs.github.com/en/desktop/adding-and-cloning-repositories/adding-an-existing-project-to-github-using-github-desktop)
5. Open the published repository, review the README and documentation links, and check the Actions result. Subsequent commits are uploaded with **Push origin**.

## Publish with Git commands

Create an empty repository named `ai-company-operating-system-template` on GitHub under your chosen owner. Do not initialize it there with a README, license, or ignore file. Authenticate Git using your preferred supported method. These commands assume a new local repository; replace `YOUR-OWNER` with the actual account or organization. [GitHub's command-line import instructions](https://docs.github.com/en/migrations/importing-source-code/using-the-command-line-to-import-source-code/adding-locally-hosted-code-to-github)

Run from the `ai-company-operating-system-template` folder:

```sh
git init -b main
git status --short
git add .
git diff --cached --stat
git diff --cached --name-only
```

Review the staged files before continuing. Then:

```sh
git commit -m "Add company AI OS demo and implementation blueprint"
git remote add origin https://github.com/YOUR-OWNER/ai-company-operating-system-template.git
git remote -v
git push -u origin main
```

If a Git repository or `origin` already exists, inspect it and adapt the commands to the intended destination; do not blindly replace its remote or overwrite existing history. The public repo should expose only the reviewed software package.

## Run a local demo for a company

With Python 3.11 or newer, start the app from the project root:

```sh
python3 -m app.server
```

Open [the local demo](http://localhost:8080). Stop it with Ctrl+C. The default server binds to your own computer. The supplied Docker Compose configuration is another local option:

```sh
docker compose up --build
```

That configuration also publishes only to localhost. The demo has an intentionally open persona selector; do not expose it as a public hosted company service. Publishing this code on GitHub does not change that limitation. For a public presentation, use the fictional local demo in a screen share or publish screenshots of fictional data. A hosted interactive demo requires a separately reviewed deployment and access design.

## A five-minute guided walkthrough

1. **Start as Alex Morgan, CEO.** Open Knowledge and search for `Atlas`. Inspect the CRM record and leadership review; then search `cash` and inspect the fictional approved snapshot. Explain that these are seeded records, not live data or automatically reconciled figures.
2. **Switch to Jordan Lee, Sales.** Search `Atlas` again. Open the customer call evidence to show time references and the buyer's requests. The compiled Atlas account brief is absent because Sales lacks the handoff source required by that combined page.
3. **Switch to Riley James, Customer Success.** Search `Atlas`. This persona has both Sales and Customer Success source scope, so the compiled account brief and its supporting handoff become readable. The example illustrates intersection of source permissions.
4. **Show an action.** Switch to Jordan, open Workflows, select **Atlas customer call · Evidence**, and propose “Confirm the Atlas implementation owner.” Create the proposal. Jordan cannot approve their own request. Switch to Alex, open Workflows, review its evidence, choose **Approve proposal**, then **Simulate execution**. The resulting state is simulated; no outside project tool is changed.
5. **Explain the boundary.** Switch to Casey Brooks, People, to show the synthetic restricted case. Return to Alex and confirm that it is absent. Switch to Taylor Chen, IT: the administrator can inspect connection planning and their runbook but does not gain access to the People case or Atlas call. The Connections page shows planned adapters.
6. **Close on implementation.** Open [data readiness and delivery](08-data-readiness-and-delivery.md), then [deployment](06-deployment.md). Use the customer's actual systems to discuss a scoped pilot, required owners, recording route, accepted data, permissions, and installation responsibilities.

Operations, Finance, Marketing, and employee views are also available. There is no guest persona or interactive revoke control in the current UI. The local tests exercise sample policy behavior; a production pilot must additionally prove the real provider's access-change behavior.

In Overview, **Find evidence** performs a deterministic keyword query over the current persona's permitted fictional records. It is useful for demonstrating evidence visibility, but should not be introduced as a generative assistant. The readiness checker is similarly a local declaration check, not an uploader or recording system.

## What to share with a prospective customer

Share the GitHub link once published, a short demo using fictional data, and a scoped description of the outcome they would pilot. Direct a business sponsor to the concept and team views; direct IT to architecture, integrations, security, and deployment; direct the implementation owner to data readiness and delivery.

Use a precise description: “This is a working permission-aware demonstration and a detailed blueprint for building your company-owned AI knowledge and workflow service.” The first customer engagement should establish source readiness and implement a bounded live workflow before expanding toward the company-wide vision.
