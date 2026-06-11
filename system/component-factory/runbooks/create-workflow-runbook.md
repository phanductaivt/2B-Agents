---
file_type: "Factory Runbook"
primary_agents: []
supporting_agents: ["PO", "BA", "Architect", "Data", "BE", "UIUX", "FE", "QA", "Release"]
activation_mode: "Triggered By Workflow"
lifecycle_stage: "System Core"
purpose: "Create a new executor-neutral workflow contract through the isolated Component Factory workflow."
---
# Create Workflow Runbook

## Purpose

Create one registered workflow contract that coordinates phases, one Active
Agent and one Active Runbook per phase, gates, outputs, recovery, and handoff.

## When To Use

Use only when a repeatable multi-phase operation is not already governed by an
existing workflow contract.

## Required Context

- `system/executors/executor-contract.md`
- `system/handoff/README.md`
- `system/workflows/workflow-contract-template.md`
- `system/workflows/workflow-lifecycle.md`
- `system/component-factory/component-types-index.md`
- `system/component-factory/meta-skills/create-workflow/SKILL.md`
- `system/component-factory/rules/component-creation-rules.md`
- `system/component-factory/rules/component-dependency-rules.md`
- `system/component-factory/rules/component-naming-rules.md`
- `system/component-factory/rules/component-scope-rules.md`
- `system/component-factory/guardrails/component-file-operation-guardrails.md`
- `system/component-factory/guardrails/component-overlap-guardrails.md`
- `system/component-factory/guardrails/component-hallucination-guardrails.md`
- `system/component-factory/guardrails/component-breaking-change-guardrails.md`
- `system/registries/workflows-index.md`
- `system/registries/runbooks-index.md`
- `system/registries/rules-index.md`
- only the Agent, runbook, rule, guardrail, skill, and output-contract entries
  needed for the proposed workflow

## Prerequisites

- workflow purpose and trigger are distinct from registered workflows
- proposed phases and phase transitions are known
- existing runbooks have been checked before proposing new ones

## Steps

1. Confirm the request requires a workflow rather than one runbook.
2. Check `system/registries/workflows-index.md` for overlap.
3. Define Workflow ID, purpose, trigger, required inputs, phases, Active Agent
   per phase, one Active Runbook per phase, required skills/rules/guardrails,
   outputs, approval gates, stop conditions, recovery rules, handoff
   requirements, and done criteria.
4. Use the canonical `system/workflows/workflow-contract-template.md`.
5. Verify each named Agent and runbook exists; use `Active Agent: None` when no
   instruction-defined Agent owns a governance or orchestration phase.
6. Create the contract at `system/workflows/<workflow-id>-workflow.md`.
7. Update `system/registries/workflows-index.md`.
8. Update `system/registries/runbooks-index.md` or
   `system/registries/rules-index.md` only when their entries actually change.
9. Record exact dependencies checked and registry changes in the Component
   Factory creation report.

## Validation Checklist

- Workflow ID, purpose, trigger, and required inputs are explicit
- every phase has exactly one Active Runbook
- every phase has one Active Agent or explicit `None`
- skills, rules, guardrails, and outputs are narrowly routed
- approval gates, stop conditions, recovery rules, handoff requirements, and
  done criteria are explicit
- phase transitions follow `system/workflows/workflow-lifecycle.md`
- `system/registries/workflows-index.md` is updated
- no governance, router, or factory Agent was invented

## Expected Output

- `system/workflows/<workflow-id>-workflow.md`
- updated `system/registries/workflows-index.md`
- only required runbook/rule registry updates
- `system/component-factory/artifacts/component-creation-report.md`

## Stop / Approval Conditions

- Stop if the workflow overlaps an existing workflow or silently combines
  unrelated workflows.
- Stop if any phase has multiple active runbooks or ambiguous Agent ownership.
- Stop if a required runbook, output contract, approval gate, or recovery route
  cannot be identified.

## Recovery / Rollback Note

If the request is a single repeatable procedure, redirect to Runbook creation
instead of creating a workflow.
