---
file_type: "Handoff Runbook"
primary_agents: []
supporting_agents: ["PO", "BA", "Architect", "Data", "BE", "UIUX", "FE", "QA", "Release"]
activation_mode: "On Executor Change"
lifecycle_stage: "System Core"
purpose: "Switch AI Executors while preserving Agent ownership, task state, permissions, and validation evidence."
reads: ["system/handoff/README.md", "system/handoff/latest-handoff.md", "system/executors/executor-contract.md", "system/executors/executor-switching-policy.md", "system/executors/executor-capability-template.md", "selected workflow contract when registered", "active runbook", "files referenced by latest handoff"]
produces: ["confirmed continuation state", "system/handoff/latest-handoff.md when capability or task state changes"]
---
# Switch AI Executor Runbook

## Purpose

Safely continue one active task with a different AI Executor.

## Required Context

### Incoming Active Executor
- The new AI system or client continuing the task.

### Active Agent
- The instruction-defined Agent recorded in the handoff.
- Do not change the Active Agent merely because the Executor changed.

### Required Inputs
- `system/handoff/README.md`
- `system/handoff/latest-handoff.md`
- `system/executors/executor-contract.md`
- `system/executors/executor-switching-policy.md`
- `system/executors/executor-capability-template.md`
- selected workflow contract when the handoff records a registered workflow
- active runbook and exact files referenced by the handoff

### Expected Outputs
- confirmed continuation summary
- updated `system/handoff/latest-handoff.md` only when capability, permission, or
  task state changes

### Stop / Approval Conditions
- Stop if the Active Task ID is missing or does not match the intended task.
- Stop if the handoff is stale, conflicting, or belongs to another project.
- Stop if a required capability, MCP, permission, input, or approval is missing.
- Do not broaden permissions or reroute Agent ownership during the switch.

## Steps

1. Read the latest handoff and identify the Active Task ID.
2. Summarize the current goal, project, workflow, phase, runbook, Agent, files
   changed, validation status, risks, and recommended next step.
3. Declare the incoming Executor's capability and permission profile.
4. Verify required MCP tools and other capabilities in the current session.
5. Compare incoming capabilities with those required by the active runbook.
6. Read only the selected workflow contract, active phase runbook, and exact
   files referenced by the handoff.
7. Confirm whether work can continue safely.
8. If continuing, preserve Agent ownership, approvals, and output contracts.
9. If blocked, update the handoff with the capability mismatch and next safe
   action.

## Validation

- Active Executor and Active Agent are separately identified.
- No previous Executor capability was silently inherited.
- No unrelated repository context was loaded.
- Continuation or blocking decision is supported by evidence.
