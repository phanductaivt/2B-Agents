# Architecture

## Core Folders
- `projects/`: real project workspaces (inputs, outputs, knowledge, tracking).
- `system/tools/`: lightweight generators and managers (`status`, `dashboard`, `flow`, `traceability`, `id`, `test_case`).
- `system/playbooks/`: reusable process definitions.
- `system/agents/`, `system/skills/`, `system/validators/`, `system/prompts/`, `system/templates/`: reusable system layer.
- `workspace/visuals/`: Mermaid flow references.
- `system/context/`: reusable prompt context pack.

## Project Folder Pattern
- `project-config.yaml`
- `01-input/requirements/`, `01-input/notes/meeting-notes/`, `01-input/assets/raw/`
- `02-output/ba/`, `02-output/design/`, `02-output/fe/`
- `04-knowledge/`
- `_ops/status.md`, `_ops/decision-log.md`, `_ops/task-tracker.md`
- `_ops/runtime/id-registry.yaml`

## How `app.py` Orchestrates
- Scans projects and requirement inputs.
- Assigns IDs and ensures requirement header ID.
- Runs BA -> UXUI -> FE -> validators.
- Writes outputs and test cases.
- Writes requirement/project traceability files.
- Updates status, project flow, dashboard Markdown/HTML, and logs.
