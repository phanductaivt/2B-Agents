---
file_type: "Factory Runbook"
primary_agents: ["PO", "BA", "Architect", "Data", "BE", "UIUX", "FE", "QA", "Release"]
supporting_agents: []
activation_mode: "Triggered By Workflow"
lifecycle_stage: "System Core"
purpose: "Create a new runtime rule through the isolated Component Factory workflow."
---
# Create Rule Runbook

## Purpose

Create a new runtime rule safely.

## When To Use

Use when a repeatable operating rule is missing.

## Prerequisites

- checked `system/rules/`
- checked overlap and naming rules

## Steps

1. Search for an existing rule that already covers the need.
2. Confirm the request is rule-level, not guardrail-level or runbook-level.
3. Use `templates/rule-template.md`.
4. Draft the rule with clear scope and usage.
5. Validate naming and dependency impact.
6. Produce `artifacts/component-creation-report.md`.

## Validation Checklist

- rule purpose is clear
- rule does not duplicate a guardrail
- runtime dependency impact is visible

## Expected Output

- a rule definition ready for runtime placement
- a creation report

## Recovery / Rollback Note

If the rule duplicates an existing control, stop and recommend extension instead.
