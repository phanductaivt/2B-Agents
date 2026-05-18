---
file_type: "Project Template Guide"
primary_agents: ["PO", "BA", "Architect", "Data", "BE", "UIUX", "FE", "QA", "Release"]
supporting_agents: []
activation_mode: "Manual Navigation"
lifecycle_stage: "Project Template"
purpose: "Explain how the runnable reference project template is structured and how to use it for new projects."
---
# Project Template

Use this folder as a runnable reference template for a new AI Operating Repository project.

This is intentionally not a blank academic template. It contains a complete ticket-date-change example so you can see the expected input, project context, agent outputs, runnable app, QA checks, and release verification in one place.

## Structure

- `README.md`
- `01-input/`
- `02-output/`
- `03-context/`
- `02-output/app/`
- `05-baselines/` for CR rollback snapshots when Git is not used

## How To Use It

1. Copy this folder for a new project
2. Replace the example requirement in `01-input/`
3. Replace or trim project context in `03-context/`
4. Clear or regenerate `02-output/` when creating a new project from scratch
4. Start with `generate-brd.md` to create the PO BRD
5. Use `generate-ba-package.md` after the BRD is ready
6. Use `generate-architecture.md` and `generate-data-design.md` before implementation
7. Use `generate-be-package.md`, then `implement-be.md`
8. Continue with wireframe, FE UI, and `implement-fe.md`
9. Use `generate-qa-review.md` after BE, design, and FE outputs are ready
10. Use `integrate-runnable-app.md` and `verify-runnable-system.md`
11. Write final artifacts, runnable code, and checks under `02-output/`

## Output Areas

- `02-output/po/` for PO BRD
- `02-output/ba/` for BA package
- `02-output/architecture/` for architecture, NFR, and security review
- `02-output/data/` for data model, state transition, schema planning, and metric tracking plan
- `02-output/be/` for BE package and BE implementation plan
- `02-output/design/` for wireframe
- `02-output/fe/` for UI and FE implementation plan
- `02-output/qa/` for QA package and smoke test plan
- `02-output/release/` for run instructions and runnable verification

## Runnable Code Areas

- `02-output/app/backend/` for FastAPI backend code
- `02-output/app/frontend/` for Vite React TypeScript frontend code

## Change Request Areas

After this project becomes stable, use `projects/PROJECT_CHANGE_REQUEST_GUIDE.md` for customer change requests or customization requests.

- `01-input/change-requests/` stores CR intake files
- `02-output/change-analysis/` stores CR impact analysis, regeneration plan, rollback plan, verification, and change log
- `05-baselines/` stores pre-apply snapshots for rollback when Git is not used

## Included Reference

The included example is a ticket date-change product slice.

- input: `01-input/`
- context: `03-context/`
- final outputs: `02-output/`
- runnable app: `02-output/app/`
