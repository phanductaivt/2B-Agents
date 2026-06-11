---
file_type: "Handoff Runbook"
primary_agents: []
supporting_agents: ["PO", "BA", "Architect", "Data", "BE", "UIUX", "FE", "QA", "Release"]
activation_mode: "On Pause Or Executor Change"
lifecycle_stage: "System Core"
purpose: "Update the repository-wide latest handoff without changing active work."
reads: ["system/handoff/README.md", "system/handoff/handoff-template.md", "system/handoff/latest-handoff.md", "system/executors/executor-contract.md", "active runbook", "files changed by the active task", "actual validation evidence"]
produces: ["system/handoff/latest-handoff.md"]
---
# Update Handoff Runbook

## Purpose

Record the current task state so another session or AI Executor can continue
without relying on chat memory or bulk-reading the repository.

## Required Context

### Active Executor
- The AI Executor currently performing or pausing the work.

### Active Agent
- The instruction-defined Agent activated by the current runbook.
- `None` when the task is repository governance and no product Agent is active.

### Required Inputs
- `system/handoff/README.md`
- `system/handoff/handoff-template.md`
- existing `system/handoff/latest-handoff.md`
- current active runbook, when any
- exact files created or modified by the active task
- actual command, tool, and validation evidence

### Expected Output
- `system/handoff/latest-handoff.md`

### Stop / Approval Conditions
- Stop if the Active Task ID or current project cannot be identified.
- Stop if replacing the current handoff may overwrite another active task.
- Do not change product outputs, governance files other than
  `system/handoff/latest-handoff.md`, or application code while updating the
  handoff.

## Steps

1. Confirm the Active Task ID and current goal.
2. Record Active Executor and Active Agent separately.
3. Record Active Workflow, Active Phase, Active Runbook, and Active Project
   separately.
4. Record available MCP tools based on current-session evidence only. For
   Filesystem/Workspace MCP, record exact workspace scope, approved operations,
   denied actions, and unrelated dirty-work boundary. Record any local
   Git/GitHub evidence separately as non-MCP activity.
5. Record Executor limitations and current permission profile.
6. List exact files created or modified.
7. Record commands, tool actions, validation, and actual results.
8. Record approvals, risks, uncertainties, and do-not-touch notes.
9. State one recommended next step with exact runbook and context.
10. Keep the handoff concise and point to source files instead of duplicating
    them.

## Validation

- Required handoff sections are present.
- No unverified command or MCP success is claimed.
- Active Executor and Active Agent are not conflated.
- Recommended next step is executable within the recorded permission profile.
