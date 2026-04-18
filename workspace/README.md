# Workspace Layer

This folder contains cross-project operational artifacts.

## Structure

- `workspace/dashboard.md`
- `workspace/dashboard.html`
- `workspace/ops-console/`
- `workspace/decision-review/`
- `workspace/visuals/`
- `workspace/logs/`

## Purpose

`workspace/` is for visibility and operations across all projects:
- dashboard overview
- operations console (primary interaction layer)
- visual architecture maps
- legacy decision-review compatibility assets
- run logs and sync logs
- optional governance/restructure reports

Open Operations Console V2:
```bash
python3 system/tools/ops_console/server.py
```

or:
```bash
python3 app.py --ops-console
```

Then open:
`http://127.0.0.1:8790`

Role boundary:
- `ops-console/` = main console and source of truth for confirmation actions.
- `ops-console/` docs workspace supports Phase 3B safe editing for allowlisted files only.
- `ops-console/` shows stale state and rerun recommendations.
- `ops-console/` supports controlled rerun actions:
  - project rerun
  - requirement rerun
  - rerun from stage
- `ops-console/` enforces eligibility checks and can return blocked reasons.
- `ops-console/` keeps generated/runtime state files protected from edits.
- `decision-review/` = deprecated wrapper/redirect only.
- `decision-review/` should not receive new logic; it is compatibility-only.

Legacy command:
```bash
python3 app.py --decision-workspace
```

Optional smoke check for console consistency:
```bash
python3 system/tools/ops_console/smoke_checks.py
```

It is not a project data folder.
Project inputs/outputs stay inside `projects/<project-name>/`.
