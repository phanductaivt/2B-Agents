---
file_type: "Workflow Contract Template"
primary_agents: []
supporting_agents: ["PO", "BA", "Architect", "Data", "BE", "UIUX", "FE", "QA", "Release"]
activation_mode: "On Workflow Creation Or Review"
lifecycle_stage: "System Core"
purpose: "Define the minimum contract required for an executor-neutral multi-phase workflow."
---
# Workflow Contract: <Workflow Name>

## Workflow ID

- `<stable-workflow-id>`

## Purpose

- Why this workflow exists.
- What it governs and what remains outside its scope.

## Trigger

- Event or user request that activates this workflow.
- Conditions that mean another workflow should be used instead.

## Required Inputs

- Exact starting inputs.
- Shared governance references:
  - `system/executors/executor-contract.md`
  - `system/workflows/workflow-lifecycle.md`
  - `system/registries/workflows-index.md`
  - applicable routing and output registries

## Active Phases

| Phase | Active Agent | Required Runbook | Entry Condition | Required Skills / Rules / Guardrails | Required Outputs | Exit Condition |
| --- | --- | --- | --- | --- | --- | --- |
| `<phase>` | `<Agent or None>` | `<exact path>` | `<condition>` | `<exact paths or active-runbook routing>` | `<exact paths or registry contract>` | `<condition>` |

Use `None` when the phase is orchestration or governance work and no
instruction-defined Agent owns it. Do not invent an Agent to fill the field.

## Approval Gates

- Gate:
  - required approver:
  - evidence:
  - allowed decisions:
  - blocked actions before approval:

## Stop Conditions

- Missing input, approval, capability, ownership, or verification conditions
  that require the AI Executor to stop instead of guessing.

## Recovery Rules

- Runbook or rollback route for clarification, failed validation, changed
  scope, or interrupted execution.

## Handoff Requirements

- Update `system/handoff/latest-handoff.md` using
  `system/handoff/update-handoff-runbook.md` when work pauses, becomes blocked,
  changes Active Workflow, Active Phase, Active Runbook, Active Agent, or
  Active Executor.
- Record Active Workflow, Active Phase, Active Runbook, Active Agent, Active
  Executor, exact context loaded, files changed, validation, risks, and next
  step.

## Done Criteria

- Required outputs exist.
- Required approvals and validation evidence exist.
- No unresolved blocking condition remains.
- Final workflow status is recorded.

## Registry Update Requirements

- Add or update the exact workflow entry in
  `system/registries/workflows-index.md`.
- Update `system/registries/runbooks-index.md`,
  `system/registries/rules-index.md`, routing registries, or output contracts
  only when their exact entries change.
- Do not duplicate canonical registry content inside the workflow contract.

## Uncertainty

- Record unresolved structural or ownership questions without inventing new
  components.
