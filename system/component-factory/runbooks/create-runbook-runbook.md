---
file_type: "Factory Runbook"
primary_agents: ["PO", "BA", "Architect", "Data", "BE", "UIUX", "FE", "QA", "Release"]
supporting_agents: []
activation_mode: "Triggered By Workflow"
lifecycle_stage: "System Core"
purpose: "Create a new runtime runbook through the isolated Component Factory workflow."
---
# Create Runbook Runbook

## Purpose

Create a new runtime runbook for a repeatable workflow.

## When To Use

Use when a workflow is repeated often enough to deserve a stable runbook.

## Prerequisites

- checked `system/runbooks/`
- checked related runtime skills and templates

## Steps

1. Confirm the workflow is not already covered.
2. Define the target component or output type.
3. Use `templates/runbook-template.md`.
4. Bind the correct skills, templates, and validation steps.
5. Produce `artifacts/component-creation-report.md`.

## Validation Checklist

- purpose is clear
- steps are actionable
- expected output is explicit
- recovery note exists

## Expected Output

- a runbook definition ready for runtime placement
- a creation report

## Recovery / Rollback Note

If the workflow is really a skill or rule, stop and redirect component type.
