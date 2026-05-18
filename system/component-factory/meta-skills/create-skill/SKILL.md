---
name: create-skill
description: Use when a new runtime Skill is needed and no suitable existing Skill already covers the job; do not use for writing BRDs, FRSs, UI screens, or other business outputs directly.
---
# Create Skill

## Purpose

Create a new runtime skill safely through Component Factory.

## Steps

1. Check `system/skills/` for overlapping skills.
2. Read:
   - `rules/component-creation-rules.md`
   - `rules/component-naming-rules.md`
   - `rules/component-scope-rules.md`
   - `guardrails/component-overlap-guardrails.md`
   - `guardrails/component-file-operation-guardrails.md`
3. Use `runbooks/create-skill-runbook.md`.
4. Use `templates/skill-template.md`.
5. Produce `artifacts/component-creation-report.md`.

## Prohibited Actions

- do not duplicate an existing skill with minor wording changes
- do not modify existing runtime files without explicit approval
- do not create a skill for direct project output generation inside Component Factory
