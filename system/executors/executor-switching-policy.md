---
file_type: "Executor Switching Policy"
primary_agents: []
supporting_agents: ["PO", "BA", "Architect", "Data", "BE", "UIUX", "FE", "QA", "Release"]
activation_mode: "On Executor Change"
lifecycle_stage: "System Core"
purpose: "Define safe continuity rules when work moves between AI Executors."
---
# AI Executor Switching Policy

## Core Rule

Changing the AI Executor must not change the active Agent's ownership, active
runbook, approval status, output contracts, or repository permissions.

Use `system/handoff/switch-ai-executor-runbook.md` for an actual switch.

## Before The Current Executor Stops

The outgoing Executor must:

1. Stop at a safe boundary.
2. Avoid beginning a partially executable destructive or high-risk operation.
3. Update `system/handoff/latest-handoff.md` using
   `system/handoff/handoff-template.md`.
4. Record actual file changes, commands, validation, approvals, risks, and
   unresolved uncertainty.
5. Separate its Executor identity from the active Agent role.
6. Record tools and MCPs actually available in the outgoing session.

## Before The Next Executor Continues

The incoming Executor must:

1. Read `system/handoff/README.md`.
2. Read `system/handoff/latest-handoff.md`.
3. Confirm the active project and active task ID.
4. Identify the active workflow, runbook, and Agent separately.
5. Verify its own capability and permission profile.
6. Reconfirm MCP availability instead of inheriting the previous Executor's
   tool claims.
7. Read only the files referenced by the handoff and active runbook.
8. Summarize understanding before editing.

## Capability Mismatch Rule

If the incoming Executor lacks a capability required by the active runbook:

- do not claim continuity is complete
- do not silently replace command or MCP evidence with inference
- record the limitation under `Executor Limitations`
- stop when the missing capability blocks safe execution
- recommend the smallest safe next step or another suitable Executor

## Permission Rule

The incoming Executor uses its current permission profile. It must not inherit,
expand, or assume permissions from the outgoing Executor.

Human approval remains valid only for the recorded scope and action. If the
switch changes the target, operation, or risk, request approval again.

## Handoff Freshness Rule

`system/handoff/latest-handoff.md` describes one current active task. Confirm its
task ID and status before relying on it.

Uncertainty: concurrent active tasks may require task-specific handoff records
in a later phase. Do not overwrite a handoff for another active task without
confirming which task is current.
