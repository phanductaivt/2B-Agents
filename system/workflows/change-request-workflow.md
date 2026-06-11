---
file_type: "Workflow Contract"
workflow_id: "change-request"
primary_agents: ["PO", "BA", "Architect", "Data", "BE", "UIUX", "FE", "QA", "Release"]
supporting_agents: []
activation_mode: "User Request"
lifecycle_stage: "System Core"
purpose: "Govern a post-baseline project change from intake through approval, controlled apply, verification, merge, or rollback."
---
# Change Request Workflow

## Workflow ID

- `change-request`

## Purpose

Control changes to an existing stable project. The workflow defines control
state and phase ownership; `system/runbooks/handle-change-request.md` remains
the detailed procedure.

## Trigger

- A stable project receives a customer change or customization request.
- Do not use for first-time project generation.

## Required Inputs

- `projects/<project>/01-input/requirements/<linked-req>.md`
- `projects/<project>/01-input/change-requests/<cr-id>.md`
- relevant project context and only affected current outputs
- `system/executors/executor-contract.md`
- `system/workflows/workflow-lifecycle.md`
- `system/runbooks/handle-change-request.md`
- `system/registries/context-routing.md`
- `system/registries/output-contracts.md`
- `system/registries/runbooks-index.md`
- `system/registries/rules-index.md`

## Active Phases

The orchestration phases have no instruction-defined Agent. Artifact analysis,
apply, and verification activate only the owning Agent identified by
`system/registries/output-contracts.md` and the approved regeneration plan.

| Phase | Active Agent | Required Runbook | Entry Condition | Required Skills / Rules / Guardrails | Required Outputs | Exit Condition |
| --- | --- | --- | --- | --- | --- | --- |
| Intake | None | `system/runbooks/handle-change-request.md` | Change request received | CR runbook Required Context | `01-input/change-requests/<cr-id>.md` | Stable CR ID and linked requirement recorded |
| Impact analysis | Owning Agent per affected artifact, only when needed | `system/runbooks/handle-change-request.md` | Intake complete | CR runbook Required Context; no artifact skill unless needed for analysis | `02-output/change-analysis/<cr-id>-impact-analysis.md` | Impact and recommendation recorded |
| Approval decision | None | `system/runbooks/handle-change-request.md` | Impact analysis complete | CR runbook rules and guardrails | Approval state or rejection record | Explicit user decision recorded |
| Regeneration and rollback planning | None | `system/runbooks/handle-change-request.md` | CR approved | CR runbook Required Context | Regeneration and rollback plans | Exact affected files, recovery scope, apply runbook, and verification runbook recorded |
| Baseline | None | `system/runbooks/handle-change-request.md` | Approved plans available and Git is not rollback layer | CR runbook Required Context | Baseline manifest and required snapshots | Baseline status recorded |
| Apply approved change | Owning Agent for the current approved target | Exact apply runbook recorded in the approved plan | Approval and baseline conditions satisfied; exact apply runbook recorded | Exact apply runbook Required Context only | Only approved target files | All planned targets applied or workflow blocked |
| Verification | Exact one verification Agent recorded in the approved plan | Exact verification runbook recorded in the approved plan | Approved changes applied; coordinator runbook inactive; exact verification runbook recorded | Exact verification runbook Required Context only | `02-output/change-analysis/<cr-id>-verification.md` and named evidence | Evidence supports Verified or recovery decision |
| Merge | None | `system/runbooks/handle-change-request.md` | Verification passed | CR runbook Required Context | Linked requirement and change log updated | CR status `Merged` |
| Rollback | Owning Agent only when required by approved rollback plan | `system/runbooks/handle-change-request.md` | Applied change is cancelled, rejected, or unsafe | Approved rollback plan and baseline only | Restored files and rollback evidence | CR status `Rolled Back` |

## Required Skills / Rules / Guardrails

- Intake, impact, approval, planning, baseline, merge, and rollback use only the
  exact rules and guardrails declared by
  `system/runbooks/handle-change-request.md`.
- Apply and verification load only the exact skills, rules, and guardrails
  declared by the approved target runbook.
- Do not load artifact-generation skills before approval.
- `system/runbooks/handle-change-request.md` is active during coordinator
  phases. Before Apply or Verification begins, transition from the coordinator
  to the one exact runbook recorded in the approved plan. Return to the
  coordinator only after that runbook records its required evidence.

## Approval Gates

- Apply gate:
  - required approver: user
  - evidence: impact analysis with recommended decision
  - allowed decisions: approve, reject, revise
  - blocked actions: regeneration, implementation, baseline apply, requirement merge
- Scope expansion gate:
  - required approver: user
  - evidence: revised impact analysis and regeneration plan
  - blocked actions: changes outside the approved plan

## Stop Conditions

- Stop after impact analysis until explicit approval.
- Stop if the linked requirement, CR ID, affected files, ownership, rollback
  scope, or required baseline is unclear.
- Stop when a discovered impact exceeds the approved plan.
- Stop before Apply or Verification when the approved plan does not record the
  exact one active runbook for that phase.
- Stop before merge unless verification evidence exists.

## Recovery Rules

- Revised request: update intake and rerun impact analysis only.
- Failed or unsafe apply: follow the approved rollback plan.
- Newly discovered scope: return to impact analysis and approval.
- Ambiguous affected artifact: stop instead of loading broad output folders.

## Handoff Requirements

- Update `system/handoff/latest-handoff.md` whenever Active Workflow, Active
  Phase, Active Runbook, Active Agent, or Active Executor changes, and at
  approval waits, baseline completion, interruptions, verification, rollback,
  or completion.
- Record CR ID, status, exact approved targets, active Agent/runbook, baseline
  path, validation evidence, and next safe action.
- Follow `system/handoff/switch-ai-executor-runbook.md` when the AI Executor
  changes.

## Done Criteria

- CR status is `Merged`, `Rolled Back`, or `Rejected`.
- Approval and verification evidence are recorded.
- Only approved files changed.
- Change log and linked requirement are updated when the CR is merged.
- No unresolved rollback or traceability gap remains.

## Uncertainty

- No dedicated orchestration Agent exists for change control. Orchestration
  phases therefore use `Active Agent: None`; owned artifact work activates the
  corresponding existing Agent.
