# 2B Agents

BA/PO agent framework with a project-first execution model and a clean 3-layer structure.

## 3-Layer Structure

1. `projects/`
- Project-specific workspaces and data
- Daily input/output surface plus project knowledge and deep ops governance

2. `system/`
- Shared engine and reusable assets
- Agents, artifacts, configs, playbooks, prompts, tools, validators, templates, shared knowledge, tests

3. `workspace/`
- Cross-project operational layer
- Dashboard, visuals, logs, and refactor reports

## Top-Level Layout

```text
2B Agents/
├── projects/
├── system/
├── workspace/
├── app.py
├── README.md
└── architecture.md
```

## Setup

Install dependencies:

```bash
pip install -r requirements.txt
```

## Python Environment (.venv)

This workspace uses a local virtual environment at `.venv/`.

If `.venv` is missing, recreate it:

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
```

Run app with local venv Python:

```bash
.venv/bin/python app.py
```

Colored terminal output now uses `rich` for:
- running steps (`INFO`, cyan/blue)
- success (`SUCCESS`, green)
- warning/skip/blocked (`WARNING`, yellow)
- errors (`ERROR`, red)
- structured run labels such as `[PROJECT]`, `[INPUT]`, and stage/agent `[BA/ba-core]`

## Quick Setup (Non-Technical)

Run these commands in this exact order from the project folder (`2B Agents`):

1. Install dependency:
```bash
pip install -r requirements.txt
```

Successful result should include lines like:
- `Successfully installed rich ...`
or
- `Requirement already satisfied: rich ...`

2. Test dashboard command (quick check):
```bash
python3 app.py --dashboard
```

Successful output should look like:
- `=== 2B Agents Pipeline ===`
- `[SUCCESS] Dashboard updated: .../workspace/dashboard.md`
- `[SUCCESS] HTML dashboard generated: .../workspace/dashboard.html`

3. Test one project run:
```bash
python3 app.py --project ticket-booking-improvement --requirement req-001.md
```

Successful output should include:
- `=== Project: ticket-booking-improvement ===`
- `[INFO] New input detected ...` or `[INFO] Changed input detected ...`
- `[SUCCESS] ...` or `[WARNING] Unchanged input skipped ...`

4. (Optional) Test context sync:
```bash
python3 app.py --sync-context
```

Successful output should include:
- `[SUCCESS] Context sync completed.`
- `[INFO] Report: .../system/context/context-sync-report.md`

## Project-Based Execution (Unchanged)

- Read inputs from `projects/<project-name>/01-input/...`
- Write internal generated outputs to `projects/<project-name>/_ops/generated/...`
- Curate user-facing outputs into `projects/<project-name>/02-output/...`
- Keep tracking and traceability in `projects/<project-name>/_ops/...`
- Orchestrate from root `app.py` using shared logic in `system/`

## Scenario Engine (Config-Based)

Scenario logic is now configuration-driven and loaded from:
- `system/scenarios/scenario-catalog.yaml`
- `system/scenarios/*.yaml`
- Guide: `system/scenarios/README.md`

Resolution order per project:
1. `project-config.yaml` -> `scenario` (if valid)
2. else map `domain` via scenario catalog
3. else fallback to `generic`

This means new projects can use existing scenarios without editing `app.py`.

To add a new scenario:
1. add `system/scenarios/<name>.yaml`
2. register it in `system/scenarios/scenario-catalog.yaml`
3. set `scenario: <name>` in project `project-config.yaml`

## Automatic Incremental Processing

Default command:
```bash
python3 app.py
```

By default, the runner now:
- scans all valid projects
- scans all files in `projects/<project-name>/01-input/requirements/`
- processes only `new` and `changed` files
- skips `unchanged` files

How detection works:
- file hash is calculated from file content (SHA-256)
- if file is not in processing state -> `new`
- if hash changed -> `changed`
- if hash unchanged -> `unchanged`
- if `--force` is used -> reprocess anyway

Processing state is stored in:
- `projects/<project-name>/_ops/runtime/processing-state.yaml`

## Beginner Workflow (No app.py edits needed)

1. Create a project from `projects/project-template/`.
2. Put requirement files in `projects/<project-name>/01-input/requirements/`.
3. Run:
```bash
python3 app.py
```
4. Review outputs in `projects/<project-name>/02-output/`.
5. If a requirement changes, run `python3 app.py` again.
Only changed/new files are regenerated.

## Dashboard & Visuals

- Markdown dashboard: `workspace/dashboard.md`
- HTML dashboard: `workspace/dashboard.html`

Visual references:
- [System Flow](workspace/visuals/system-flow.md)
- [Agent Flow](workspace/visuals/agent-flow.md)
- [Playbook Flow](workspace/visuals/playbook-flow.md)

## Context and Knowledge

- Global context: `system/context/`
- Shared knowledge: `system/knowledge/`
- Project knowledge: `projects/<project-name>/04-knowledge/`

Knowledge priority:
1. project knowledge
2. shared knowledge
3. generic fallback

## Quick Commands

Run all projects:
```bash
python3 app.py
```

Run one project:
```bash
python3 app.py --project ticket-booking-improvement
```

Run one requirement:
```bash
python3 app.py --project ticket-booking-improvement --requirement req-001.md
```

Controlled mode (artifact + gate model):
```bash
python3 app.py --project ticket-booking-improvement --mode controlled
```

Run one stage:
```bash
python3 app.py --project ticket-booking-improvement --requirement req-001.md --stage ba-core
```

Run one artifact:
```bash
python3 app.py --project ticket-booking-improvement --requirement req-001.md --artifact frs
```

Refresh dashboard only:
```bash
python3 app.py --dashboard
```

Run safe context sync (Level 1):
```bash
python3 app.py --sync-context
```

## ID System

Every requirement gets a `# Requirement ID: REQ-001` header and linked artifact IDs:
- `REQ`, `BRD`, `FR`, `US`, `AC`, `FEAT`, `TC`, `UI`, `RV`
- Zero-padded format, for example `REQ-001`, `FR-003`, `TC-010`

## Example Projects

- `projects/ticket-booking-improvement/`
- `projects/loyalty-feature-expansion/`
- `projects/project-template/`

## Start Here

- `README.md`
- `architecture.md`
- `projects/README.md`
- `projects/project-template/README.md`

<!-- TODO: Add a short "new project onboarding" checklist in this README. -->
