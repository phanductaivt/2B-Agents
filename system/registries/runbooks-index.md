---
file_type: "Runbooks Index"
primary_agents: []
supporting_agents: ["PO", "BA", "Architect", "Data", "BE", "UIUX", "FE", "QA", "Release"]
activation_mode: "Routing Reference"
lifecycle_stage: "System Core"
purpose: "Map workflow phases and operations to existing runbooks without bulk-loading runbook folders."
---
# Runbooks Index

Use this index to identify a candidate runbook. Load only the selected runbook.
The runbook's own Required Context remains authoritative for phase execution.

## Product Delivery And Change Control

| Runbook | Active Agent | Related Workflow | Use When | Primary Result |
| --- | --- | --- | --- | --- |
| `system/runbooks/generate-product-slice.md` | Active phase Agent only | `product-slice` | Coordinating one new requirement | Delegates to phase runbooks |
| `system/runbooks/generate-brd.md` | PO | `product-slice` | Product intent and BRD are needed | PO BRD |
| `system/runbooks/generate-ba-package.md` | BA | `product-slice` | Clarification and BA package are needed | BA package and approval gate |
| `system/runbooks/generate-architecture.md` | Architect | `product-slice` | Technical shape, NFR, and security direction are needed | Architecture package |
| `system/runbooks/generate-data-design.md` | Data | `product-slice` | Persistence, state, schema, or metrics need design | Data package |
| `system/runbooks/generate-be-package.md` | BE | `product-slice` | Backend behavior and API contract need design | BE package |
| `system/runbooks/implement-be.md` | BE | `product-slice`, `change-request` when approved | Backend implementation is approved and ready | Backend app, tests, and plan |
| `system/runbooks/generate-wireframe.md` | UIUX | `product-slice` | Reviewable UX flow and screen intent are needed | Wireframe |
| `system/runbooks/generate-fe-ui.md` | FE | `product-slice` | Reviewable frontend UI is needed | FE review UI |
| `system/runbooks/implement-fe.md` | FE | `product-slice`, `change-request` when approved | Frontend implementation is approved and ready | Frontend app and plan |
| `system/runbooks/generate-qa-review.md` | QA | `product-slice`, `change-request` when approved | Quality review and smoke planning are needed | QA package |
| `system/runbooks/integrate-runnable-app.md` | Release | `product-slice`, `change-request` when approved | Reproducible run instructions are needed | Run instructions |
| `system/runbooks/verify-runnable-system.md` | Release | `product-slice`, `change-request` when approved | Runnable status needs command evidence | Runnable verification and readiness |
| `system/runbooks/resolve-clarification.md` | Owning Agent | Recovery route for `product-slice` or `change-request` | Material ambiguity blocks safe continuation | Clarified source or affected artifact |
| `system/runbooks/regenerate-output.md` | Owning Agent | Recovery route for `product-slice`; approved target route for `change-request` | One approved target needs regeneration | Updated target only |
| `system/runbooks/handle-change-request.md` | Owning Agent only during owned artifact work; otherwise None | `change-request` | Stable project receives a change request | Controlled CR lifecycle outputs |
| `system/runbooks/phase-5-end-to-end-test.md` | Active product phase Agent | Manual testing, outside registered delivery workflows | A controlled workflow test is explicitly requested | Manual findings summary |

## Continuity

| Runbook | Active Agent | Related Workflow | Use When | Primary Result |
| --- | --- | --- | --- | --- |
| `system/handoff/update-handoff-runbook.md` | Current Agent or None | All workflows | Work pauses, blocks, changes state, or completes | Updated canonical handoff |
| `system/handoff/switch-ai-executor-runbook.md` | Preserve recorded Agent | All workflows | Another AI Executor continues the task | Confirmed continuation state |

## Component Factory

| Runbook | Active Agent | Related Workflow | Use When | Primary Result |
| --- | --- | --- | --- | --- |
| `system/component-factory/runbooks/create-skill-runbook.md` | None | `component-governance` | Creating a runtime Skill | Skill definition and creation report |
| `system/component-factory/runbooks/create-rule-runbook.md` | None | `component-governance` | Creating a runtime Rule | Rule definition and creation report |
| `system/component-factory/runbooks/create-guardrail-runbook.md` | None | `component-governance` | Creating a runtime Guardrail | Guardrail definition and creation report |
| `system/component-factory/runbooks/create-runbook-runbook.md` | None | `component-governance` | Creating a runtime Runbook | Runbook definition and creation report |
| `system/component-factory/runbooks/create-template-runbook.md` | None | `component-governance` | Creating a runtime Template | Template definition and creation report |
| `system/component-factory/runbooks/create-artifact-runbook.md` | None | `component-governance` | Creating an Artifact contract | Artifact contract and creation report |
| `system/component-factory/runbooks/create-agent-runbook.md` | None | `component-governance` | Creating an instruction-defined Agent | Agent definition, registry update, and creation report |
| `system/component-factory/runbooks/create-workflow-runbook.md` | None | `component-governance` | Creating an executor-neutral Workflow | Workflow contract, registry update, and creation report |
| `system/component-factory/runbooks/review-component-runbook.md` | None | `component-governance` | Reviewing an existing system component | Component review report |
| `system/component-factory/runbooks/update-component-runbook.md` | None | `component-governance` | Updating an existing system component | Controlled update and change log |

## Uncertainty

- Legacy Component Factory runbooks do not all use the standard runtime
  `Required Context` structure. The component-governance workflow narrows their
  routing; Agent and Workflow creation runbooks declare exact context.
