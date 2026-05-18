---
file_type: "Project Guide"
primary_agents: ["PO", "BA", "Architect", "Data", "BE", "UIUX", "FE", "QA", "Release"]
supporting_agents: []
activation_mode: "Manual Navigation"
lifecycle_stage: "Project System"
purpose: "Explain the project area, template usage, and active project flow."
---
# Projects

Projects are the main working surface.

## Final Project Structure

- `README.md`
- `01-input/`
- `02-output/`
- `03-context/`
- `02-output/app/`
- `05-baselines/` when change requests are applied without Git rollback

## Daily Flow

1. Copy `project-template/`
2. Put business input into `01-input/`
3. Add project context in `03-context/`
4. Use the copy-ready prompts and terminal commands in `PROJECT_EXECUTION_GUIDE.md`
5. Review the clarification gate in `02-output/ba/<req>-clarification.md`
6. Approve with `Approved - Proceed` or `Approved - Proceed with assumptions`, or block and update input/context
7. Continue with Architect, Data, BE, UIUX, FE, QA, and Release only after approval; Data includes metric tracking plans for PO feature-health decisions
8. Review final artifacts and runnable code in `02-output/`

Codex may recommend a decision, but it must not run downstream agents until user approval is explicit.

## Template

`project-template/` is a runnable reference template.

It already contains one complete ticket date-change example across:
- `01-input/`
- `03-context/`
- `02-output/`
- `02-output/app/`

When creating a new project, copy `project-template/`, then replace the requirement, context, and generated outputs as needed.

## Change Requests

Use `PROJECT_CHANGE_REQUEST_GUIDE.md` when a stable project receives a customer change request or customization request.

Change request files belong in:
- `01-input/change-requests/` for CR intake
- `02-output/change-analysis/` for impact analysis, regeneration plan, rollback plan, verification, and change log
- `05-baselines/` for pre-apply snapshots when Git is not used

Do not put post-baseline CR steps into `PROJECT_EXECUTION_GUIDE.md`. That guide is for creating a new project and running the initial product slice.
