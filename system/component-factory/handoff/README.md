# Compatibility Pointer: Repository Handoff

Repository-wide handoff governance now lives in:

- `system/handoff/README.md`
- `system/handoff/latest-handoff.md`
- `system/handoff/handoff-template.md`
- `system/handoff/update-handoff-runbook.md`
- `system/handoff/switch-ai-executor-runbook.md`

Do not update handoff state in `system/component-factory/handoff/`.

This compatibility pointer remains because earlier sessions and references may
still use the old path. Component Factory continues to govern runtime component
creation and maintenance; it does not own repository-wide Executor continuity.
