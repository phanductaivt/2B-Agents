---
name: create-guardrail
description: Use when a new runtime Guardrail is needed to prevent unsafe, duplicate, hallucinated, or breaking behavior and existing guardrails do not already cover the risk; do not use for general documentation writing.
---
# Create Guardrail

## Purpose

Create a new runtime guardrail through Component Factory.

## Steps

1. Check `system/guardrails/` for existing risk coverage.
2. Read Component Factory rules for naming, scope, dependency, and updates.
3. Use `runbooks/create-guardrail-runbook.md`.
4. Use `templates/guardrail-template.md`.
5. Produce `artifacts/component-creation-report.md`.

## Prohibited Actions

- do not create a guardrail that only restates a rule with no safety value
- do not create a guardrail with no trigger condition or stop condition
