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

## Steps

1. Read the current component.
2. Identify the narrowest safe update.
3. Check naming, scope, and dependency impact.
4. Apply only the necessary change.
5. Record the update in `artifacts/component-change-log.md`.
6. Produce `artifacts/component-review-report.md` when review context is needed.

## Validation Checklist

- no unsafe rename or move happened
- dependency impact was checked
- update did not create overlap
- rationale is documented

## Expected Output

- a controlled component update
- a change log entry

## Recovery / Rollback Note

If the update would create a breaking change, stop and recommend a staged plan.
