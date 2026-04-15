# Context Tools

This folder contains simple helpers for context loading and safe context sync.

## Files
- `context_loader.py`: load global/project context files for pipeline runs.
- `prompt_builder.py`: combine context + task input into one prompt package.
- `context_sync.py`: Level 1 safe sync for a small set of core context files.
- `context_diff_report.py`: lightweight text-change summary helper.

## Level 1 Sync Scope
`context_sync.py` updates only these files, and only inside `AUTO-SYNC` markers:
- `system/context/context-summary.md`
- `system/context/artifact-model.md`
- `system/context/workflow-playbook.md`
- `system/context/load-profiles.md`

Level 1 intentionally does **not** auto-rewrite:
- `system/context/traceability-rules.md`
- `system/context/id-system.md`
- `system/context/output-standards.md`
- `system/context/test-case-rules.md`
- `system/context/versioning-rules.md`
- `system/context/dependency-rules.md`
- `system/context/risk-rules.md`
- `system/context/anti-patterns.md`
- `system/context/output-checklists.md`

It also writes:
- `system/context/context-sync-report.md`
- `workspace/logs/context-sync.log`
- `system/context/change-log.md` (append-only entry)

## Run
```bash
python3 system/tools/context/context_sync.py
```

<!-- TODO: Add an example of interpreting the sync report for first-time users. -->
