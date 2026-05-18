---
file_type: "Factory Runbook"
primary_agents: ["PO", "BA", "Architect", "Data", "BE", "UIUX", "FE", "QA", "Release"]
supporting_agents: []
activation_mode: "Triggered By Workflow"
lifecycle_stage: "System Core"
purpose: "Create a new runtime skill through the isolated Component Factory workflow."
---
# Create Skill Runbook

## Purpose

Create a new runtime skill safely and without duplicating existing capabilities.

## When To Use

Use when a new reusable runtime skill is needed.

## Prerequisites

- checked `system/skills/`
- checked Component Factory rules
- checked Component Factory guardrails

## Steps

1. Search `system/skills/` for overlap.
2. Confirm the request is truly for a skill.
3. Use `templates/skill-template.md`.
4. Draft the skill using the required structure.
5. Validate naming, scope, dependency, and overlap.
6. Produce `artifacts/component-creation-report.md`.

## Validation Checklist

- no duplicate skill exists
- naming matches runtime convention
- scope is narrow and reusable
- dependencies are explicit

## Expected Output

- a skill definition ready for runtime placement
- a creation report

## Recovery / Rollback Note

If overlap or breakage risk appears, stop and recommend updating an existing skill instead.
