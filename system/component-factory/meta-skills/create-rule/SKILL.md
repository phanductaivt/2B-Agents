---
name: create-rule
description: Use when a new runtime Rule is needed to guide execution behavior consistently and existing Rules are insufficient; do not use for creating project-specific requirement content.
---
# Create Rule

## Purpose

Create a new runtime rule through Component Factory.

## Steps

1. Check `system/rules/` for overlap or conflict.
2. Read the factory rules and guardrails for scope, naming, dependency, and safety.
3. Use `runbooks/create-rule-runbook.md`.
4. Use `templates/rule-template.md`.
5. Produce `artifacts/component-creation-report.md`.

## Prohibited Actions

- do not create a rule that duplicates an existing guardrail or runbook
- do not sneak runtime redesign into a rule creation request
