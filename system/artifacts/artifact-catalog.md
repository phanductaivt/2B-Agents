---
file_type: "Artifact Contract Index"
primary_agents: ["PO", "BA", "Architect", "Data", "BE", "UIUX", "FE", "QA", "Release"]
supporting_agents: []
activation_mode: "Always-On Shared"
lifecycle_stage: "System Core"
purpose: "Define the canonical artifact set, owners, and final output locations."
---
# Artifact Catalog

## PO Artifact

- `brd`
  - output: `<req>-brd.md` or `<initiative>-brd.md`
  - path: `02-output/po/`
  - owner: PO

## BA Artifacts

- `clarification`
  - output: `<req>-clarification.md`
  - path: `02-output/ba/`
  - owner: BA
- `process-bpmn`
  - output: `<req>-process-bpmn.md`
  - path: `02-output/ba/`
  - owner: BA
- `frs`
  - output: `<req>-frs.md`
  - path: `02-output/ba/`
  - owner: BA
- `user-story`
  - output: `<req>-user-story.md`
  - path: `02-output/ba/`
  - owner: BA
- `acceptance-criteria`
  - output: `<req>-acceptance-criteria.md`
  - path: `02-output/ba/`
  - owner: BA
- `feature-list`
  - output: `<req>-feature-list.md`
  - path: `02-output/ba/`
  - owner: BA

## BE Artifacts

- `be-spec`
  - output: `<req>-be-spec.md`
  - path: `02-output/be/`
  - owner: BE
- `api-contract`
  - output: `<req>-api-contract.md`
  - path: `02-output/be/`
  - owner: BE

## Architecture Artifacts

- `architecture-note`
  - output: `<req>-architecture-note.md`
  - path: `02-output/architecture/`
  - owner: Architect
- `nfr-review`
  - output: `<req>-nfr-review.md`
  - path: `02-output/architecture/`
  - owner: Architect
- `security-review`
  - output: `<req>-security-review.md`
  - path: `02-output/architecture/`
  - owner: Architect

## Data Artifacts

- `data-model`
  - output: `<req>-data-model.md`
  - path: `02-output/data/`
  - owner: Data
- `state-transition`
  - output: `<req>-state-transition.md`
  - path: `02-output/data/`
  - owner: Data
- `schema-plan`
  - output: `<req>-schema-plan.md`
  - path: `02-output/data/`
  - owner: Data
- `metric-tracking-plan`
  - output: `<req>-metric-tracking-plan.md`
  - path: `02-output/data/`
  - owner: Data

## BE Implementation Artifacts

- `be-implementation-plan`
  - output: `<req>-be-implementation-plan.md`
  - path: `02-output/be/`
  - owner: BE

## FE Implementation Artifacts

- `fe-implementation-plan`
  - output: `<req>-fe-implementation-plan.md`
  - path: `02-output/fe/`
  - owner: FE

## QA Artifacts

- `test-scenarios`
  - output: `<req>-test-scenarios.md`
  - path: `02-output/qa/`
  - owner: QA
- `test-cases`
  - output: `<req>-test-cases.md`
  - path: `02-output/qa/`
  - owner: QA
- `smoke-test-plan`
  - output: `<req>-smoke-test-plan.md`
  - path: `02-output/qa/`
  - owner: QA
- `qa-release-readiness`
  - output: `<req>-release-readiness.md`
  - path: `02-output/qa/`
  - owner: QA

## Design Artifact

- `wireframe`
  - output: `<req>-wireframe.md`
  - path: `02-output/design/`
  - owner: UIUX

## FE Artifact

- `ui`
  - output: `<req>-ui.html`
  - path: `02-output/fe/`
  - owner: FE

## Release Artifacts

- `run-instructions`
  - output: `<req>-run-instructions.md`
  - path: `02-output/release/`
  - owner: Release
- `runnable-system-verification`
  - output: `<req>-runnable-system-verification.md`
  - path: `02-output/release/`
  - owner: Release
- `release-readiness`
  - output: `<req>-release-readiness.md`
  - path: `02-output/release/`
  - owner: Release

## Change Request Artifacts

- `change-request`
  - output: `<cr-id>.md`
  - path: `01-input/change-requests/`
  - owner: PO / BA
- `impact-analysis`
  - output: `<cr-id>-impact-analysis.md`
  - path: `02-output/change-analysis/`
  - owner: PO / BA with downstream agents
- `regeneration-plan`
  - output: `<cr-id>-regeneration-plan.md`
  - path: `02-output/change-analysis/`
  - owner: BA / Release
- `rollback-plan`
  - output: `<cr-id>-rollback-plan.md`
  - path: `02-output/change-analysis/`
  - owner: Release / QA
- `change-verification`
  - output: `<cr-id>-verification.md`
  - path: `02-output/change-analysis/`
  - owner: QA / Release
- `change-log`
  - output: `change-log.md`
  - path: `02-output/change-analysis/`
  - owner: PO / BA / Release
- `baseline-manifest`
  - output: `baseline-manifest.md`
  - path: `05-baselines/before-<cr-id>/`
  - owner: Release
