---
file_type: "Workflow Contract"
workflow_id: "component-governance"
primary_agents: []
supporting_agents: ["PO", "BA", "Architect", "Data", "BE", "UIUX", "FE", "QA", "Release"]
activation_mode: "User Request"
lifecycle_stage: "System Core"
purpose: "Govern controlled creation, review, and update of runtime system components through Component Factory."
---
# Component Governance Workflow

## Workflow ID

- `component-governance`

## Purpose

Govern creation, review, and update of supported system components through
Component Factory without creating a governance Agent.

## Trigger

- A user requests creation, review, or update of a Skill, Rule, Guardrail,
  Runbook, Template, Artifact contract, Agent, or Workflow.
- Do not use for project delivery outputs or application implementation.

## Required Inputs

- exact component request and target path, when known
- exact existing component and checked dependencies for review/update
- `system/executors/executor-contract.md`
- `system/workflows/workflow-lifecycle.md`
- `system/component-factory/README.md`
- `system/component-factory/component-types-index.md`
- `system/registries/runbooks-index.md`
- `system/registries/rules-index.md`
- relevant existing registry entries for the target component type
- `system/registries/output-contracts.md` only when the target component creates
  or changes a project output contract

## Active Phases

No instruction-defined Agent currently owns Component Factory governance.
`Active Agent` remains `None`; the AI Executor follows the selected factory
runbook, meta-skill, rules, and guardrails.

| Phase | Active Agent | Required Runbook | Entry Condition | Required Skills / Rules / Guardrails | Required Outputs | Exit Condition |
| --- | --- | --- | --- | --- | --- | --- |
| Classify request | None | Selected factory create, review, or update runbook | Component request received | `system/component-factory/rules/component-scope-rules.md`; relevant overlap guardrail | Component type and operation decision | Correct route selected |
| Create component | None | One exact runbook from the Creation Route Table below | New component justified | Matching creation meta-skill; creation, naming, scope, dependency rules; relevant factory guardrails | Target component and creation report | Validation checklist passes |
| Review component | None | `system/component-factory/runbooks/review-component-runbook.md` | Existing target identified | `system/component-factory/meta-skills/system-auditor/SKILL.md`; dependency, scope, overlap, hallucination, breaking-change controls | Component review report | Evidence supports findings |
| Update component | None | `system/component-factory/runbooks/update-component-runbook.md` | Existing target and approved update scope identified | Update, dependency, naming, scope rules; file-operation, overlap, hallucination, breaking-change guardrails | Controlled update and change log; review report when needed | Dependency and safety checks pass |

### Creation Route Table

| Component Type | Required Runbook | Required Meta-Skill |
| --- | --- | --- |
| Skill | `system/component-factory/runbooks/create-skill-runbook.md` | `system/component-factory/meta-skills/create-skill/SKILL.md` |
| Rule | `system/component-factory/runbooks/create-rule-runbook.md` | `system/component-factory/meta-skills/create-rule/SKILL.md` |
| Guardrail | `system/component-factory/runbooks/create-guardrail-runbook.md` | `system/component-factory/meta-skills/create-guardrail/SKILL.md` |
| Runbook | `system/component-factory/runbooks/create-runbook-runbook.md` | `system/component-factory/meta-skills/create-runbook/SKILL.md` |
| Template | `system/component-factory/runbooks/create-template-runbook.md` | `system/component-factory/meta-skills/create-template/SKILL.md` |
| Artifact | `system/component-factory/runbooks/create-artifact-runbook.md` | `system/component-factory/meta-skills/create-artifact/SKILL.md` |
| Agent | `system/component-factory/runbooks/create-agent-runbook.md` | `system/component-factory/meta-skills/create-agent/SKILL.md` |
| Workflow | `system/component-factory/runbooks/create-workflow-runbook.md` | `system/component-factory/meta-skills/create-workflow/SKILL.md` |

Select one route only. Load only its matching runbook, meta-skill, template,
rules, and guardrails.

## Required Skills / Rules / Guardrails

- Creation uses only the matching meta-skill from the Creation Route Table.
- Review uses `system/component-factory/meta-skills/system-auditor/SKILL.md`.
- Rules are selected from `system/registries/rules-index.md` for the active
  component operation only.
- Guardrails are selected by exact risk only:
  - `system/component-factory/guardrails/component-file-operation-guardrails.md`
  - `system/component-factory/guardrails/component-overlap-guardrails.md`
  - `system/component-factory/guardrails/component-hallucination-guardrails.md`
  - `system/component-factory/guardrails/component-breaking-change-guardrails.md`

## Approval Gates

- Breaking or structural change gate:
  - required approver: user
  - evidence: dependency and breakage impact
  - blocked actions: delete, rename, move, destructive overwrite, silent scope
    change, or broad runtime redesign

## Stop Conditions

- Stop when component type, target path, ownership, overlap, dependency impact,
  or approval is unclear.
- Stop if the request is actually for a project output or application change.
- Stop if a new component duplicates an existing component.
- Stop before any prohibited file operation without explicit approval.

## Recovery Rules

- If overlap exists, recommend updating the existing component.
- If evidence is insufficient, produce an incomplete review with uncertainty.
- If a proposed update is breaking, propose a staged plan instead of applying
  it.
- If the component type is wrong, return to classification.

## Handoff Requirements

- Update `system/handoff/latest-handoff.md` whenever Active Workflow, Active
  Phase, Active Runbook, Active Agent, or Active Executor changes, and when
  governance work pauses, becomes blocked, changes target, or changes
  operation.
- Record exact target components, dependencies inspected, selected factory
  runbook, files changed, validation, approval state, and uncertainty.

## Done Criteria

- The selected factory runbook validation checklist passes.
- Required Component Factory report or change log exists.
- Required exact registry updates are complete and dependency impacts are
  recorded.
- No unapproved destructive or breaking operation occurred.

## Uncertainty

- Existing legacy Component Factory runbooks predate the standard runtime
  `Required Context` structure. New Agent and Workflow creation routes declare
  exact context; broader legacy alignment remains outside Phase 3.
