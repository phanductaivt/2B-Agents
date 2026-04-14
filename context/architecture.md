# Architecture

## Core Folders
- `projects/`: real project workspaces (inputs, outputs, knowledge, tracking).
- `tools/`: lightweight generators and managers (`status`, `dashboard`, `flow`, `traceability`, `id`, `test_case`).
- `playbooks/`: reusable process definitions.
- `agents/`, `skills/`, `validators/`, `prompts/`, `templates/`: reusable system layer.
- `visuals/`: Mermaid flow references.
- `context/`: reusable prompt context pack.

## Project Folder Pattern
- `project-config.yaml`
- `inputs/requirements/`, `inputs/meeting-notes/`, `inputs/raw/`
- `outputs/generated/<requirement-name>/...`
- `knowledge/`
- `status.md`, `decision-log.md`, `task-tracker.md`
- `id-registry.yaml`

## How `app.py` Orchestrates
- Scans projects and requirement inputs.
- Assigns IDs and ensures requirement header ID.
- Runs BA -> UXUI -> FE -> validators.
- Writes outputs and test cases.
- Writes requirement/project traceability files.
- Updates status, project flow, dashboard Markdown/HTML, and logs.
