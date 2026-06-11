---
file_type: "Context Routing Registry"
primary_agents: ["PO", "BA", "Architect", "Data", "BE", "UIUX", "FE", "QA", "Release"]
supporting_agents: []
activation_mode: "Routing Reference"
lifecycle_stage: "System Core"
purpose: "Route each phase to the smallest required context set before execution."
---
# Context Routing

## Purpose Of Context Routing

Context routing keeps each execution phase focused on the files required for the current decision or output. It prevents the AI from loading the whole repository when one active runbook, one active agent, a small set of skills, and a small set of upstream artifacts are enough.

## No Bulk-Loading Principle

Do not bulk-read entire system directories. Follow the AI Executor Contract,
select the workflow and active phase, then load only the context declared by
the one active runbook, this registry, or a directly referenced knowledge
index.

Avoid bulk-loading:
- `system/agents/`
- `system/skills/`
- `system/templates/`
- `system/rules/`
- `system/guardrails/`
- `system/agent-knowledge/<role>/`
- all previous `02-output/` folders

## Phase Routing Algorithm

1. Follow `system/executors/executor-contract.md`.
2. Identify the user goal, task ID, and project path.
3. Select one active workflow from `system/registries/workflows-index.md` when
   the task matches a registered multi-phase workflow.
4. Load only the selected workflow contract and identify its active phase.
5. Select the one active runbook from the workflow phase or routing table.
6. Load the active runbook.
7. Select the active Agent from the workflow phase.
8. Load required rules and guardrails listed for the phase.
9. Load required skills listed for the phase.
10. Load only the templates needed for expected outputs in the phase.
11. Read required project inputs and required handoff outputs from previous phases.
12. Read `system/agent-knowledge/<role>/INDEX.md` only when reusable role knowledge is needed.
13. From the knowledge index, load only need-specific files listed under "Load When Needed".
14. If required context is missing, stop and report the missing file or folder before generating downstream output.

## How To Select Active Workflow

Use `system/registries/workflows-index.md` for registered multi-phase tasks.
Load only the selected workflow contract. For a standalone operation that does
not match a registered workflow, record `Active Workflow: None` and select the
specific runbook directly.

## How To Select Active Runbook

Use the runbook declared by the active workflow phase. For a standalone
operation, use the most specific runbook for the request. Use
`generate-product-slice.md` only as a coordinator, then route into the
phase-specific runbook. Use `handle-change-request.md` for approved project
change request flow. Use `regenerate-output.md` only for targeted regeneration
after identifying the impacted artifact.

## How To Select Active Agent

The active workflow phase's `Active Agent` value is authoritative and
overrides runbook `primary_agents`. Load only that Agent definition from
`system/agents/<role>/AGENT.md`.

Orchestration runbooks may list multiple `primary_agents` to show eligible
roles across the workflow; this does not activate them together. If the active
workflow phase declares `Active Agent: None`, do not infer an Agent from the
runbook.

For a standalone operation with no registered workflow, use a single
unambiguous runbook `primary_agents` owner. If the runbook lists multiple
possible owners, stop and resolve ownership through the output contract or user
direction before activating an Agent.

## How To Select Required Skills

Load required skill files named in the active runbook. Load optional skills only when their trigger condition is true. If a skill is not mapped to the current phase, do not load it unless the active runbook explicitly routes to it.

## How To Select Templates

Load only templates that correspond to expected output files in the active phase. Checklists are optional review aids and should be loaded only when the active runbook or quality gate calls for them.

## How To Read Agent Knowledge

For reusable role knowledge, read only `system/agent-knowledge/<role>/INDEX.md` first. Then load only the specific files named in the index that match the current need, such as validation, handoff, security, runnable verification, or tracking.

Do not read all files under `system/agent-knowledge/<role>/`.

## How To Read Handoff Outputs From Previous Phases

Read the smallest upstream set that lets the current phase work safely. Prefer exact requirement-scoped files such as `02-output/ba/<req>-frs.md` over whole folders such as `02-output/ba/`.

If several previous outputs exist, choose files with the current requirement ID. If no matching file exists, stop and report the missing handoff instead of using unrelated output.

## How To Avoid Stale Or Unrelated Outputs

- Match the requirement ID before reading previous outputs.
- Prefer current project files over template or sample project files.
- Do not use outputs from another project folder.
- Treat older or unmatched artifacts as unrelated unless the user explicitly routes to them.
- If multiple candidate outputs conflict, stop and report the conflict.
- Do not infer approval from generated files; use the clarification approval status.

## Phase Routing Table

| Phase | Runbook | Active Agent | Required Skills | Required Templates | Required Rules | Required Guardrails | Required Inputs | Required Handoff Outputs | Expected Outputs |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Product slice coordination | `system/runbooks/generate-product-slice.md` | Active phase agent only | Load skills from active phase runbook only | Load templates from active phase runbook only | `system/rules/read-rules-start-here.md` | `system/guardrails/define-context-loading.md`, `system/guardrails/define-execution-protocol.md`, `system/guardrails/define-clarification-rules.md` | `01-input/requirements/<req>.md`, relevant `03-context/` files | Exact upstream files declared by active phase runbook | Delegates to exact outputs in `system/registries/output-contracts.md` |
| PO product intent | `system/runbooks/generate-brd.md` | PO | `system/skills/brd-drafter/SKILL.md`, `system/skills/baccm-product-framer/SKILL.md`, `system/skills/requirement-classifier/SKILL.md`; conditional `system/skills/requirement-clarifier/SKILL.md`, `system/skills/market-research-synthesizer/SKILL.md`, `system/skills/prioritization-helper/SKILL.md` | `system/templates/requirements/template-brd.md`, optional `system/templates/checklists/checklist-brd.md` | `system/rules/read-rules-start-here.md`, `system/rules/define-output-standards.md`, `system/rules/define-project-conventions.md` | `system/guardrails/define-context-loading.md`, `system/guardrails/define-clarification-rules.md`, `system/guardrails/verify-output-quality.md` | `01-input/requirements/<req>.md`, relevant `03-context/` files | None | `02-output/po/<req>-brd.md` |
| BA package | `system/runbooks/generate-ba-package.md` | BA | `system/skills/requirement-clarifier/SKILL.md`, `system/skills/ambiguity-checker-plus/SKILL.md`, `system/skills/frs-drafter/SKILL.md`, `system/skills/user-story-writer/SKILL.md`, `system/skills/acceptance-criteria-writer/SKILL.md`, `system/skills/bpmn-mermaid-writer/SKILL.md`, `system/skills/feature-breakdown-writer/SKILL.md`; conditional `system/skills/process-analyzer/SKILL.md`, `system/skills/scope-boundary-checker/SKILL.md`, `system/skills/rule-coverage-checker/SKILL.md`, `system/skills/exception-scenario-expander/SKILL.md` | `system/templates/requirements/template-frs.md`, `system/templates/requirements/template-user-story.md`, `system/templates/requirements/template-acceptance-criteria.md`, optional checklists declared by runbook | `system/rules/read-rules-start-here.md`, `system/rules/define-output-standards.md` | `system/guardrails/define-context-loading.md`, `system/guardrails/define-clarification-rules.md`, `system/guardrails/verify-output-quality.md` | `01-input/requirements/<req>.md`, relevant `03-context/` files | `02-output/po/<req>-brd.md` | `02-output/ba/<req>-clarification.md`, `02-output/ba/<req>-process-bpmn.md`, `02-output/ba/<req>-user-story.md`, `02-output/ba/<req>-acceptance-criteria.md`, `02-output/ba/<req>-frs.md`, `02-output/ba/<req>-feature-list.md` |
| Architecture | `system/runbooks/generate-architecture.md` | Architect | `system/skills/architecture-designer/SKILL.md`, `system/skills/nfr-reviewer/SKILL.md`, `system/skills/security-reviewer/SKILL.md` | `system/templates/architecture/template-architecture-note.md`, `system/templates/architecture/template-nfr-review.md`, `system/templates/architecture/template-security-review.md` | `system/rules/read-rules-start-here.md`, `system/rules/define-output-standards.md` | `system/guardrails/define-context-loading.md`, `system/guardrails/verify-output-quality.md` | relevant `03-context/` files | `02-output/po/<req>-brd.md`, `02-output/ba/<req>-frs.md`, `02-output/ba/<req>-feature-list.md`, `02-output/ba/<req>-acceptance-criteria.md`, optional `02-output/design/<req>-wireframe.md` | `02-output/architecture/<req>-architecture-note.md`, `02-output/architecture/<req>-nfr-review.md`, `02-output/architecture/<req>-security-review.md` |
| Data design | `system/runbooks/generate-data-design.md` | Data | `system/skills/data-model-designer/SKILL.md`, `system/skills/sqlite-schema-planner/SKILL.md`, `system/skills/metric-framework-selector/SKILL.md`, `system/skills/feature-metrics-planner/SKILL.md`, `system/skills/tracking-event-planner/SKILL.md`, `system/skills/metric-logic-checker/SKILL.md` | `system/templates/data/template-data-model.md`, `system/templates/data/template-state-transition.md`, `system/templates/data/template-schema-plan.md`, `system/templates/data/template-metric-tracking-plan.md` | `system/rules/read-rules-start-here.md`, `system/rules/define-output-standards.md` | `system/guardrails/define-context-loading.md`, `system/guardrails/verify-output-quality.md` | relevant `03-context/` files | `02-output/po/<req>-brd.md`, `02-output/ba/<req>-frs.md`, `02-output/ba/<req>-feature-list.md`, `02-output/architecture/<req>-architecture-note.md`, `02-output/architecture/<req>-nfr-review.md`, `02-output/architecture/<req>-security-review.md`, optional exact routed UI/API/QA feedback files | `02-output/data/<req>-data-model.md`, `02-output/data/<req>-state-transition.md`, `02-output/data/<req>-schema-plan.md`, `02-output/data/<req>-metric-tracking-plan.md` |
| BE package | `system/runbooks/generate-be-package.md` | BE | `system/skills/be-solution-designer/SKILL.md`, `system/skills/api-contract-writer/SKILL.md`, conditional `system/skills/rule-coverage-checker/SKILL.md` | `system/templates/technical-design/template-be-spec.md`, `system/templates/technical-design/template-api-contract.md` | `system/rules/read-rules-start-here.md`, `system/rules/define-output-standards.md` | `system/guardrails/define-context-loading.md`, `system/guardrails/verify-output-quality.md` | relevant `03-context/` files | `02-output/po/<req>-brd.md`, `02-output/ba/<req>-frs.md`, `02-output/ba/<req>-feature-list.md`, optional `02-output/ba/<req>-process-bpmn.md`, `02-output/architecture/<req>-architecture-note.md`, `02-output/data/<req>-data-model.md`, `02-output/data/<req>-state-transition.md`, `02-output/data/<req>-schema-plan.md`, `02-output/data/<req>-metric-tracking-plan.md` | `02-output/be/<req>-be-spec.md`, `02-output/be/<req>-api-contract.md` |
| BE implementation | `system/runbooks/implement-be.md` | BE | `system/skills/be-implementation-planner/SKILL.md`, `system/skills/fastapi-implementer/SKILL.md` | `system/templates/implementation/template-be-implementation-plan.md` | `system/rules/read-rules-start-here.md`, `system/rules/define-project-conventions.md` | `system/guardrails/define-context-loading.md`, `system/guardrails/define-artifact-contracts.md` | relevant `03-context/` files | `02-output/be/<req>-be-spec.md`, `02-output/be/<req>-api-contract.md`, `02-output/architecture/<req>-architecture-note.md`, `02-output/data/<req>-data-model.md`, `02-output/data/<req>-schema-plan.md`, `02-output/data/<req>-state-transition.md` | `02-output/be/<req>-be-implementation-plan.md`, `02-output/app/backend/`, `02-output/app/backend/tests/` |
| Wireframe | `system/runbooks/generate-wireframe.md` | UIUX | `system/skills/wireframe-writer/SKILL.md`, conditional `system/skills/process-analyzer/SKILL.md` | `system/templates/design/template-wireframe.md`, optional `system/templates/checklists/checklist-wireframe.md` | `system/rules/read-rules-start-here.md`, `system/rules/define-output-standards.md` | `system/guardrails/define-context-loading.md`, `system/guardrails/verify-output-quality.md` | relevant `03-context/` files | `02-output/po/<req>-brd.md`, `02-output/ba/<req>-frs.md`, `02-output/ba/<req>-feature-list.md`, `02-output/ba/<req>-user-story.md`, `02-output/ba/<req>-acceptance-criteria.md`, optional `02-output/ba/<req>-process-bpmn.md` | `02-output/design/<req>-wireframe.md` |
| FE review UI | `system/runbooks/generate-fe-ui.md` | FE | `system/skills/html-implementer/SKILL.md`, conditional `system/skills/fe-state-modeler/SKILL.md`, `system/skills/fe-validation-mapper/SKILL.md`, `system/skills/fe-api-consumption-planner/SKILL.md` | `system/templates/technical-design/template-fe-technical-design.md` when needed, optional `system/templates/checklists/checklist-ui.md` | `system/rules/read-rules-start-here.md`, `system/rules/define-output-standards.md` | `system/guardrails/define-context-loading.md`, `system/guardrails/verify-output-quality.md` | relevant `03-context/` files | `02-output/po/<req>-brd.md`, `02-output/ba/<req>-frs.md`, `02-output/ba/<req>-feature-list.md`, `02-output/ba/<req>-user-story.md`, `02-output/ba/<req>-acceptance-criteria.md`, `02-output/be/<req>-api-contract.md`, `02-output/be/<req>-be-spec.md`, optional `02-output/data/<req>-metric-tracking-plan.md`, `02-output/design/<req>-wireframe.md`, optional `02-output/architecture/<req>-architecture-note.md` | `02-output/fe/<req>-ui.html` |
| FE implementation | `system/runbooks/implement-fe.md` | FE | `system/skills/fe-app-implementer/SKILL.md`, `system/skills/react-api-integration-planner/SKILL.md`, conditional `system/skills/fe-state-modeler/SKILL.md`, `system/skills/fe-validation-mapper/SKILL.md` | `system/templates/implementation/template-fe-implementation-plan.md` | `system/rules/read-rules-start-here.md`, `system/rules/define-project-conventions.md` | `system/guardrails/define-context-loading.md`, `system/guardrails/define-artifact-contracts.md` | relevant `03-context/` files | `02-output/ba/<req>-frs.md`, `02-output/ba/<req>-feature-list.md`, `02-output/ba/<req>-acceptance-criteria.md`, optional `02-output/data/<req>-metric-tracking-plan.md`, `02-output/be/<req>-api-contract.md`, `02-output/be/<req>-be-implementation-plan.md`, `02-output/design/<req>-wireframe.md`, `02-output/architecture/<req>-architecture-note.md` | `02-output/fe/<req>-fe-implementation-plan.md`, `02-output/app/frontend/` |
| QA review | `system/runbooks/generate-qa-review.md` | QA | `system/skills/test-scenario-designer/SKILL.md`, `system/skills/test-case-writer/SKILL.md`, `system/skills/smoke-test-writer/SKILL.md`, `system/skills/release-readiness-reviewer/SKILL.md`, conditional `system/skills/exception-scenario-expander/SKILL.md`, `system/skills/rule-coverage-checker/SKILL.md` | `system/templates/quality/template-test-scenarios.md`, `system/templates/quality/template-test-cases.md`, `system/templates/quality/template-release-readiness.md`, optional exact QA checklists declared by runbook | `system/rules/read-rules-start-here.md`, `system/rules/define-output-standards.md` | `system/guardrails/define-context-loading.md`, `system/guardrails/verify-output-quality.md` | relevant `03-context/` files | `02-output/po/<req>-brd.md`, `02-output/ba/<req>-frs.md`, `02-output/ba/<req>-feature-list.md`, `02-output/ba/<req>-acceptance-criteria.md`, optional `02-output/data/<req>-metric-tracking-plan.md`, `02-output/be/<req>-api-contract.md`, `02-output/be/<req>-be-spec.md`, optional `02-output/design/<req>-wireframe.md`, optional `02-output/fe/<req>-ui.html`, optional `02-output/fe/<req>-fe-implementation-plan.md` | `02-output/qa/<req>-quality-review-package.md`, `02-output/qa/<req>-test-strategy.md`, `02-output/qa/<req>-test-scenarios.md`, `02-output/qa/<req>-test-cases.md`, `02-output/qa/<req>-smoke-test-plan.md`, `02-output/qa/<req>-release-readiness.md` as QA quality readiness |
| Runnable integration | `system/runbooks/integrate-runnable-app.md` | Release | `system/skills/release-runbook-writer/SKILL.md` | `system/templates/release/template-release-runbook.md` | `system/rules/read-rules-start-here.md`, `system/rules/define-project-conventions.md` | `system/guardrails/define-context-loading.md`, `system/guardrails/define-artifact-contracts.md` | `02-output/app/backend/README.md`, `02-output/app/frontend/README.md` | `02-output/be/<req>-api-contract.md`, `02-output/fe/<req>-fe-implementation-plan.md`, `02-output/qa/<req>-smoke-test-plan.md` | `02-output/release/<req>-run-instructions.md` |
| Runnable verification | `system/runbooks/verify-runnable-system.md` | Release | `system/skills/runnable-system-verifier/SKILL.md` | `system/templates/release/template-runnable-system-verification.md` | `system/rules/read-rules-start-here.md`, `system/rules/define-output-standards.md` | `system/guardrails/define-context-loading.md`, `system/guardrails/define-artifact-contracts.md`, `system/guardrails/verify-output-quality.md` | `02-output/app/backend/README.md`, `02-output/app/frontend/README.md`, backend/frontend app files only as needed to execute declared commands | `02-output/qa/<req>-smoke-test-plan.md`, `02-output/release/<req>-run-instructions.md`, optional `02-output/qa/<req>-release-readiness.md` | `02-output/release/<req>-runnable-system-verification.md`, `02-output/release/<req>-release-readiness.md` as runnable/system readiness |
| Clarification resolution | `system/runbooks/resolve-clarification.md` | Owning phase agent | As needed: `requirement-clarifier`, `ambiguity-checker-plus`, `rule-coverage-checker` | Target artifact template if updated | `system/rules/read-rules-start-here.md` | `system/guardrails/define-context-loading.md`, `system/guardrails/define-clarification-rules.md` | requirement or affected upstream artifact | affected handoff output | clarified source artifact or clarified output section |
| Targeted regeneration | `system/runbooks/regenerate-output.md` | Owning phase agent | Skill binding of target artifact | Template of target artifact | `system/rules/read-rules-start-here.md` | `system/guardrails/define-context-loading.md`, `system/guardrails/verify-output-quality.md` | changed source, existing target output | required upstream outputs for target artifact | updated artifact, app code, or test file |
| Change request | `system/runbooks/handle-change-request.md` | Owning agent per affected artifact | Load only the artifact-specific skill paths after CR approval | `system/templates/change-control/template-change-request.md`, `system/templates/change-control/template-impact-analysis.md`, `system/templates/change-control/template-regeneration-plan.md`, `system/templates/change-control/template-rollback-plan.md`, `system/templates/change-control/template-change-verification.md`, `system/templates/change-control/template-change-log.md`; select the exact template for the current CR step | `system/rules/read-rules-start-here.md`, `system/rules/define-project-conventions.md` | `system/guardrails/define-context-loading.md`, `system/guardrails/define-artifact-contracts.md` | linked requirement, CR file, relevant context | exact affected generated artifacts or app files named in impact analysis/regeneration plan | `01-input/change-requests/<cr-id>.md`, `02-output/change-analysis/<cr-id>-impact-analysis.md`, `02-output/change-analysis/<cr-id>-regeneration-plan.md`, `02-output/change-analysis/<cr-id>-rollback-plan.md`, `02-output/change-analysis/<cr-id>-verification.md`, `02-output/change-analysis/change-log.md` |
