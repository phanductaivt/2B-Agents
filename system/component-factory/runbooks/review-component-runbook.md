---
file_type: "Factory Runbook"
primary_agents: ["PO", "BA", "Architect", "Data", "BE", "UIUX", "FE", "QA", "Release"]
supporting_agents: []
activation_mode: "Triggered By Workflow"
lifecycle_stage: "System Core"
purpose: "Review an existing runtime component through the isolated Component Factory workflow."
---
# Review Component Runbook

## Purpose

Review a component for naming, scope, dependency, overlap, and safety quality.

## When To Use

Use when auditing or evaluating an existing runtime component.

## Prerequisites

- identified target component
- identified component type
- selected type route from `system/component-factory/component-types-index.md`

## Type-Specific Required Context

- Agent review: target `system/agents/<role>/AGENT.md`, exact
  `system/registries/agents-index.md` entry, and only relevant skill, rule,
  guardrail, runbook, output-contract, Executor, and handoff references.
- Workflow review: target `system/workflows/<workflow-id>-workflow.md`,
  `system/workflows/workflow-lifecycle.md`, exact
  `system/registries/workflows-index.md` entry, and only relevant runbook, rule,
  output-contract, Executor, and handoff references.
- Do not bulk-read Agent, Workflow, registry, or system folders.

## Steps

1. Read the target component.
2. Search related runtime folders for overlap.
3. Check naming, scope, dependency, and breakage risk.
4. For an Agent, verify identity, ownership, non-responsibilities, inputs,
   outputs, skills, rules/guardrails, runbooks, handoff, boundaries, usage
   examples, and `system/registries/agents-index.md` alignment.
5. For a Workflow, verify ID, trigger, phases, one Active Agent or `None` and
   one Active Runbook per phase, routing, outputs, gates, stops, recovery,
   handoff, done criteria, and `system/registries/workflows-index.md` alignment.
6. Use `templates/component-review-template.md`.
7. Produce `artifacts/component-review-report.md`.

## Validation Checklist

- overlap risk checked
- dependency risk checked
- naming fit checked
- update safety checked
- canonical registry alignment checked
- Agent or Workflow type-specific contract checked when applicable

## Expected Output

- a review report with findings and recommendations

## Recovery / Rollback Note

If evidence is insufficient, stop and mark the review incomplete instead of guessing.
