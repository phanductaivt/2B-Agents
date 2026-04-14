# Project-Based BA-Led Agent Framework

This workspace is a reusable AI agent framework for BA-led product work.

It helps a Business Analyst or Product Owner user work with:
- requirement clarification
- BPMN-style process drafting in Mermaid
- user story generation
- acceptance criteria writing
- BRD drafting
- agile-style FRS drafting
- feature hierarchy and feature list generation
- wireframe drafting
- frontend HTML demo generation
- review and validation
- playbook orchestration
- project knowledge reuse

## Two Simple Layers

This workspace now has two clear layers:

1. System-level folders
- reusable parts such as `agents/`, `skills/`, `playbooks/`, `validators/`, `prompts/`, `tools/`, `templates/`, and shared `knowledge/`

2. Project-level folders
- real working data under `projects/<project-name>/`
- each project keeps its own inputs, outputs, knowledge, config, and README

## Why This Helps

- each project keeps its own files in one place
- input and output are easier to control in VS Code
- project knowledge stays close to the real work
- the reusable system stays simple

## Main Project Folder

Each project now follows this pattern:

```text
projects/<project-name>/
  README.md
  project-config.yaml
  status.md
  decision-log.md
  task-tracker.md
  projects/<project-name>/inputs/
    requirements/
    meeting-notes/
    raw/
  projects/<project-name>/outputs/
    generated/
  knowledge/
    glossary.md
    business-rules.md
    notes.md
```

## Main Folders

System-level folders:
- `agents/`: role-based agent definitions
- `skills/`: reusable BA-led analysis and product-structuring skills
- `artifacts/`: artifact model catalog for artifact-by-artifact execution
- `knowledge/`: shared fallback knowledge for all projects
- `playbooks/`: reusable end-to-end processes
- `tools/`: simple local-first file utilities and future placeholders
- `validators/`: quality checks
- `prompts/`: prompt guidance for agents and skills
- `configs/`: system-wide model, routing, permissions, and template settings
- `templates/`: business document templates
- `tests/`: simple manual testing notes
- `logs/`: space for future run notes

Project-level folder:
- `projects/`: real project workspaces with separate inputs, outputs, knowledge, config, and project management files

Root-level input/output folders no longer exist.
All real work happens only inside `projects/<project-name>/`.

## Project Tracking Files

Each project includes three simple tracking files:
- `status.md`: the main progress snapshot for the project and each requirement
- `decision-log.md`: key decisions with date, reason, and impact
- `task-tracker.md`: a lightweight Markdown task board
- `change-log.md`: project-level revision history for output changes

## Project Dashboard

The workspace also includes:
- `projects/dashboard.md` for a Markdown overview
- `projects/dashboard.html` for a simple web view

Use Markdown inside VS Code, and HTML if you want a browser view.

The HTML dashboard includes:
- summary metric cards
- filters and search
- project table with progress bars
- project cards and blocked list

## Visual System Maps

Open these in VS Code to understand the flow visually:
- [system-flow.md](/Users/macbookair/2B%20Agents/visuals/system-flow.md)
- [agent-flow.md](/Users/macbookair/2B%20Agents/visuals/agent-flow.md)
- [playbook-flow.md](/Users/macbookair/2B%20Agents/visuals/playbook-flow.md)

## Project Flow Visuals

Each project has an auto-generated `project-flow.md` that shows:
- inputs and outputs
- agent flow
- traceability to outputs
- status and dashboard updates

Each processed requirement also generates:
- `outputs/generated/<requirement-name>/requirement-flow.md`
This shows the requirement-to-output flow with Mermaid diagrams.

## Context Pack (Token Saving)

Use the `context/` folder to avoid repeating long project history in prompts.

- Fast load: `context/context-summary.md`
- Deep load: `context/full-context.md`
- Focused load: one file such as `context/id-system.md`
- Loader utility: `tools/context/context_loader.py`

Prompt example:
- `Read context/context-summary.md and process requirement req-001 in project ticket-booking-improvement.`

Best practice:
- Use summary for routine generation.
- Use full context only for broad redesign/debug tasks.
- Use specific context files for focused requests (IDs, traceability, tests, risks).

## Auto Context Injection

Context is auto-loaded during `app.py` runs. You do not need to write manual context-loading prompts.

Auto-loaded global context:
- `context/context-summary.md`
- `context/workflow-playbook.md`
- `context/output-standards.md`
- `context/id-system.md`
- `context/traceability-rules.md`

Auto-loaded project context:
- `projects/<project-name>/knowledge/glossary.md`
- `projects/<project-name>/knowledge/business-rules.md`
- `projects/<project-name>/knowledge/notes.md`

Optional context load audit:
- `logs/context-load.log`

Traceability outputs:
- `outputs/generated/<requirement-name>/requirement-traceability-matrix.md`
- `outputs/generated/<requirement-name>/requirement-traceability-flow.md`
- `requirement-traceability-summary.md` at the project root

Test case outputs:
- `outputs/generated/<requirement-name>/test-cases.md` (generated from FRS, user story, and acceptance criteria)
- TC IDs link to AC/US/FR IDs inside the test case matrix

Artifact control outputs (for controlled mode):
- `outputs/generated/<requirement-name>/artifact-status.md`
- `outputs/generated/<requirement-name>/artifact-checklist.md`
- `outputs/generated/<requirement-name>/gate-report.md`
- `outputs/generated/<requirement-name>/risk-notes.md`

Dependency mapping output:
- `projects/<project-name>/dependency-map.md` (project-level dependency table + Mermaid graph + downstream risk notes)

Versioning outputs:
- `projects/<project-name>/change-log.md` stores project-level revisions
- `projects/<project-name>/outputs/generated/<requirement-name>/version-info.md` stores requirement-level version details
- first generation starts at `v1.0`
- meaningful regeneration increments to `v1.1`, `v1.2`, and so on
- larger structural updates can move to a new major version (for example `v2.0`)

Requirement ID system:
- `id-registry.yaml` inside each project stores IDs for REQ, BRD, FR, US, AC, FEAT, UI, RV, TC
- each requirement input file gets a `# Requirement ID: REQ-001` header

ID rules (zero-padded):
- REQ-001, BRD-001, FR-001, US-001, AC-001, FEAT-001, UI-001, RV-001, TC-001

## Example Projects

This workspace includes:
- `projects/ticket-booking-improvement/`
- `projects/loyalty-feature-expansion/`
- `projects/project-template/`

## Quick Start

Run all projects automatically:

```bash
python3 app.py
```

Run one project only:

```bash
python3 app.py --project ticket-booking-improvement
```

Run one requirement only:

```bash
python3 app.py --project ticket-booking-improvement --requirement req-001.md
```

Re-run all requirements in one project:

```bash
python3 app.py --project ticket-booking-improvement --force
```

Run controlled mode (next runnable artifact only):

```bash
python3 app.py --project ticket-booking-improvement --mode controlled
```

Run one specific artifact in controlled mode:

```bash
python3 app.py --project ticket-booking-improvement --requirement req-001.md --artifact frs
```

Run one stage in controlled mode:

```bash
python3 app.py --project ticket-booking-improvement --requirement req-001.md --stage ba-core
```

Refresh the dashboard:

```bash
python3 app.py --dashboard
```

## What The Demo Does

The automated flow in `app.py`:
- scans all projects under `projects/`
- reads all requirement files from `projects/<project-name>/inputs/requirements/`
- loads that project's `project-config.yaml`
- loads that project's knowledge first
- uses shared knowledge only as fallback
- runs the BA Agent outputs including feature list creation
- runs the UXUI Agent wireframe step
- runs the FE Agent HTML step
- runs validators
- supports controlled artifact-by-artifact execution with gate checks
- updates artifact status/checklist/gate report in controlled governance mode
- updates version tracking (`version-info.md` + `change-log.md`) on generation/regeneration
- refreshes project dependency mapping in `dependency-map.md`
- updates `status.md` for the processed requirement
- writes output into `projects/<project-name>/outputs/generated/<input-name>/`

Artifact model source:
- `artifacts/artifact-catalog.yaml` defines artifact name, stage, owner, dependencies, outputs, validators, and gate requirement.

The dashboard flow:
- reads each project's `status.md`
- regenerates `projects/dashboard.md`
- generates `projects/dashboard.html`

## Prompt vs Playbook vs Project

- Prompt: instruction for one task
- Playbook: reusable end-to-end process
- Project: container for one real piece of work with its own inputs, outputs, config, and knowledge

## Practical Example

Example input:
- `projects/ticket-booking-improvement/inputs/requirements/req-001.md`

Example output folder:
- `projects/ticket-booking-improvement/outputs/generated/req-001/`

Example generated files:
- `clarification.md`
- `process-bpmn.md`
- `user-story.md`
- `acceptance-criteria.md`
- `brd.md`
- `frs.md`
- `feature-list.md`
- `wireframe.md`
- `review-notes.md`
- `ui.html`

## Start Here

Open these files first:
- `projects/README.md`
- `README.md`
- `architecture.md`
- `projects/project-template/README.md`

<!-- TODO: Add a small starter checklist for creating a new project from the template. -->
