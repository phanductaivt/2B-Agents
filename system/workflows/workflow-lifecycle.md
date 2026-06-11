---
file_type: "Workflow Lifecycle"
primary_agents: []
supporting_agents: ["PO", "BA", "Architect", "Data", "BE", "UIUX", "FE", "QA", "Release"]
activation_mode: "Always-On Workflow Governance"
lifecycle_stage: "System Core"
purpose: "Define executor-neutral workflow selection, state, transitions, recovery, and handoff behavior."
---
# Workflow Lifecycle

## Selection

1. Identify the user goal, active project, and task ID.
2. Select one workflow from `system/registries/workflows-index.md`.
3. Load the selected workflow contract.
4. Confirm the current workflow state and active phase.
5. Load only the active phase runbook and its declared context.

If no workflow matches, stop and record the uncertainty. Do not silently
combine workflows or invent a new workflow.

## State Model

| State | Meaning |
| --- | --- |
| `Not Started` | Trigger identified, but required inputs or workflow selection are not confirmed. |
| `Active` | One phase is executing under its required runbook. |
| `Pending Approval` | A declared approval gate blocks further execution. |
| `Paused` | Work stopped at a safe boundary and can resume from handoff. |
| `Blocked` | Required input, capability, decision, or safe recovery route is missing. |
| `Recovering` | A declared clarification, regeneration, or rollback route is active. |
| `Complete` | Done criteria are satisfied and recorded. |
| `Cancelled` | The user ended the workflow without completing it. |

## Phase Transition Rule

Before changing phases, the AI Executor must confirm:

- the current phase exit condition is satisfied
- required outputs and evidence exist
- required approval is explicit
- the next phase entry condition is satisfied
- the next active Agent and runbook are identified

Only one phase and one runbook are active at a time. Load the next phase context
only after the transition is confirmed.

## Approval Rule

An Agent or AI Executor may recommend a decision. Only the user or other
explicitly named approver can approve a workflow gate.

Do not infer approval from output existence, prior recommendations, or work
performed by a previous AI Executor.

## Recovery Rule

Use only recovery routes declared by the active workflow:

- clarification for missing or conflicting meaning
- targeted regeneration for an affected approved artifact
- rollback for an applied change with an approved rollback scope
- blocked handoff when no safe recovery route exists

Recovery does not silently change the workflow, phase ownership, or approval
scope.

## Handoff Rule

Follow `system/handoff/update-handoff-runbook.md` whenever:

- work pauses or becomes blocked
- Active Workflow, Active Phase, Active Runbook, Active Agent, Active Executor,
  or active project changes
- material validation or risk state changes

For an AI Executor change, also follow
`system/handoff/switch-ai-executor-runbook.md`.

## Completion Rule

A workflow is complete only when its contract's done criteria are met. Record
the final status, outputs, validation evidence, unresolved non-blocking risks,
and recommended next step in the canonical handoff.
