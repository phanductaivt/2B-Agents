# Project Template

Use this folder as the starting point for a new project.

## Purpose

This template helps you create a clean project workspace with:
- project config
- project inputs
- project outputs
- project knowledge
- project tracking files
- project flow visual
- requirement ID registry

Tracking file purposes:
- `status.md`: main progress snapshot for the project and each requirement
- `decision-log.md`: key decisions with date, reason, and impact
- `task-tracker.md`: lightweight task board
- `change-log.md`: project-level version history for generated outputs
- `dependency-map.md`: project-level requirement/FR/feature dependency view
- `project-flow.md`: auto-generated visual flow for this project
- `id-registry.yaml`: stores all IDs for REQ, BRD, FR, US, AC, FEAT, UI, RV, TC

## What To Fill First

1. `project-config.yaml`
2. `status.md`
3. `decision-log.md`
4. `task-tracker.md`
5. `change-log.md`
6. `knowledge/business-rules.md`
7. `knowledge/glossary.md`
8. `projects/<project-name>/inputs/requirements/req-001.md`

## Where Things Go

- requirements: `projects/<project-name>/inputs/requirements/`
- meeting notes: `projects/<project-name>/inputs/meeting-notes/`
- raw text: `projects/<project-name>/inputs/raw/`
- generated output: `projects/<project-name>/outputs/generated/`
- project knowledge: `projects/<project-name>/knowledge/`
- project status: `status.md`
- project decisions: `decision-log.md`
- project tasks: `task-tracker.md`
- project changes: `change-log.md`

## How To Run

After you copy and rename this folder:

```bash
python3 app.py --project <new-project-name> --input req-001.md
```

After run:
- requirement version info: `outputs/generated/<requirement-name>/version-info.md`
- project change history: `change-log.md`
- project dependency view: `dependency-map.md`
- artifact governance files: `artifact-status.md`, `artifact-checklist.md`, `gate-report.md`

<!-- TODO: Add a simple naming rule for project folders and requirement files. -->
