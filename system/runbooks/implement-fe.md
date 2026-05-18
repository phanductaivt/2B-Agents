---
file_type: "Runbook"
primary_agents: ["FE"]
supporting_agents: ["UIUX", "BE", "Data", "QA", "Release"]
activation_mode: "Triggered By Workflow"
lifecycle_stage: "System Core"
purpose: "Implement a local runnable Vite React TypeScript frontend from BA, Data, BE, UIUX, and FE planning outputs."
reads: ["02-output/ba/", "02-output/data/", "02-output/be/", "02-output/design/", "02-output/architecture/", "02-output/app/backend/", "03-context/", "system/skills/", "system/templates/"]
produces: ["02-output/fe/<req>-fe-implementation-plan.md", "02-output/app/frontend/"]
---
# Implement FE

Use this runbook after API contract and wireframe are ready.

## Required Skills

- `fe-app-implementer`
- `react-api-integration-planner`

## Optional Skills

- `fe-state-modeler`
- `fe-validation-mapper`

## Steps

1. Read BA package, Data metric tracking plan when relevant, BE API contract, BE implementation plan, wireframe, and architecture note.
2. Invoke `react-api-integration-planner` to map user actions to API endpoints and response branches.
3. Invoke `fe-state-modeler` when UI states are non-trivial.
4. Invoke `fe-validation-mapper` when user input validation matters.
5. Write `02-output/fe/<req>-fe-implementation-plan.md`.
6. Invoke `fe-app-implementer` and create frontend code under `02-output/app/frontend/`.
7. Update frontend README with exact install, run, and build commands.

## Validation

- FE calls endpoints that exist in the API contract
- loading, success, validation, and business error states are visible where relevant
- frontend build command is documented
- FE does not invent API fields or business logic
- tracking implementation notes match the metric tracking plan or are explicitly out of scope
