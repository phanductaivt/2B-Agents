# Tools

This folder contains simple local-first connectors and utilities.

Current tool areas:
- `files/`: read input files and write Markdown or HTML outputs locally for one selected project
- `project/`: lightweight helpers for status, dashboard, flow, traceability, IDs, test cases, and versioning (`change-log.md`, `version-info.md`)
- `jira/`: placeholder for a future Jira connector
- `confluence/`: placeholder for a future Confluence connector

Dependency mapping helper:
- `tools/project/dependency_manager.py` generates `projects/<project-name>/dependency-map.md`.

Artifact control helper:
- `tools/project/artifact_runner.py` loads artifact catalog, resolves dependencies, and updates `artifact-status.md`.
- `tools/project/artifact_control_manager.py` is legacy and can be kept only for backward reference.

The framework currently depends on local file tools first.

Project-aware rule:
- the selected project controls where input is read and where output is written
- the file tools now work with `projects/<project-name>/...`

External connectors remain placeholders only.
