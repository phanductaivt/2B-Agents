---
name: system-auditor
description: Use when reviewing existing runtime components for overlap, dependency drift, naming inconsistency, missing metadata, or safety weaknesses inside the AI operating system; do not use for project delivery review.
---
# System Auditor

## Purpose

Review runtime system components through the isolated Component Factory layer.

## Steps

1. Identify the target component type and folder.
2. Check related runtime folders before making any recommendation.
3. Use `runbooks/review-component-runbook.md`.
4. Use `templates/component-review-template.md`.
5. Produce `artifacts/component-review-report.md`.

## Required Checks

- overlap risk
- naming consistency
- scope fitness
- dependency clarity
- update safety
- metadata quality
- canonical registry alignment
- Agent ownership and boundary completeness when reviewing an Agent
- Workflow phase, one-active-runbook, lifecycle, gate, and handoff completeness
  when reviewing a Workflow

## Prohibited Actions

- do not delete files during review
- do not rename files during review
- do not move files during review
- do not claim a breakage risk without checking the repository
