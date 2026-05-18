---
file_type: "Rule"
primary_agents: ["PO", "BA", "Architect", "Data", "BE", "UIUX", "FE", "QA", "Release"]
supporting_agents: []
activation_mode: "Always-On Shared"
lifecycle_stage: "System Core"
purpose: "Define how final outputs should look, read, and stay consistent."
---
# Define Output Standards

## Core Final Artifacts

Write final versions directly into:

### PO
- `02-output/po/<req>-brd.md`

### BA
- `02-output/ba/<req>-clarification.md`
- `02-output/ba/<req>-process-bpmn.md`
- `02-output/ba/<req>-user-story.md`
- `02-output/ba/<req>-acceptance-criteria.md`
- `02-output/ba/<req>-frs.md`
- `02-output/ba/<req>-feature-list.md`

### BE
- `02-output/be/<req>-be-spec.md`
- `02-output/be/<req>-api-contract.md`

### Architecture
- `02-output/architecture/<req>-architecture-note.md`
- `02-output/architecture/<req>-nfr-review.md`
- `02-output/architecture/<req>-security-review.md`

### Data
- `02-output/data/<req>-data-model.md`
- `02-output/data/<req>-state-transition.md`
- `02-output/data/<req>-schema-plan.md`
- `02-output/data/<req>-metric-tracking-plan.md`

### BE
- `02-output/be/<req>-be-implementation-plan.md`

### FE
- `02-output/fe/<req>-fe-implementation-plan.md`

### QA
- `02-output/qa/<req>-test-scenarios.md`
- `02-output/qa/<req>-test-cases.md`
- `02-output/qa/<req>-smoke-test-plan.md`
- `02-output/qa/<req>-release-readiness.md`

### Design
- `02-output/design/<req>-wireframe.md`

### FE
- `02-output/fe/<req>-ui.html`

### Release
- `02-output/release/<req>-run-instructions.md`
- `02-output/release/<req>-runnable-system-verification.md`
- `02-output/release/<req>-release-readiness.md`

### Runnable Code
- `02-output/app/backend/`
- `02-output/app/frontend/`
