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

## Steps

1. Read the target component.
2. Search related runtime folders for overlap.
3. Check naming, scope, dependency, and breakage risk.
4. Use `templates/component-review-template.md`.
5. Produce `artifacts/component-review-report.md`.

## Validation Checklist

- overlap risk checked
- dependency risk checked
- naming fit checked
- update safety checked

## Expected Output

- a review report with findings and recommendations

## Recovery / Rollback Note

If evidence is insufficient, stop and mark the review incomplete instead of guessing.
