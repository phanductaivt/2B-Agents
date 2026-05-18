---
file_type: "Factory Runbook"
primary_agents: ["PO", "BA", "Architect", "Data", "BE", "UIUX", "FE", "QA", "Release"]
supporting_agents: []
activation_mode: "Triggered By Workflow"
lifecycle_stage: "System Core"
purpose: "Create a new runtime guardrail through the isolated Component Factory workflow."
---
# Create Guardrail Runbook

## Purpose

Create a new runtime guardrail that reduces risk clearly.

## When To Use

Use when a known unsafe pattern is not already controlled.

## Prerequisites

- checked `system/guardrails/`
- checked risk overlap

## Steps

1. Identify the risk category.
2. Confirm no existing guardrail already covers the trigger.
3. Use `templates/guardrail-template.md`.
4. Define trigger, prohibited actions, required checks, stop condition, and safe fallback.
5. Produce `artifacts/component-creation-report.md`.

## Validation Checklist

- risk is specific
- trigger is explicit
- fallback is safe
- no overlap remains unresolved

## Expected Output

- a guardrail definition ready for runtime placement
- a creation report

## Recovery / Rollback Note

If the risk is already covered elsewhere, stop and document overlap instead.
