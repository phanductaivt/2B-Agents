---
file_type: "Agent Matrix"
primary_agents: ["PO", "BA", "Architect", "Data", "BE", "UIUX", "FE", "QA", "Release"]
supporting_agents: []
activation_mode: "Manual Navigation"
lifecycle_stage: "System Core"
purpose: "Map each active agent to its inputs, outputs, runbooks, skills, templates, and knowledge sources."
---
# Define Agent Usage Matrix

## Agent Usage Matrix

| Agent | Main Responsibility | Reads | Writes | Primary Runbook | Core Skills | Core Templates / Checklists | Agent Knowledge |
| --- | --- | --- | --- | --- | --- | --- | --- |
| PO | product framing and BRD ownership | `01-input/`, `03-context/`, `system/rules/`, `system/guardrails/` | `02-output/po/<req>-brd.md` | `generate-brd.md` | `brd-drafter`, `baccm-product-framer`, `market-research-synthesizer`, `requirement-classifier`, `prioritization-helper` | `template-brd.md`, `checklist-brd.md` | `po/` |
| BA | analysis package ownership | `01-input/`, `03-context/`, `02-output/po/`, `system/rules/`, `system/guardrails/` | `02-output/ba/*.md` | `generate-ba-package.md` | `requirement-clarifier`, `ambiguity-checker-plus`, `frs-drafter`, `user-story-writer`, `acceptance-criteria-writer`, `bpmn-mermaid-writer`, `feature-breakdown-writer`, `scope-boundary-checker`, `rule-coverage-checker`, `exception-scenario-expander` | `template-frs.md`, `template-user-story.md`, `template-acceptance-criteria.md`, `checklist-clarification.md`, `checklist-frs.md`, `checklist-feature-list.md`, `checklist-user-story.md`, `checklist-acceptance-criteria.md` | `ba/` |
| Architect | architecture, NFR, and security readiness | `02-output/po/`, `02-output/ba/`, `03-context/`, `system/rules/`, `system/guardrails/` | `02-output/architecture/*.md` | `generate-architecture.md` | `architecture-designer`, `nfr-reviewer`, `security-reviewer` | `template-architecture-note.md`, `template-nfr-review.md`, `template-security-review.md` | `architect/` |
| Data | data model, state transition, SQLite schema planning, and feature metric tracking | `02-output/po/`, `02-output/ba/`, `02-output/architecture/`, `02-output/design/`, `02-output/be/`, `02-output/fe/`, `02-output/qa/`, `03-context/` | `02-output/data/*.md` | `generate-data-design.md` | `data-model-designer`, `sqlite-schema-planner`, `metric-framework-selector`, `feature-metrics-planner`, `tracking-event-planner`, `metric-logic-checker` | `template-data-model.md`, `template-state-transition.md`, `template-schema-plan.md`, `template-metric-tracking-plan.md` | `data/` |
| BE | backend service behavior, API contract, server-side tracking touchpoints, and FastAPI implementation | `02-output/po/`, `02-output/ba/`, `02-output/architecture/`, `02-output/data/`, `03-context/`, `system/rules/`, `system/guardrails/` | `02-output/be/*.md`, `02-output/app/backend/` | `generate-be-package.md`, `implement-be.md` | `be-solution-designer`, `api-contract-writer`, `be-implementation-planner`, `fastapi-implementer` | `template-be-spec.md`, `template-api-contract.md`, `template-be-implementation-plan.md` | `be/` |
| UIUX | low-detail interaction structure and wireframe | `02-output/po/`, `02-output/ba/`, `03-context/`, `system/rules/`, `system/guardrails/` | `02-output/design/<req>-wireframe.md` | `generate-wireframe.md` | `wireframe-writer` | `template-wireframe.md`, `checklist-wireframe.md` | `uiux/` |
| FE | runnable React frontend, reviewable UI, and UI tracking touchpoints | `02-output/po/`, `02-output/ba/`, `02-output/be/`, `02-output/design/`, `02-output/architecture/`, `02-output/data/`, `03-context/` | `02-output/fe/<req>-ui.html`, `02-output/fe/<req>-fe-implementation-plan.md`, `02-output/app/frontend/` | `generate-fe-ui.md`, `implement-fe.md` | `html-implementer`, `fe-state-modeler`, `fe-validation-mapper`, `fe-api-consumption-planner`, `fe-app-implementer`, `react-api-integration-planner` | `template-fe-technical-design.md`, `template-fe-implementation-plan.md`, `checklist-ui.md` | `fe/` |
| QA | test coverage, tracking verification, test cases, release-readiness review | `02-output/po/`, `02-output/ba/`, `02-output/be/`, `02-output/design/`, `02-output/fe/`, `02-output/data/`, `03-context/` | `02-output/qa/*.md` | `generate-qa-review.md` | `test-scenario-designer`, `test-case-writer`, `release-readiness-reviewer` | `template-test-scenarios.md`, `template-test-cases.md`, `template-release-readiness.md`, `checklist-test-scenarios.md`, `checklist-test-cases.md`, `checklist-release-readiness.md` | `qa/` |
| Release | local runnable verification and run instructions | `02-output/`, `02-output/app/`, `02-output/qa/` | `02-output/release/*.md` | `integrate-runnable-app.md`, `verify-runnable-system.md` | `smoke-test-writer`, `runnable-system-verifier`, `release-runbook-writer` | `template-runnable-system-verification.md`, `template-release-runbook.md` | `release/` |

## Shared System Layers

- `system/rules/` is shared by every active agent.
- `system/guardrails/` is shared by every active agent.
- `system/runbooks/resolve-clarification.md`, `system/runbooks/regenerate-output.md`, and `system/runbooks/handle-change-request.md` are cross-agent runbooks.
- `system/templates/checklists/` is a shared review layer, even when one checklist has a stronger primary agent owner.

## Skill-Binding Summary

| Runbook | Required Skills | Optional Skills |
| --- | --- | --- |
| `generate-brd.md` | `brd-drafter`, `baccm-product-framer`, `requirement-classifier` | `market-research-synthesizer`, `prioritization-helper`, `requirement-clarifier` |
| `generate-ba-package.md` | `requirement-clarifier`, `frs-drafter`, `user-story-writer`, `acceptance-criteria-writer`, `bpmn-mermaid-writer`, `feature-breakdown-writer` | `ambiguity-checker-plus`, `process-analyzer`, `scope-boundary-checker`, `rule-coverage-checker`, `exception-scenario-expander` |
| `generate-architecture.md` | `architecture-designer`, `nfr-reviewer`, `security-reviewer` | none fixed |
| `generate-data-design.md` | `data-model-designer`, `sqlite-schema-planner`, `metric-framework-selector`, `feature-metrics-planner`, `tracking-event-planner`, `metric-logic-checker` | none fixed |
| `generate-be-package.md` | `be-solution-designer`, `api-contract-writer` | `rule-coverage-checker` |
| `implement-be.md` | `be-implementation-planner`, `fastapi-implementer` | none fixed |
| `generate-wireframe.md` | `wireframe-writer` | `process-analyzer` |
| `generate-fe-ui.md` | `html-implementer` | `fe-state-modeler`, `fe-validation-mapper`, `fe-api-consumption-planner` |
| `implement-fe.md` | `fe-app-implementer`, `react-api-integration-planner` | `fe-state-modeler`, `fe-validation-mapper` |
| `generate-qa-review.md` | `test-scenario-designer`, `test-case-writer`, `release-readiness-reviewer` | `exception-scenario-expander`, `rule-coverage-checker` |
| `integrate-runnable-app.md` | `smoke-test-writer`, `release-runbook-writer` | none fixed |
| `verify-runnable-system.md` | `runnable-system-verifier` | none fixed |
| `resolve-clarification.md` | none fixed | `requirement-clarifier`, `ambiguity-checker-plus`, `rule-coverage-checker` |
| `regenerate-output.md` | depends on target artifact | use the skill binding of the artifact-specific runbook |
| `handle-change-request.md` | depends on impacted artifact and app scope | use the skill binding of the artifact-specific runbook after CR approval and baseline |
