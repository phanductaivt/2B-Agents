---
file_type: "Workflow Contract"
workflow_id: "product-slice"
primary_agents: ["PO", "BA", "Architect", "Data", "BE", "UIUX", "FE", "QA", "Release"]
supporting_agents: []
activation_mode: "User Request"
lifecycle_stage: "System Core"
purpose: "Govern one requirement from product intent through quality review and runnable verification."
---
# Product Slice Workflow

## Workflow ID

- `product-slice`

## Purpose

Coordinate one new requirement through the existing product-slice runbooks.
This workflow governs phase order, approval, recovery, handoff, and completion;
`system/runbooks/generate-product-slice.md` remains the orchestration procedure.

## Trigger

- A user requests a new product slice from a requirement.
- Do not use for an approved post-baseline change request; use
  `system/workflows/change-request-workflow.md`.

## Required Inputs

- `projects/<project>/01-input/requirements/<req>.md`
- relevant files from `projects/<project>/03-context/`
- `system/executors/executor-contract.md`
- `system/workflows/workflow-lifecycle.md`
- `system/runbooks/generate-product-slice.md`
- `system/registries/context-routing.md`
- `system/registries/agents-index.md`
- `system/registries/skills-index.md`
- `system/registries/runbooks-index.md`
- `system/registries/rules-index.md`
- `system/registries/output-contracts.md`

## Active Phases

Required skills, rules, guardrails, templates, inputs, and handoff outputs are
loaded from the active runbook only. Shared JIT guardrails are
`system/guardrails/define-context-loading.md` and the exact additional
guardrails declared by that runbook.

| Phase | Active Agent | Required Runbook | Entry Condition | Required Skills / Rules / Guardrails | Required Outputs | Exit Condition |
| --- | --- | --- | --- | --- | --- | --- |
| Coordination | None | `system/runbooks/generate-product-slice.md` | Requirement and project identified | Orchestration context declared by runbook | Delegated only | Active phase selected |
| Product intent | PO | `system/runbooks/generate-brd.md` | Requirement available | Active-runbook Required Context | `02-output/po/<req>-brd.md` | Product intent sufficient for BA |
| BA clarification | BA | `system/runbooks/generate-ba-package.md` | PO BRD available | Active-runbook Required Context | `02-output/ba/<req>-clarification.md` | Clarification gate explicitly approved |
| BA package generation | BA | `system/runbooks/generate-ba-package.md` | Clarification gate explicitly approved | Active-runbook Required Context | `02-output/ba/<req>-process-bpmn.md` when process behavior applies, `02-output/ba/<req>-user-story.md`, `02-output/ba/<req>-acceptance-criteria.md`, `02-output/ba/<req>-frs.md`, `02-output/ba/<req>-feature-list.md` | Required BA package outputs are complete and no blocking gap remains |
| Architecture | Architect | `system/runbooks/generate-architecture.md` | BA package generation exit condition satisfied | Active-runbook Required Context | Architecture outputs in output contracts | Architecture stop conditions clear |
| Data design | Data | `system/runbooks/generate-data-design.md` | Architecture and BA handoff available | Active-runbook Required Context | Data outputs in output contracts | Data handoff complete |
| Backend design | BE | `system/runbooks/generate-be-package.md` | Required BA/architecture/data handoffs available | Active-runbook Required Context | BE spec and API contract | Backend contract complete |
| Backend implementation | BE | `system/runbooks/implement-be.md` | Approved backend contract available | Active-runbook Required Context | BE plan, backend app, backend tests | Backend run/test path documented |
| UX design | UIUX | `system/runbooks/generate-wireframe.md` | Approved BA behavior available | Active-runbook Required Context | Wireframe | FE handoff complete |
| Frontend review UI | FE | `system/runbooks/generate-fe-ui.md` | BA, BE, and wireframe handoffs available | Active-runbook Required Context | FE review UI | Review UI handoff complete |
| Frontend implementation | FE | `system/runbooks/implement-fe.md` | API contract, wireframe, and FE planning available | Active-runbook Required Context | FE plan and frontend app | Build/start path documented |
| Quality review | QA | `system/runbooks/generate-qa-review.md` | Required requirement and delivery outputs available | Active-runbook Required Context | QA outputs in output contracts | Quality risks and smoke plan recorded |
| Runnable integration | Release | `system/runbooks/integrate-runnable-app.md` | Backend, frontend, and QA smoke plan available | Active-runbook Required Context | Run instructions | Reproducible commands documented |
| Runnable verification | Release | `system/runbooks/verify-runnable-system.md` | Run instructions and runnable app available | Active-runbook Required Context | Runnable verification and Release readiness | Actual command evidence and status recorded |

## Required Skills / Rules / Guardrails

- Skills: exact paths declared by the active phase runbook and
  `system/registries/skills-index.md` only.
- Rules: exact paths declared by the active phase runbook and
  `system/registries/rules-index.md` only.
- Guardrails: `system/guardrails/define-context-loading.md` plus exact
  additional guardrails declared by the active phase runbook only.

## Approval Gates

- BA clarification gate:
  - required approver: user
  - evidence: `02-output/ba/<req>-clarification.md`
  - allowed decisions: `Approved - Proceed`, `Approved - Proceed with assumptions`, `Blocked`
  - blocked actions: BA package generation, Architect, and all downstream phases

## Stop Conditions

- Stop when the active runbook reports missing required context.
- Stop while clarification approval is pending or blocked.
- Stop before a phase whose exact upstream handoff is missing.
- Stop before runnable claims without actual Release command evidence.
- Stop if the active AI Executor lacks a required capability or permission.

## Recovery Rules

- Use `system/runbooks/resolve-clarification.md` for material ambiguity.
- Use `system/runbooks/regenerate-output.md` for targeted approved regeneration.
- If scope becomes a post-baseline change request, stop and route to
  `system/workflows/change-request-workflow.md`.

## Handoff Requirements

- Follow `system/handoff/update-handoff-runbook.md` whenever Active Workflow,
  Active Phase, Active Runbook, Active Agent, or Active Executor changes, and
  at approval waits, pauses, blocks, or workflow completion.
- Record exact requirement-scoped upstream outputs consumed by the active phase.
- Follow `system/handoff/switch-ai-executor-runbook.md` when the AI Executor
  changes.

## Done Criteria

- Required phase outputs exist according to
  `system/registries/output-contracts.md`.
- QA quality review and smoke plan are recorded.
- Release records actual runnable verification evidence and reproducible run
  instructions, or honestly records a non-runnable status.
- No blocking approval or missing-context condition remains.

## Uncertainty

- Optional phases may be skipped only when the active runbook and output
  contracts show they are unnecessary for the requested slice.
