---
file_type: "Workflows Index"
primary_agents: []
supporting_agents: ["PO", "BA", "Architect", "Data", "BE", "UIUX", "FE", "QA", "Release"]
activation_mode: "Workflow Selection"
lifecycle_stage: "System Core"
purpose: "Select the workflow contract that governs the current multi-phase task."
---
# Workflows Index

Use this registry to select one active workflow before selecting its active
phase and runbook. Load only the selected workflow contract.

| Workflow ID | Contract | Purpose | Trigger | Coordinator / Entry Runbook | Active Agents | Primary Approval Gate | Required Outputs | Status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `product-slice` | `system/workflows/product-slice-workflow.md` | Govern one new requirement through product, delivery, QA, and runnable verification. | New product-slice request. | `system/runbooks/generate-product-slice.md` | PO, BA, Architect, Data, BE, UIUX, FE, QA, Release by active phase | User approval after BA clarification | Phase outputs defined by `system/registries/output-contracts.md` | Active |
| `change-request` | `system/workflows/change-request-workflow.md` | Govern a post-baseline change through impact, approval, controlled apply, verification, merge, or rollback. | Change or customization request for a stable project. | `system/runbooks/handle-change-request.md` | Owning Agent per approved affected artifact; `None` for orchestration phases | User approval after impact analysis and again for expanded scope | Change-control outputs and approved affected targets | Active |
| `component-governance` | `system/workflows/component-governance-workflow.md` | Govern controlled creation, review, or update of runtime system components. | Component creation, review, or update request. | Exact runbook under `system/component-factory/runbooks/` selected by operation and component type | None; no instruction-defined Component Factory Agent exists | User approval for destructive, structural, or breaking change | Target component plus required Component Factory report/change log | Active |

## Selection Rules

- Use `product-slice` for first-time requirement delivery.
- Use `change-request` for changes to an existing stable project.
- Use `component-governance` for system component work, not product outputs.
- If the task does not match a registered workflow, stop and record the
  uncertainty instead of combining workflows.

## Shared Governance

All registered workflows use:

- `system/executors/executor-contract.md`
- `system/workflows/workflow-lifecycle.md`
- `system/handoff/README.md`
- `system/registries/runbooks-index.md`
- `system/registries/rules-index.md`
