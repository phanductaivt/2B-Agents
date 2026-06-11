---
file_type: "Factory Runbook"
primary_agents: ["PO", "BA", "Architect", "Data", "BE", "UIUX", "FE", "QA", "Release"]
supporting_agents: []
activation_mode: "Triggered By Workflow"
lifecycle_stage: "System Core"
purpose: "Update an existing runtime component through the isolated Component Factory workflow."
---
# Update Component Runbook

## Purpose

Update an existing runtime component safely.

## When To Use

Use when an existing component should be improved rather than replaced.

## Prerequisites

- reviewed current component
- checked related runtime dependencies
- selected type route from `system/component-factory/component-types-index.md`

## Type-Specific Required Context

- Agent update: target `system/agents/<role>/AGENT.md`, exact
  `system/registries/agents-index.md` entry, approved ownership impact, and only
  affected skill, rule, guardrail, runbook, output-contract, Executor, and
  handoff references.
- Workflow update: target `system/workflows/<workflow-id>-workflow.md`,
  `system/workflows/workflow-lifecycle.md`, exact
  `system/registries/workflows-index.md` entry, approved lifecycle impact, and
  only affected runbook, rule, output-contract, Executor, and handoff
  references.
- Do not bulk-read Agent, Workflow, registry, or system folders.

## Steps

1. Read the current component.
2. Identify the narrowest safe update.
3. Check naming, scope, and dependency impact.
4. For an Agent update, check ownership, output contracts, workflows, runbooks,
   skills/rules, usage matrix, registry entry, and handoff impact.
5. For a Workflow update, check phase identity, one-active-runbook behavior,
   Agent routing, gates, lifecycle transitions, output contracts, registry
   entry, and handoff impact.
6. Apply only the necessary change.
7. Update only exact registry entries affected by the approved change.
8. Record the update in `artifacts/component-change-log.md`.
9. Produce `artifacts/component-review-report.md` when review context is needed.

## Validation Checklist

- no unsafe rename or move happened
- dependency impact was checked
- update did not create overlap
- rationale is documented
- affected registry entries are aligned
- Agent ownership or Workflow lifecycle behavior did not drift silently

## Expected Output

- a controlled component update
- a change log entry

## Recovery / Rollback Note

If the update would create a breaking change, stop and recommend a staged plan.
