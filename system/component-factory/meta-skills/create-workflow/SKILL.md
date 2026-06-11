---
name: create-workflow
description: Use when a distinct repeatable multi-phase operation needs an executor-neutral workflow contract and no existing workflow can be safely extended; do not use for a single procedure or ad hoc task.
---
# Create Workflow

## Purpose

Create a registered executor-neutral workflow contract through Component
Factory.

## Steps

1. Check `system/registries/workflows-index.md` for overlap.
2. Check only the candidate phase runbooks and their relevant registry entries.
3. Use `system/component-factory/runbooks/create-workflow-runbook.md`.
4. Use the canonical `system/workflows/workflow-contract-template.md`.
5. Update `system/registries/workflows-index.md` and only other registries whose
   entries actually change.
6. Produce the Component Factory creation report.

## Required Checks

- stable Workflow ID, purpose, trigger, inputs, phases, outputs, gates, recovery,
  handoff, and done criteria
- one Active Agent or explicit `None` per phase
- exactly one Active Runbook per phase
- exact, narrow skills/rules/guardrails routing

## Prohibited Actions

- do not create a workflow that duplicates or silently combines registered
  workflows
- do not assign multiple active runbooks to one phase
- do not invent an Agent to fill an orchestration or governance phase
