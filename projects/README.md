# Projects Layer

This folder contains project-specific workspaces only.

## What Belongs Here

Each project is self-contained, including:
- `README.md`
- `project-config.yaml` (can define `scenario` and/or `domain`)
- `01-input/` (daily input surface)
- `02-output/` (daily curated output surface)
- `03-guides/` (short working guide for BA/Design/FE)
- `04-knowledge/` (project-specific knowledge)
- `_ops/` (tracking, runtime, traceability, generated internals)
  - `_ops/confirmations/` (pending confirmations + decisions)

## What Does Not Belong Here

- Shared engine components (they are now in `system/`)
- Cross-project dashboard and logs (they are now in `workspace/`)

## Dashboard

Use:
- `workspace/dashboard.md`
- `workspace/dashboard.html`

Dashboard field meaning:
- Project-level summary uses `Project Phase`, `Project Owner`, and `Project Readiness`.
- Execution-level snapshot uses artifact metrics such as execution stage/owner, artifact completion rate, and gate summary.

## Execution

Project execution remains the same:
- read input from `projects/<project-name>/01-input/requirements/...`
- write internal generated output to `projects/<project-name>/_ops/generated/...`
- copy curated user-facing output to `projects/<project-name>/02-output/...`
- review and resolve pending confirmations in `projects/<project-name>/_ops/confirmations/...`

Source-of-truth rule:
- `_ops/generated/` is runtime source-of-truth for execution, gates, traceability, and status.
- `02-output/` is curated daily reading surface for BA/Design/FE users.

Research confirmation rule:
- confirmation items can include `Research Recommendation` and `Recommended Data`.
- only human confirmation changes an item to `Confirmed Data`.

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

```bash
python3 app.py --ops-console
```

```bash
python3 app.py --decision-workspace
```

Visual guides:
- [System Flow](../workspace/visuals/system-flow.md)
- [Agent Flow](../workspace/visuals/agent-flow.md)
- [Playbook Flow](../workspace/visuals/playbook-flow.md)
