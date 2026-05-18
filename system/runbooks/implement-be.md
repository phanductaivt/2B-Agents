---
file_type: "Runbook"
primary_agents: ["BE"]
supporting_agents: ["Architect", "Data", "QA", "Release"]
activation_mode: "Triggered By Workflow"
lifecycle_stage: "System Core"
purpose: "Implement a local runnable FastAPI backend from approved product, analysis, architecture, data, and BE outputs."
reads: ["02-output/po/", "02-output/ba/", "02-output/architecture/", "02-output/data/", "02-output/be/", "03-context/", "system/skills/", "system/templates/"]
produces: ["02-output/be/<req>-be-implementation-plan.md", "02-output/app/backend/", "02-output/app/backend/tests/"]
---
# Implement BE

Use this runbook after BE spec, API contract, architecture, and data design are ready.

## Required Skills

- `be-implementation-planner`
- `fastapi-implementer`

## Steps

1. Read BE spec, API contract, architecture note, data model, schema plan, state transition, and metric tracking plan when backend events are in scope.
2. Invoke `be-implementation-planner` and write `02-output/be/<req>-be-implementation-plan.md`.
3. Invoke `fastapi-implementer` and create backend code under `02-output/app/backend/`.
4. Include a minimal SQLite setup and seed path.
5. Include pytest tests for core API behavior.
6. Update backend README with exact setup, run, and test commands.

## Validation

- API routes match the API contract
- validation and error behavior match BA/BE artifacts
- SQLite persistence supports the approved slice
- backend tests cover at least one happy path and one material negative path
- server-side tracking notes from the BE spec/API contract are implemented or explicitly deferred

## Recovery

If implementation exposes a missing rule, stop and use `resolve-clarification.md` instead of coding around the gap.
