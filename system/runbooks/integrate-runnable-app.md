---
file_type: "Runbook"
primary_agents: ["Release"]
supporting_agents: ["BE", "FE", "QA"]
activation_mode: "Triggered By Workflow"
lifecycle_stage: "System Core"
purpose: "Align backend, frontend, database, and smoke checks before runnable-system verification."
reads: ["02-output/app/backend/", "02-output/app/frontend/", "02-output/be/", "02-output/fe/", "02-output/qa/"]
produces: ["02-output/qa/<req>-smoke-test-plan.md", "02-output/release/<req>-run-instructions.md"]
---
# Integrate Runnable App

Use this runbook after BE and FE implementations exist.

## Required Skills

- `smoke-test-writer`
- `release-runbook-writer`

## Steps

1. Read backend README, frontend README, API contract, FE implementation plan, and QA outputs.
2. Confirm FE API calls match backend routes.
3. Confirm database setup or seed behavior is documented.
4. Invoke `smoke-test-writer` and create or update `02-output/qa/<req>-smoke-test-plan.md`.
5. Invoke `release-runbook-writer` and write `02-output/release/<req>-run-instructions.md`.

## Validation

- backend run command exists
- frontend run or build command exists
- database setup/reset command exists
- smoke check exists
- commands are exact enough to execute
