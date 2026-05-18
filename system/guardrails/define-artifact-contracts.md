---
file_type: "Guardrail"
primary_agents: ["PO", "BA", "Architect", "Data", "BE", "UIUX", "FE", "QA", "Release"]
supporting_agents: []
activation_mode: "Always-On Shared"
lifecycle_stage: "System Core"
purpose: "Define what each artifact must contain and how it should relate to upstream and downstream outputs."
---
# Define Artifact Contracts

Artifacts should stay practical, reviewable, and easy to regenerate.

## PO Package

Write directly to `02-output/po/`:
- `<req>-brd.md`
- or `<initiative>-brd.md`

## BA Package

Write directly to `02-output/ba/`:
- `<req>-clarification.md`
- `<req>-process-bpmn.md`
- `<req>-user-story.md`
- `<req>-acceptance-criteria.md`
- `<req>-frs.md`
- `<req>-feature-list.md`

## BE Package

Write directly to `02-output/be/`:
- `<req>-be-spec.md`
- `<req>-api-contract.md`

## Architecture Package

Write directly to `02-output/architecture/`:
- `<req>-architecture-note.md`
- `<req>-nfr-review.md`
- `<req>-security-review.md`

## Data Package

Write directly to `02-output/data/`:
- `<req>-data-model.md`
- `<req>-state-transition.md`
- `<req>-schema-plan.md`
- `<req>-metric-tracking-plan.md`

## QA Package

Write directly to `02-output/qa/`:
- `<req>-test-scenarios.md`
- `<req>-test-cases.md`
- `<req>-smoke-test-plan.md`
- `<req>-release-readiness.md`

## Design Package

Write directly to `02-output/design/`:
- `<req>-wireframe.md`

## FE Package

Write directly to `02-output/fe/`:
- `<req>-ui.html`
- `<req>-fe-implementation-plan.md`

## BE Package

Write directly to `02-output/be/`:
- `<req>-be-spec.md`
- `<req>-api-contract.md`
- `<req>-be-implementation-plan.md`

## Release Package

Write directly to `02-output/release/`:
- `<req>-run-instructions.md`
- `<req>-runnable-system-verification.md`
- `<req>-release-readiness.md`

## Runnable App Package

Generated runnable app code belongs in:
- `02-output/app/backend/`
- `02-output/app/frontend/`

A project must not be called runnable unless verification records:
- backend start or test command
- frontend start or build command
- database setup command
- at least one smoke or test command
- actual command result or explicit reason a command could not be run

## Change Request Package

Change request intake belongs in:
- `01-input/change-requests/<cr-id>.md`

Change analysis outputs belong in:
- `02-output/change-analysis/<cr-id>-impact-analysis.md`
- `02-output/change-analysis/<cr-id>-regeneration-plan.md`
- `02-output/change-analysis/<cr-id>-rollback-plan.md`
- `02-output/change-analysis/<cr-id>-verification.md`
- `02-output/change-analysis/change-log.md`

Baseline snapshots belong in:
- `05-baselines/before-<cr-id>/baseline-manifest.md`
- `05-baselines/before-<cr-id>/files/`

Change request artifacts must not replace the linked requirement until the CR is approved, applied, verified, and merged.
