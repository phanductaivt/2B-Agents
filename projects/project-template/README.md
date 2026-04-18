# Project Template

Use this folder as the starting point for a new project.

## Purpose

This template helps you create a clean project workspace with:
- project config
- daily input/output surface
- short user guides
- project knowledge
- deep ops/tracking/runtime files

## Folder Layout

- `01-input/`
- `02-output/`
- `03-guides/`
- `04-knowledge/`
- `_ops/`

Inside `_ops/`:
- `status.md`: main progress snapshot
- `decision-log.md`: key decisions
- `task-tracker.md`: lightweight task board
- `change-log.md`: project-level version history
- `dependency-map.md`: dependency view
- `project-flow.md`: auto-generated visual flow
- `confirmations/pending-confirmations.yaml`: confirmation source of truth
- `confirmations/pending-confirmations.md`: readable confirmation summary
- `confirmations/decisions-log.md`: confirmation decision history
- confirmation data labels:
  - `Research Recommendation` and `Recommended Data` (not final)
  - `Confirmed Data` only after human confirmation
- `traceability/requirement-traceability-summary.md`
- `runtime/id-registry.yaml`: artifact IDs
- `runtime/processing-state.yaml`: incremental hash state

## What To Fill First

1. `project-config.yaml`
2. `03-guides/README.md`
3. `04-knowledge/business-rules.md`
4. `04-knowledge/glossary.md`
5. `01-input/requirements/req-001.md`

Scenario setup in `project-config.yaml`:
- `scenario`: optional explicit scenario key (example: `ticketing`, `loyalty`, `order-status`, `generic`)
- `domain`: used for automatic mapping when `scenario` is not set

Fallback rule:
1. use `scenario` if defined and valid
2. else map by `domain`
3. else fallback to `generic`

Add a custom scenario later:
- create a new YAML file under `system/scenarios/`
- register it in `system/scenarios/scenario-catalog.yaml`
- set `scenario: <your-scenario-key>` in project config

## Where Things Go

- requirements: `projects/<project-name>/01-input/requirements/`
- meeting notes: `projects/<project-name>/01-input/notes/meeting-notes/`
- raw text: `projects/<project-name>/01-input/assets/raw/`
- curated BA output: `projects/<project-name>/02-output/ba/`
- curated design output: `projects/<project-name>/02-output/design/`
- curated FE output: `projects/<project-name>/02-output/fe/`
- project knowledge: `projects/<project-name>/04-knowledge/`
- deep generated runtime output: `projects/<project-name>/_ops/generated/`
- project tracking and governance: `projects/<project-name>/_ops/`

Operations console:
```bash
python3 app.py --ops-console
```

Then open:
`http://127.0.0.1:8790`

## How To Run

After you copy and rename this folder:

```bash
python3 app.py --project <new-project-name> --requirement req-001.md
```

After run:
- requirement version info: `_ops/generated/<requirement-name>/version-info.md`
- project change history: `_ops/change-log.md`
- project dependency view: `_ops/dependency-map.md`
- artifact governance files: `artifact-status.md`, `artifact-checklist.md`, `gate-report.md`

<!-- TODO: Add a simple naming rule for project folders and requirement files. -->
