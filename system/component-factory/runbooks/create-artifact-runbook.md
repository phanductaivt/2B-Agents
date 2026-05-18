---
file_type: "Factory Runbook"
primary_agents: ["PO", "BA", "Architect", "Data", "BE", "UIUX", "FE", "QA", "Release"]
supporting_agents: []
activation_mode: "Triggered By Workflow"
lifecycle_stage: "System Core"
purpose: "Create a new artifact contract or artifact standard through the isolated Component Factory workflow."
---
# Create Artifact Runbook

## Purpose

Create a new artifact contract or artifact-supporting runtime standard.

## When To Use

Use when the runtime artifact layer needs a new controlled artifact definition.

## Prerequisites

- checked `system/artifacts/`
- checked runtime naming and scope rules

## Steps

1. Confirm the target artifact type.
2. Search the runtime artifact layer for overlap.
3. Use `templates/artifact-contract-template.md`.
4. Define owner, path, output naming, and scope.
5. Produce `artifacts/component-creation-report.md`.

## Validation Checklist

- artifact type is explicit
- owner is explicit
- output shape is explicit
- no project-output confusion exists

## Expected Output

- an artifact contract definition ready for runtime placement
- a creation report

## Recovery / Rollback Note

If the request is really for a template or runbook, stop and redirect.
