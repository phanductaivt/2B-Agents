---
file_type: "Execution Guide"
primary_agents: ["PO", "BA", "Architect", "Data", "BE", "UIUX", "FE", "QA", "Release"]
supporting_agents: []
activation_mode: "Manual Navigation"
lifecycle_stage: "Project System"
purpose: "Copy-ready cookbook for creating a project, adding input/context, running clarification approval, and generating outputs."
---
# Project Execution Guide

This guide is the main copy/paste cookbook for running a project in this repository.

Use this guide for new project setup and first-time product-slice generation. For a stable project that receives a customer change request or customization request, use `projects/PROJECT_CHANGE_REQUEST_GUIDE.md` instead.

Use it from the repository root:

```bash
cd "/Users/macbookair/2B Agents"
```

Core rule:
- Codex may recommend a decision.
- Only the user can approve downstream execution.
- Do not run downstream agents while `User Approval Status` is `Pending User Approval` or `Blocked`.

## Quick Start

### Terminal command

Replace `my-new-project` and `req-001.md`, then run:

```bash
PROJECT_NAME="my-new-project"; REQ_FILE="req-001.md"; mkdir -p "projects/$PROJECT_NAME"/{01-input/{requirements,notes/meeting-notes,assets/raw},03-context,02-output/{po,ba,architecture,data,be,design,fe,qa,release,app/{backend/{app,tests},frontend/src}}}; touch "projects/$PROJECT_NAME/01-input/requirements/$REQ_FILE"; touch "projects/$PROJECT_NAME/03-context/"{business-rules.md,domain-notes.md,glossary.md,policy.md,market-research.md}
```

### Prompt to copy

Replace project and requirement names:

```text
Run clarification gate only for this project. Do not run downstream agents.

Project:
- projects/<project-name>/

Requirement:
- 01-input/requirements/<requirement-file>.md

Operating mode:
- Follow system/runbooks/generate-product-slice.md
- Follow system/rules/
- Follow system/guardrails/
- Use system/agents/ as role definitions
- Use system/agent-knowledge/ when relevant
- Use system/skills/ and system/templates/
- Read project context from 03-context/

Clarification gate:
- PO/BA must read the requirement and project context.
- Extract problem insight, current pain point, user/stakeholder, and expected business value.
- Create supplemental clarification questions before expanding artifacts.
- Classify each question as blocking, non-blocking, or assumption-backed.
- Recommend a decision, but leave approval to me.
- Write the clarification output to 02-output/ba/.
- Set User Approval Status to Pending User Approval.
- Stop after the clarification gate.

Final response:
- List files created or updated.
- Tell me the exact review file path.
- Tell me the exact sections I should read.
- State Recommended Decision and User Approval Status.
- Tell me the exact approval phrases I can reply with.
```

### Expected result

- Project folders exist under `projects/<project-name>/`.
- Requirement file exists under `01-input/requirements/`.
- Context files exist under `03-context/`.
- After the prompt runs, review `02-output/ba/<req>-clarification.md`.

## Step 1: Create Project Folders

### What to do

Create the standard project structure.

### Option 1 - Prompt to copy

Use this if you want Codex to create the folders:

```text
Create a new project folder structure.

Project name:
- <project-name>

Create these folders:
- 01-input/requirements/
- 01-input/notes/meeting-notes/
- 01-input/assets/raw/
- 03-context/
- 02-output/po/
- 02-output/ba/
- 02-output/architecture/
- 02-output/data/
- 02-output/be/
- 02-output/design/
- 02-output/fe/
- 02-output/qa/
- 02-output/release/
- 02-output/app/backend/app/
- 02-output/app/backend/tests/
- 02-output/app/frontend/src/

Do not generate product outputs yet.
```

### Option 2 - Terminal command

Replace `my-new-project`:

```bash
PROJECT_NAME="my-new-project"; mkdir -p "projects/$PROJECT_NAME"/{01-input/{requirements,notes/meeting-notes,assets/raw},03-context,02-output/{po,ba,architecture,data,be,design,fe,qa,release,app/{backend/{app,tests},frontend/src}}}
```

### Expected result

```text
projects/<project-name>/
├── 01-input/
├── 02-output/
└── 03-context/
```

## Step 2: Add Requirement Input

### What to do

Put the official requirement into `01-input/requirements/`.

Use this file for changes that should become source-of-truth requirement input.

### Option 1 - Prompt to copy

Use this if you want Codex to create a requirement draft from your notes:

```text
Create or update the requirement input file below.

Project:
- projects/<project-name>/

Requirement file:
- 01-input/requirements/<requirement-file>.md

Requirement notes:
<paste your requirement notes here>

Write only the input requirement file. Do not run agents yet.
```

### Option 2 - Terminal command

Replace project, file name, and requirement text:

```bash
PROJECT_NAME="my-new-project"; REQ_FILE="req-001.md"; cat > "projects/$PROJECT_NAME/01-input/requirements/$REQ_FILE" <<'EOF'
# Requirement: <short title>

## Background
<what is happening today>

## Goal
<what outcome you want>

## Users / Stakeholders
<who is affected>

## Scope
<what should be included in v1>

## Out Of Scope
<what should not be included in v1>

## Business Rules
<known rules, constraints, approval rules, policy rules>

## Notes
<extra notes, examples, links, or meeting notes>
EOF
```

### Expected result

- `projects/<project-name>/01-input/requirements/<requirement-file>.md` exists.
- The requirement is clear enough for Codex to run the clarification gate.

## Step 3: Add Project Context

### What to do

Put reusable business knowledge into `03-context/`.

Use context files when the information should apply beyond one requirement.

### Option 1 - Prompt to copy

Use this if you want Codex to create starter context files:

```text
Create starter project context files.

Project:
- projects/<project-name>/

Create or update:
- 03-context/business-rules.md
- 03-context/domain-notes.md
- 03-context/glossary.md
- 03-context/policy.md
- 03-context/market-research.md

Context notes:
<paste known business rules, domain notes, policy constraints, glossary terms, or market notes here>

Do not run agents yet.
```

### Option 2 - Terminal command

Replace `my-new-project`:

```bash
PROJECT_NAME="my-new-project"; mkdir -p "projects/$PROJECT_NAME/03-context"; touch "projects/$PROJECT_NAME/03-context/"{business-rules.md,domain-notes.md,glossary.md,policy.md,market-research.md}
```

Optional starter content:

```bash
PROJECT_NAME="my-new-project"; cat > "projects/$PROJECT_NAME/03-context/business-rules.md" <<'EOF'
# Business Rules

- <rule 1>
- <rule 2>
EOF

cat > "projects/$PROJECT_NAME/03-context/domain-notes.md" <<'EOF'
# Domain Notes

- <domain note 1>
- <domain note 2>
EOF
```

### Expected result

- `03-context/` contains reusable business, domain, glossary, policy, or market notes.
- Empty context files are allowed, but Codex must still run the clarification gate.

## Step 4: Run Clarification Gate

### What to do

Run PO/BA discovery first. This should create the clarification file and stop for your approval.

### Option 1 - Prompt to copy: clarification gate only

Use this when you want to check input quality before any downstream work:

```text
Run clarification gate only. Do not run downstream agents.

Project:
- projects/<project-name>/

Requirement:
- 01-input/requirements/<requirement-file>.md

Operating mode:
- Follow system/runbooks/generate-product-slice.md
- Follow system/rules/
- Follow system/guardrails/
- Use system/agents/ as role definitions
- Use system/agent-knowledge/ when relevant
- Use system/skills/ and system/templates/
- Read project context from 03-context/

Clarification gate:
- PO/BA must read the requirement and project context.
- Extract Insight & Pain Point.
- Extract Known Facts.
- List Assumptions.
- List Blocking Questions.
- List Non-Blocking Questions.
- Set Recommended Decision to Proceed, Proceed with assumptions, or Blocked.
- Set User Approval Status to Pending User Approval.
- Write the result to 02-output/ba/<req>-clarification.md.
- Stop after writing the clarification file.

Final response:
- Tell me the exact clarification file path.
- Tell me the exact sections to review.
- State Recommended Decision.
- State User Approval Status.
- Tell me the exact approval replies I can use.
```

### Option 1 - Prompt to copy: full slice with approval gate

Use this when you want Codex to prepare for the full product slice but still stop before downstream agents:

```text
You are my multi-agent execution team for this repository.

Project:
- projects/<project-name>/

Requirement:
- 01-input/requirements/<requirement-file>.md

Operating mode:
- Follow system/runbooks/generate-product-slice.md
- Follow system/rules/
- Follow system/guardrails/
- Use system/agents/ as role definitions
- Use system/agent-knowledge/ when relevant
- Use system/skills/ and system/templates/
- Read project context from 03-context/

Execution goal:
- Generate the complete product slice from input to runnable local app.
- Write all final outputs directly into this project's 02-output/.

Approval gate:
- First run PO/BA clarification.
- Recommend a decision, but do not self-approve.
- Set User Approval Status to Pending User Approval.
- Stop after the clarification gate.
- Do not run Architect/Data/BE/UIUX/FE/QA/Release until I explicitly approve.

Final response while waiting:
- List files created or updated.
- Tell me the exact review file path.
- Tell me the exact sections to read.
- State Recommended Decision and User Approval Status.
- Tell me the exact approval phrases I can reply with.
```

### Option 2 - Terminal command

No terminal command runs the agents directly. Use terminal only to confirm files exist:

```bash
PROJECT_NAME="my-new-project"; find "projects/$PROJECT_NAME/01-input" "projects/$PROJECT_NAME/03-context" -maxdepth 3 -type f | sort
```

### Expected result

- `projects/<project-name>/02-output/po/<req>-brd.md` may be created or updated.
- `projects/<project-name>/02-output/ba/<req>-clarification.md` is created.
- `User Approval Status` is `Pending User Approval`.
- Downstream agents have not run yet.

## Step 5: Review Clarification Output

### What to do

Open the clarification file and decide whether input is ready.

### Option 1 - Prompt to copy

Use this if you want Codex to summarize what you should review:

```text
Show me what I need to review before approval.

Project:
- projects/<project-name>/

Clarification file:
- 02-output/ba/<req>-clarification.md

Summarize only:
- Insight & Pain Point
- Known Facts
- Assumptions
- Blocking Questions
- Non-Blocking Questions
- Recommended Decision
- User Approval Status
- Downstream Readiness Notes

Do not run downstream agents.
```

### Option 2 - Terminal command

Replace project and file name:

```bash
PROJECT_NAME="my-new-project"; CLARIFICATION_FILE="req-001-clarification.md"; sed -n '1,220p' "projects/$PROJECT_NAME/02-output/ba/$CLARIFICATION_FILE"
```

Or list BA outputs:

```bash
PROJECT_NAME="my-new-project"; find "projects/$PROJECT_NAME/02-output/ba" -maxdepth 1 -type f | sort
```

### Expected result

You should know:
- whether Codex understood the insight and pain point
- which facts are confirmed
- which assumptions Codex wants to use
- which questions block progress
- whether Codex recommends proceeding, proceeding with assumptions, or blocking

## Step 6: Approve, Approve With Assumptions, Or Block

### What to do

Reply to Codex with one of the approval decisions below.

### Option 1 - Prompt to copy: approve as-is

Use this when the clarification is good and no assumption needs correction:

```text
Approved - Proceed. Continue with downstream agents.
```

### Option 1 - Prompt to copy: approve with assumptions

Use this when the clarification has acceptable assumptions:

```text
Approved - Proceed with assumptions. Continue with downstream agents.
```

Use this when you want to adjust assumptions before continuing:

```text
Approved - Proceed with assumptions.

Adjust assumptions first:
- <assumption or decision 1>
- <assumption or decision 2>
- <assumption or decision 3>

Then continue with downstream agents.
```

### Option 1 - Prompt to copy: block

Use this when you need to collect more business information:

```text
Blocked. Do not run downstream agents. I will update the requirement/context first.
```

### Option 1 - Prompt to copy: answer small clarifications in chat

Use this for small updates that do not need to become permanent context yet:

```text
Update the clarification with these decisions, then keep User Approval Status as Pending User Approval so I can review again:
- <decision 1>
- <decision 2>
- <decision 3>
```

Use this if you are ready to approve in the same reply:

```text
Update the clarification with these decisions and Approved - Proceed with assumptions. Then continue with downstream agents:
- <decision 1>
- <decision 2>
- <decision 3>
```

### Option 2 - Terminal command

No terminal command is needed for approval. Approval must be a prompt reply.

### Expected result

- If approved, Codex may continue to downstream agents.
- If blocked, Codex must stop and wait.
- If updated but still pending, Codex updates the clarification and waits for another review.

## Step 7: Update Input Or Rerun Gate

### What to do

If you blocked the run, update official input/context and rerun only the clarification gate.

Use file edits when the information should be saved as source-of-truth.

### Option 1 - Prompt to copy: after editing files

Use this after you update requirement or context files:

```text
I updated the requirement/context. Rerun clarification gate only. Do not run downstream agents.

Project:
- projects/<project-name>/

Requirement:
- 01-input/requirements/<requirement-file>.md

Review the updated input and context, regenerate the clarification output, set User Approval Status to Pending User Approval, and stop.
```

### Option 1 - Prompt to copy: ask Codex to update source files

Use this if you want Codex to update the source files for you:

```text
Update the official input/context with the following information.

Project:
- projects/<project-name>/

Update target:
- <01-input/requirements/<file>.md or 03-context/<file>.md>

Information to add:
- <new fact/rule/decision 1>
- <new fact/rule/decision 2>

After updating, rerun clarification gate only. Do not run downstream agents.
```

### Option 2 - Terminal command

Use this to append notes to a context file:

```bash
PROJECT_NAME="my-new-project"; cat >> "projects/$PROJECT_NAME/03-context/business-rules.md" <<'EOF'

## Added Rules

- <new business rule 1>
- <new business rule 2>
EOF
```

Use this to inspect updated files:

```bash
PROJECT_NAME="my-new-project"; find "projects/$PROJECT_NAME/01-input" "projects/$PROJECT_NAME/03-context" -maxdepth 3 -type f | sort
```

### Expected result

- Source input/context contains the new information.
- Clarification gate can be rerun without generating downstream outputs.

## Step 8: Continue Downstream After Approval

### What to do

After approval, Codex may generate the remaining PO/BA package, architecture, data, backend, frontend, QA, release, and runnable app outputs.

### Option 1 - Prompt to copy

Use this after approving the clarification:

```text
Continue downstream agents after approval.

Project:
- projects/<project-name>/

Requirement:
- 01-input/requirements/<requirement-file>.md

Approval:
- <Approved - Proceed or Approved - Proceed with assumptions>

Continue from the approved clarification gate and generate the remaining product slice:
1. BA package in 02-output/ba/
2. Architecture outputs in 02-output/architecture/
3. Data outputs in 02-output/data/, including metric tracking plan
4. BE spec, API contract, BE implementation plan, and backend app
5. UIUX wireframe
6. FE implementation plan and frontend app
7. QA scenarios, test cases, smoke test plan, and readiness
8. Release run instructions, runnable verification, and release readiness

Run or document backend tests, frontend build, database setup, and local smoke verification.
If something fails, record the exact error and route the fix to the responsible agent.
```

### Option 2 - Terminal command

Use this to watch generated outputs:

```bash
PROJECT_NAME="my-new-project"; find "projects/$PROJECT_NAME/02-output" -maxdepth 3 -type f | sort
```

### Expected result

Final outputs should appear in:
- `02-output/po/`
- `02-output/ba/`
- `02-output/architecture/`
- `02-output/data/` including `<req>-metric-tracking-plan.md`
- `02-output/be/`
- `02-output/design/`
- `02-output/fe/`
- `02-output/qa/`
- `02-output/release/`
- `02-output/app/backend/`
- `02-output/app/frontend/`

## Step 9: Review Final Outputs And Runnable App

### What to do

Check generated artifacts, run instructions, verification results, and local app readiness.

For product measurement review, also read `02-output/data/<req>-metric-tracking-plan.md` and check:
- selected framework and why it fits this feature
- key metrics and how PO should read them
- tracking events/actions, triggers, sources, and required properties
- decision scenarios that explain what PO should do when metrics move together
- gaps, proposed-only sources, or missing baselines/targets

### Option 1 - Prompt to copy

Use this to ask Codex for a final review summary:

```text
Review the generated project outputs and runnable status.

Project:
- projects/<project-name>/

Report:
- files created or updated
- assumptions used
- blockers, if any
- backend test/build status
- frontend build status
- database setup status
- smoke verification status
- whether the project is ready for local runnable review

Do not silently fix unrelated artifacts.
```

### Option 2 - Terminal command

List final outputs:

```bash
PROJECT_NAME="my-new-project"; find "projects/$PROJECT_NAME/02-output" -maxdepth 4 -type f | sort
```

Read release verification:

```bash
PROJECT_NAME="my-new-project"; find "projects/$PROJECT_NAME/02-output/release" -maxdepth 1 -type f -print -exec sed -n '1,180p' {} \;
```

### Expected result

You should know whether the project is ready for local runnable review, which blockers remain, and which run instructions to use.

Local links such as `http://localhost:5173` work only while the backend/frontend servers are running. If you close the terminal, restart your machine, or return in a later session, use Step 10 to start the generated app again.

## Step 10: Restart Local App Later

### What to do

Use this after the app has already been generated and you want to open the local review link again.

This step should start the existing generated app only. It should not regenerate BRD, BA, BE, FE, QA, or release artifacts.

### Option 1 - Prompt to copy

Use this when you want Codex to start the local app and tell you the clickable URL:

```text
Start the generated local app for review.

Project:
- projects/<project-name>/

Requirement:
- 01-input/requirements/<requirement-file>.md

Use the existing generated app only:
- backend: 02-output/app/backend/
- frontend: 02-output/app/frontend/
- release instructions: 02-output/release/

Do not regenerate artifacts.
Do not change source files unless a run command is missing or broken.

Tasks:
- Read the release run instructions.
- Start the backend server.
- Start the frontend server.
- Tell me the local frontend URL I can click.
- Tell me the backend URL.
- If startup fails, show the exact error and the file or command that needs fixing.
```

### Option 2 - Terminal command

Use two terminal windows or tabs.

Terminal 1: start backend.

Replace `my-new-project`:

```bash
PROJECT_NAME="my-new-project"; cd "projects/$PROJECT_NAME/02-output/app/backend"; python3 -m venv .venv 2>/dev/null || true; source .venv/bin/activate; pip install -r requirements.txt; uvicorn app.main:app --reload --port 8000
```

Terminal 2: start frontend.

Replace `my-new-project`:

```bash
PROJECT_NAME="my-new-project"; cd "projects/$PROJECT_NAME/02-output/app/frontend"; npm install; npm run dev
```

If the generated app uses different commands, read the release run instructions:

```bash
PROJECT_NAME="my-new-project"; find "projects/$PROJECT_NAME/02-output/release" -maxdepth 1 -type f -print -exec sed -n '1,220p' {} \;
```

### Expected result

The frontend command should print a local URL, usually:

```text
http://localhost:5173
```

The backend is usually available at:

```text
http://localhost:8000
```

Open the frontend URL in your browser while both servers are still running.

## When To Edit Files Vs Reply In Prompt

Edit `01-input/requirements/<requirement-file>.md` when:
- the official requirement changes
- actor, scope, business flow, or expected value changes
- a business rule becomes source-of-truth

Edit `03-context/business-rules.md` when:
- a rule applies across multiple requirements
- a validation, approval, policy, or operational rule should be reused

Edit `03-context/domain-notes.md` when:
- you add domain knowledge or business process explanation

Edit `03-context/policy.md` when:
- you add compliance, permission, privacy, or policy constraints

Edit `03-context/glossary.md` when:
- you add terms that agents should use consistently

Reply in prompt when:
- you only confirm or adjust a few assumptions
- the decision is temporary for the current requirement
- you want Codex to update clarification first and let you review again

## Review Checklist

Before approving, read:
- `projects/<project-name>/02-output/ba/<req>-clarification.md`

Check these sections:
- `Insight & Pain Point`
- `Known Facts`
- `Assumptions`
- `Blocking Questions`
- `Non-Blocking Questions`
- `Recommended Decision`
- `User Approval Status`
- `Downstream Readiness Notes`

Approve only when:
- the insight and pain point are correct
- facts are not mixed with assumptions
- blocking questions are answered or intentionally blocked
- assumptions are acceptable
- downstream readiness notes make sense

## Approval Replies

Copy one:

```text
Approved - Proceed. Continue with downstream agents.
```

```text
Approved - Proceed with assumptions. Continue with downstream agents.
```

```text
Blocked. Do not run downstream agents. I will update the requirement/context first.
```
