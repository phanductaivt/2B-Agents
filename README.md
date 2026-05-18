---
file_type: "Repository Guide"
primary_agents: ["PO", "BA", "Architect", "Data", "BE", "UIUX", "FE", "QA", "Release"]
supporting_agents: []
activation_mode: "Manual Navigation"
lifecycle_stage: "Repository Root"
purpose: "Explain the repository operating model, active folders, and daily workflow."
---
# 2B Agents

`2B Agents` is now a pure AI Operating Repository.

Operating model:

**Business Input -> Project Context -> Runbook -> Agent -> Skill -> Template -> Final Output -> Runnable App**

Codex/AI is the execution engine.

Stable project change model:

**Change Request -> Impact Analysis -> Approval -> Baseline -> Targeted Apply -> Verification -> Requirement Merge Or Rollback**

## Active Repository Areas

- `projects/`
- `system/rules/`
- `system/guardrails/`
- `system/runbooks/`
- `system/agents/`
- `system/agent-knowledge/`
- `system/skills/`
- `system/templates/`
- `system/artifacts/`

## Daily Workflow

1. Clone `projects/project-template/`
2. Put business input into `01-input/`
3. Put project context into `03-context/`
4. Prompt Codex using the copy-ready cookbook in `projects/PROJECT_EXECUTION_GUIDE.md`
5. Codex creates the PO/BA clarification gate and stops for user approval
6. Review `02-output/ba/<req>-clarification.md`
7. Approve with `Approved - Proceed` or `Approved - Proceed with assumptions`, or block and update input/context
8. Continue with Architect, Data, BE, Design, FE, QA, and Release only after approval
9. Review final artifacts, runnable code, and verification evidence in `02-output/`
10. Codex reads:
   - `system/rules/`
   - `system/guardrails/`
   - `system/runbooks/`
   - `system/agents/`
   - `system/agent-knowledge/`
   - `system/skills/`
   - `system/templates/`
   - project `01-input/`
   - project `03-context/`
11. Codex writes every project output into `02-output/`, including runnable software and tests
   - `02-output/po/` for PO BRD when product framing is needed
   - `02-output/ba/` for the BA package
   - `02-output/architecture/` for architecture, NFR, and security review
   - `02-output/data/` for data model, state transition, SQLite schema planning, and metric tracking plans
   - `02-output/be/` for BE API, service design, and BE implementation planning
   - `02-output/design/` for wireframe
   - `02-output/fe/` for UI and FE implementation planning
   - `02-output/qa/` for QA test design, smoke test planning, and quality review
   - `02-output/release/` for run instructions and runnable-system verification

Runnable code belongs in:
- `02-output/app/backend/`
- `02-output/app/frontend/`

## Change Request Workflow

Use `projects/PROJECT_CHANGE_REQUEST_GUIDE.md` after a project is already stable and a customer sends a change request or customization request.

Change request work uses:
- `01-input/change-requests/` for CR intake
- `02-output/change-analysis/` for impact analysis, regeneration plan, rollback plan, verification, and change log
- `05-baselines/` for pre-apply snapshots when Git is not used as the rollback layer
- `system/runbooks/handle-change-request.md` as the governing runbook

Core change request rule:
- do not apply or regenerate a CR before impact analysis and explicit approval
- do not apply an approved CR without a baseline snapshot when Git is not being used
- merge the CR into the linked requirement only after verification
- rejected CRs remain as audit trail and must not modify official requirement/output/app files

## Project Context Rule

Project-specific business, domain, and policy context belongs in:
- `projects/<project>/03-context/`

If project context is missing, Codex should:
- infer from the requirement
- use the active rules, agent guidance, skills, and templates
- create the clarification gate first
- ask clarification only when a gap is critical
- stop until the user approves downstream execution
