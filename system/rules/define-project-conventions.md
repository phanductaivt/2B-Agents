---
file_type: "Rule"
primary_agents: ["PO", "BA", "Architect", "Data", "BE", "UIUX", "FE", "QA", "Release"]
supporting_agents: []
activation_mode: "Always-On Shared"
lifecycle_stage: "System Core"
purpose: "Define project folder conventions, naming standards, and repository usage patterns."
---
# Define Project Conventions

## Standard Project Structure

- `README.md`
- `01-input/`
- `01-input/requirements/`
- `01-input/notes/meeting-notes/`
- `01-input/assets/raw/`
- `01-input/change-requests/`
- `02-output/`
- `02-output/po/`
- `02-output/ba/`
- `02-output/architecture/`
- `02-output/data/`
- `02-output/be/`
- `02-output/design/`
- `02-output/fe/`
- `02-output/qa/`
- `02-output/release/`
- `02-output/change-analysis/`
- `02-output/app/backend/`
- `02-output/app/backend/app/`
- `02-output/app/backend/tests/`
- `02-output/app/frontend/`
- `02-output/app/frontend/src/`
- `03-context/`
- `05-baselines/`

`05-baselines/` is required only when approved change requests are applied without Git as the rollback layer.

## File Naming

- requirements: `req-001.md`
- change requests: `cr-001.md`
- PO outputs: `req-001-brd.md`
- BA outputs: `req-001-clarification.md`, `req-001-process-bpmn.md`, `req-001-user-story.md`, `req-001-acceptance-criteria.md`, `req-001-frs.md`, `req-001-feature-list.md`
- architecture outputs: `req-001-architecture-note.md`, `req-001-nfr-review.md`, `req-001-security-review.md`
- data outputs: `req-001-data-model.md`, `req-001-state-transition.md`, `req-001-schema-plan.md`, `req-001-metric-tracking-plan.md`
- BE outputs: `req-001-be-spec.md`, `req-001-api-contract.md`, `req-001-be-implementation-plan.md`
- design outputs: `req-001-wireframe.md`
- FE outputs: `req-001-ui.html`, `req-001-fe-implementation-plan.md`
- QA outputs: `req-001-test-scenarios.md`, `req-001-test-cases.md`, `req-001-smoke-test-plan.md`, `req-001-release-readiness.md`
- release outputs: `req-001-run-instructions.md`, `req-001-runnable-system-verification.md`, `req-001-release-readiness.md`
- change analysis outputs: `cr-001-impact-analysis.md`, `cr-001-regeneration-plan.md`, `cr-001-rollback-plan.md`, `cr-001-verification.md`, `change-log.md`

## Source Of Truth Rules

- official requirement input belongs in `01-input/requirements/`
- reusable project facts, policies, glossary, and market notes belong in `03-context/`
- generated delivery artifacts belong in `02-output/`
- runnable backend and frontend code belongs under `02-output/app/`
- post-baseline customer changes must use `01-input/change-requests/` and `02-output/change-analysis/`
- do not merge a change request into the linked requirement until it is applied and verified

## System File Naming

- runbooks, rules, and guardrails should use a clear `action-object` naming style in filenames
- templates should use `template-<object>.md`
- checklists should use `checklist-<object>.md`
