# 2B Agents

BA-focused agent framework with a project-first execution model and a clean 3-layer structure.

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

Source-of-truth rule:
- Runtime execution truth lives in `_ops/...` files.
- `02-output/...` is a curated consumption layer, not execution state.

## Confirmations In Operations Console

Each project now includes confirmation files:
- `projects/<project-name>/_ops/confirmations/pending-confirmations.yaml` (source of truth)
- `projects/<project-name>/_ops/confirmations/pending-confirmations.md` (readable summary)
- `projects/<project-name>/_ops/confirmations/decisions-log.md` (history)

Open the main operations console:
```bash
python3 app.py --ops-console
```

Then open:
`http://127.0.0.1:8790`

What confirmation actions can do in ops_console:
- filter/search confirmation items
- filter by project, status, type, and owner
- confirm/reject/needs-more-info/resolve
- write decision notes and approver
- set confirmed-at
- save back to YAML + Markdown logs safely

Research decision boundary:
- Researcher recommendations are tracked as `Research Recommendation` + `Recommended Data`.
- Final truth requires your confirmation (`decision_authority: human-required`).
- After you confirm/resolve an item, data state becomes `Confirmed Data`.

Docs + Actions workspace in Phase 3B:
- preview docs by project with metadata
- safe edit/save only for allowlisted document classes:
  - `01-input/requirements/*`
  - `01-input/notes/*`
  - `04-knowledge/business-rules.md`
  - `04-knowledge/notes.md`
  - `_ops/decision-log.md`
  - `_ops/confirmations/*.md`
- view-only for `02-output/*`
- protected: `_ops/runtime/*`, `_ops/generated/**`, gate result/report files
- stale detection states: `fresh`, `stale`, `needs-rerun`, `manual-override`
- controlled rerun levels are available:
  - `Rerun Project`
  - `Rerun Requirement`
  - `Rerun From Stage`
- rerun actions are guarded by eligibility checks and stale/recommendation context
- artifact-level rerun is not enabled in this phase

Scope note:
- `workspace/ops-console/` is now the main interaction surface.
- `workspace/decision-review/` is deprecated and kept only for compatibility.

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
- Operations Console V2 shell: `workspace/ops-console/index.html`

Dashboard semantics:
- Project Summary fields: `Project Phase`, `Project Owner`, `Project Status`, `Project Readiness`, `Last Update`
- Execution Snapshot fields: `Current Execution Stage`, `Current Execution Owner`, `Artifact Completion Rate`, `Gate Summary`, `Blocked Reason`
- `Project Readiness` is project-level milestone progress from requirement statuses (not artifact completion rate).
- `Artifact Completion Rate` is execution progress from artifact status files.
- Shared semantic mapping source: `system/tools/project/semantic_mapper.py`
- Shared summary parsing source: `system/tools/project/summary_reader.py`

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

Legacy decision workspace wrapper (deprecated):
```bash
python3 app.py --decision-workspace
```
Use this only for compatibility. Primary path is `--ops-console`.

Open Operations Console V2 (primary console):
```bash
python3 app.py --ops-console
```

Or direct:
```bash
python3 system/tools/ops_console/server.py
```

Then open:
`http://127.0.0.1:8790`

Optional lightweight console consistency check:
```bash
python3 system/tools/ops_console/smoke_checks.py
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
