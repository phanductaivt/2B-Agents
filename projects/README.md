# Projects Layer

This folder contains project-specific workspaces only.

## What Belongs Here

Each project is self-contained, including:
- `README.md`
- `project-config.yaml` (can define `scenario` and/or `domain`)
- `01-input/` (daily input surface)
- `02-output/` (daily curated output surface)
- `03-guides/` (short working guide for BA/PO/Design/FE)
- `04-knowledge/` (project-specific knowledge)
- `_ops/` (tracking, runtime, traceability, generated internals)

## What Does Not Belong Here

- Shared engine components (they are now in `system/`)
- Cross-project dashboard and logs (they are now in `workspace/`)

## Dashboard

Use:
- `workspace/dashboard.md`
- `workspace/dashboard.html`

## Execution

Project execution remains the same:
- read input from `projects/<project-name>/01-input/requirements/...`
- write internal generated output to `projects/<project-name>/_ops/generated/...`
- copy curated user-facing output to `projects/<project-name>/02-output/...`

Run examples:

```bash
python3 app.py --project ticket-booking-improvement
```

```bash
python3 app.py --project ticket-booking-improvement --requirement req-001.md --stage ba-core
```

```bash
python3 app.py --dashboard
```

Visual guides:
- [System Flow](../workspace/visuals/system-flow.md)
- [Agent Flow](../workspace/visuals/agent-flow.md)
- [Playbook Flow](../workspace/visuals/playbook-flow.md)
