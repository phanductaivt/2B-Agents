# Tools

This folder contains simple local-first connectors and utilities.

Current tool areas:
- `files/`: read input files and write Markdown or HTML outputs locally for one selected project
- `project/`: lightweight helpers for status, dashboard, flow, traceability, IDs, test cases, and versioning (`change-log.md`, `version-info.md`)
- `context/`: context loading and safe Level 1 context sync helpers
- `logging/`: shared Rich-based colored terminal logger (`console_logger.py`)
- `jira/`: placeholder for a future Jira connector
- `confluence/`: placeholder for a future Confluence connector

Dependency mapping helper:
- `system/tools/project/dependency_manager.py` generates `projects/<project-name>/_ops/dependency-map.md`.
- `system/tools/project/scenario_manager.py` resolves scenario from project config + scenario catalog.

Artifact control helper:
- `system/tools/project/artifact_runner.py` manages artifact dependency order, gate checks, and artifact status updates.
- `system/tools/project/artifact_review_manager.py` manages artifact-level checklist-based review files and approval state summaries.

The framework currently depends on local file tools first.

Project-aware rule:
- the selected project controls where input is read and where output is written
- the file tools now work with `projects/<project-name>/...`

External connectors remain placeholders only.
