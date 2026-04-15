# Context Pack

This folder stores reusable context so you do not need to repeat long setup text in every chat or run.

## Start Here
- Open `system/context/index.md` to see all files and what each file is for.
- Open `system/context/load-profiles.md` to choose a small context set by task type.

## Fast Usage
- Quick load: `system/context/context-summary.md`
- Deep load: `system/context/full-context.md`
- Task-focused load: pick one profile from `system/context/load-profiles.md`

## Maintenance
- Track updates in `system/context/change-log.md`
- Avoid common mistakes in `system/context/anti-patterns.md`

## Safe Auto Sync (Level 1)
- Run `python3 system/tools/context/context_sync.py` (or `python3 app.py --sync-context`)
- This updates only a small set of core files:
  - `context-summary.md`
  - `artifact-model.md`
  - `workflow-playbook.md`
  - `load-profiles.md`
- Only content inside `AUTO-SYNC` markers is changed.
- Review results in `system/context/context-sync-report.md`.
- Level 1 does not auto-rewrite deep rule files (ID, traceability, test-case, versioning, dependency, risk, anti-patterns, checklists).

<!-- TODO: Add a monthly context review checklist (owner + date). -->
