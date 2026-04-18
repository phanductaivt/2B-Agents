# Operations Console V2 (Phase 3B)

This module is the primary interaction layer in Phase 3B.

## Scope in Phase 3B

- Main operations console surface
- Confirmation decision workspace (read + write)
- Docs workspace (viewer + controlled editor for allowlisted files)
- Stale detection + downstream impact analysis + rerun recommendations
- Controlled rerun actions (project / requirement / from-stage)
- Stable model mapping from current project data
- No unrestricted artifact-level rerun
- No gate override actions

## Role Boundary

- `ops_console` is now the single main console path.
- `decision-review` is deprecated and kept only as a legacy wrapper.

## Source of Truth

- Runtime and governance source: `projects/<project-name>/_ops/...`
- Curated daily view: `projects/<project-name>/02-output/...`
- Confirmation machine source: `_ops/confirmations/pending-confirmations.yaml`

Confirmation data labels:
- `Research Recommendation` = recommendation-only context from research/analysis.
- `Recommended Data` = not final yet, human decision required.
- `Confirmed Data` = final after human confirmation/resolution.

## Main Files

- `server.py`: local HTTP server for the console
- `state_mapper.py`: stable data model mapping layer (consumes shared project semantics)
- `project_api.py`: overview and project-level read endpoints
- `tasks_api.py`: requirement and task read endpoints
- `confirmations_api.py`: confirmation read + write/update endpoints
- `docs_api.py`: document listing, preview, and safe save for allowlisted docs
- `staleness_engine.py`: conservative stale-state and downstream-impact evaluator
- `actions_api.py`: capabilities summary for this phase

Shared semantic source:
- `system/tools/project/semantic_mapper.py`
- `system/tools/project/summary_reader.py`

## Run

```bash
python3 system/tools/ops_console/server.py
```

Then open:

`http://127.0.0.1:8790`

## Docs Edit Boundaries (Phase 3B)

Editable:
- `01-input/requirements/*`
- `01-input/notes/*`
- `04-knowledge/business-rules.md`
- `04-knowledge/notes.md`
- `_ops/decision-log.md`
- `_ops/confirmations/*.md`

View-only:
- `02-output/ba/*.md`
- `02-output/design/*.md`
- `02-output/fe/*.html`

Protected (non-editable):
- `_ops/runtime/*`
- `_ops/generated/**`
- gate result/report files

## Stale State Model (Phase 3B)

Document states:
- `fresh`
- `stale`
- `needs-rerun`
- `manual-override`

Lightweight state file:
- `projects/<project-name>/_ops/runtime/ops-console-staleness.yaml`

This phase computes recommendations and allows controlled rerun actions only through guarded APIs.

## Controlled Rerun Levels (Phase 3B)

Supported:
- `rerun_project`
- `rerun_requirement`
- `rerun_from_stage`

Guards:
- project/requirement/stage validation
- stale/recommendation consistency checks
- stale snapshot freshness guard (re-evaluates editable upstream docs before deny/allow)
- blocked reason returned when action is denied
- runner reuse via `app.py` command execution (no second pipeline path)

Not supported:
- unrestricted artifact-level rerun
- gate override from UI

## Lightweight Consistency Checks

Run a small smoke suite before/after cleanup changes:

```bash
python3 system/tools/ops_console/smoke_checks.py
```

It validates:
- dashboard/ops summary consistency
- protected edit boundaries
- rerun allow/deny basic paths
- stale-state vocabulary normalization
