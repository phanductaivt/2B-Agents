---
file_type: "Runbook"
primary_agents: ["PO", "BA", "Architect", "Data", "BE", "UIUX", "FE", "QA", "Release"]
supporting_agents: []
activation_mode: "Triggered By Workflow"
lifecycle_stage: "System Core"
purpose: "Regenerate an existing artifact or runnable app output after upstream changes or review feedback."
reads: ["existing output", "upstream artifacts", "03-context/", "system/rules/", "system/guardrails/", "02-output/app/", "02-output/qa/"]
produces: ["updated artifact, app code, or test file"]
---
# Regenerate Output

Use this runbook when an input or context file changes.

For post-baseline customer change requests or customization requests, use `handle-change-request.md` first. Do not use this runbook to bypass CR intake, impact analysis, approval, baseline snapshot, verification, or requirement merge control.

## Skill Routing

- regenerate BRD with `brd-drafter`, `baccm-product-framer`, and `requirement-classifier`
- regenerate BA outputs with the BA package skills bound in `generate-ba-package.md`
- regenerate architecture outputs with `architecture-designer`, `nfr-reviewer`, and `security-reviewer`
- regenerate data outputs with `data-model-designer`, `sqlite-schema-planner`, `metric-framework-selector`, `feature-metrics-planner`, `tracking-event-planner`, and `metric-logic-checker`
- regenerate BE outputs with `be-solution-designer` and `api-contract-writer`
- regenerate BE implementation with `be-implementation-planner` and `fastapi-implementer`
- regenerate wireframe with `wireframe-writer`
- regenerate FE UI with `html-implementer`
- regenerate FE implementation with `fe-app-implementer` and `react-api-integration-planner`
- regenerate QA outputs with `test-scenario-designer`, `test-case-writer`, and `release-readiness-reviewer`
- regenerate release outputs with `smoke-test-writer`, `runnable-system-verifier`, and `release-runbook-writer`

## Steps

1. Identify the changed requirement or context source
2. Regenerate only the impacted artifact, app code, or test file
3. Keep filenames stable so review remains simple
4. Re-run verification when regenerated code affects local runnable behavior
