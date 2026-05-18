---
name: skill-master-framework
description: Use when defining or refining the overall method for how Component Factory creates, reviews, updates, and quality-controls Skills, Rules, Guardrails, Runbooks, Templates, and Artifacts; do not use for creating business delivery outputs directly.
---
# Skill Master Framework

## Purpose

Provide the master operating pattern for all Component Factory meta-skills.

## Required Behavior

1. Check the current repository before creating anything.
2. Identify whether the requested work is:
   - create
   - review
   - update
3. Route to the correct Component Factory runbook.
4. Route to the correct Component Factory template.
5. Enforce Component Factory rules and guardrails.
6. Produce the required report artifact.

## Required Checks

- search related runtime folders first
- confirm no duplicate component already exists
- confirm the requested component belongs to the target type
- confirm the request is not asking for direct business output generation

## Prohibited Actions

- do not create business delivery outputs
- do not delete runtime files
- do not rename runtime files
- do not move runtime files
- do not overwrite existing files without explicit approval

## Output

- a controlled component change aligned with the factory rules
- a matching creation, review, or change report
