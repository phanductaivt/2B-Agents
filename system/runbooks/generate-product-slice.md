---
file_type: "Runbook"
primary_agents: ["PO", "BA", "Architect", "Data", "BE", "UIUX", "FE", "QA", "Release"]
supporting_agents: []
activation_mode: "Triggered By Workflow"
lifecycle_stage: "System Core"
purpose: "Coordinate one requirement from business input to runnable local software outputs."
reads: ["01-input/", "03-context/", "system/rules/", "system/guardrails/", "system/runbooks/", "system/agents/", "system/skills/", "system/templates/"]
produces: ["02-output/"]
---
# Generate Product Slice

Use this runbook as the master flow for one requirement.

## Phase 0: Requirement Discovery And Clarification Gate

Before running downstream agents, PO and BA must inspect the requirement and project context for:
- problem insight
- current pain point
- affected actor or stakeholder
- expected business value
- missing business rules
- clarification questions
- assumptions
- recommended proceed or block decision
- user approval status

Question handling:
- classify each question as `blocking`, `non-blocking`, or `assumption-backed`
- ask the user only for blocking questions that would materially change safe product behavior
- record non-blocking questions with the assumption that allows the work to proceed
- if no clarification questions are needed, explicitly state why the requirement is safe to proceed

Approval handling:
- the agent may recommend `Proceed`, `Proceed with assumptions`, or `Blocked`
- the agent must set `User Approval Status: Pending User Approval` after the clarification gate
- when waiting for approval, the final response must point the user to the exact review file and sections to read
- do not continue to Architect, Data, BE, UIUX, FE, QA, or Release until the user explicitly approves `Approved - Proceed` or `Approved - Proceed with assumptions`
- if the user marks the gate `Blocked`, stop and wait for updated input or a user decision to override the block
- do not continue while any blocking question remains unanswered and cannot be safely handled as an explicit assumption

## Agent Sequence

1. PO: `generate-brd.md`
2. BA: `generate-ba-package.md`
3. Architect: `generate-architecture.md`
4. Data: `generate-data-design.md`
5. BE: `generate-be-package.md`, then `implement-be.md`
6. UIUX: `generate-wireframe.md`
7. FE: `generate-fe-ui.md`, then `implement-fe.md`
8. QA: `generate-qa-review.md`
9. Release: `integrate-runnable-app.md`, then `verify-runnable-system.md`

## Required Checks Before Advancing

- do not start BA without PO BRD
- do not start architecture or any downstream agent without explicit user approval after the BA clarification gate
- do not treat a recommended decision as approval
- do not continue when the user approval status is `Pending User Approval` or `Blocked`
- do not start architecture without PO BRD and BA package
- do not start data design without architecture and BA package
- do not implement BE without BE spec, API contract, architecture, and data design
- do not implement FE without API contract, wireframe, and FE technical design or equivalent FE planning
- do not verify runnable status without app code, tests or smoke checks, and run commands

## Expected Output

- final artifacts in `02-output/`
- runnable code in `02-output/app/backend/` and `02-output/app/frontend/`
- smoke test planning in `02-output/qa/`
- verification results in `02-output/release/`

When the run stops for approval, the final response must include:
- review file: `02-output/ba/<req>-clarification.md`
- sections to review: `Insight & Pain Point`, `Known Facts`, `Assumptions`, `Blocking Questions`, `Non-Blocking Questions`, `Recommended Decision`, `User Approval Status`, and `Downstream Readiness Notes`
- current recommended decision and approval status
- exact acceptable user replies: `Approved - Proceed`, `Approved - Proceed with assumptions`, or `Blocked`

## Recovery

If a downstream step finds a material conflict, stop and use `resolve-clarification.md` or regenerate only the affected upstream artifact.
