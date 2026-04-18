# Architecture

This repository uses a clean 3-layer structure and keeps project execution model unchanged.

## Runtime Flow

`projects/<project-name>/01-input` -> `BA` -> `UXUI` -> `FE` -> `validators` -> `projects/<project-name>/_ops/generated` -> `projects/<project-name>/02-output`

Scenario layer:
- project scenario is resolved from `project-config.yaml` + `system/scenarios/scenario-catalog.yaml`
- scenario defaults are loaded from `system/scenarios/*.yaml`
- BA/UXUI/FE package generation uses loaded scenario defaults (not hardcoded project branches)

Incremental runner behavior:
- `app.py` checks `projects/<project-name>/_ops/runtime/processing-state.yaml`
- only new/changed requirement inputs are processed by default
- unchanged inputs are skipped

## Layer Model

1. `projects/` (project-specific workspaces)
- `01-input`, `02-output`, `03-guides`, `04-knowledge`, and `_ops` governance/runtime files

2. `system/` (shared reusable engine)
- agents, artifacts, configs, scenarios, context pack, playbooks, prompts, skills, templates, tools, validators, shared knowledge, tests

3. `workspace/` (cross-project operations)
- dashboard, visuals, logs, and operational reports

## Why Dashboard Is In `workspace/`

Dashboard is cross-project visibility, so it lives outside `projects/`:
- `workspace/dashboard.md`
- `workspace/dashboard.html`

Operations console (main console surface) lives in workspace:
- `workspace/ops-console/index.html`

Decision review UI path is deprecated:
- `workspace/decision-review/index.html` (legacy compatibility redirect)

## Knowledge Model

- Shared knowledge: `system/knowledge/`
- Project knowledge: `projects/<project-name>/04-knowledge/`

Priority:
1. project knowledge
2. shared knowledge
3. fallback defaults

## Root Entrypoint

`app.py` remains at repository root and orchestrates:
- shared logic from `system/tools/`
- config/catalog from `system/configs/` and `system/artifacts/`
- logging to `workspace/logs/`
- project IO inside `projects/<project-name>/...`

## Controlled Governance

Per requirement output folder:
- `artifact-status.md`
- `artifact-checklist.md`
- `gate-results.md`
- `gate-report.md`
- `artifact-reviews/*.md`

Gate and approval rules are configured in:
- `system/configs/gates.yaml`

Per project confirmation workspace:
- `_ops/confirmations/pending-confirmations.yaml` (source of truth)
- `_ops/confirmations/pending-confirmations.md` (readable summary)
- `_ops/confirmations/decisions-log.md` (decision trail)

Source-of-truth split:
- `_ops/...` = runtime/governance truth used by runners, gates, and summaries.
- `02-output/...` = curated reading surface for daily BA/Design/FE usage.

## Visual References

- [System Flow](workspace/visuals/system-flow.md)
- [Agent Flow](workspace/visuals/agent-flow.md)
- [Playbook Flow](workspace/visuals/playbook-flow.md)
