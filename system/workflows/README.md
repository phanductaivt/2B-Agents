---
file_type: "Workflow Governance Index"
primary_agents: []
supporting_agents: ["PO", "BA", "Architect", "Data", "BE", "UIUX", "FE", "QA", "Release"]
activation_mode: "Workflow Selection"
lifecycle_stage: "System Core"
purpose: "Explain how executor-neutral workflows coordinate existing runbooks, agents, approvals, outputs, and handoffs."
---
# Workflows

## Purpose

`system/workflows/` defines multi-phase governance without duplicating the
procedures owned by runbooks.

An AI Executor selects one active workflow, then one active phase and runbook.
The active runbook selects the instruction-defined Agent and the exact context
needed for that phase.

## Workflow And Runbook Boundary

- A workflow defines phase order, gates, transitions, recovery, handoff, and
  done criteria.
- A runbook defines how to perform one operation or phase.
- An Agent defines role ownership.
- Registries provide routing, ownership, skills, rules, and output contracts.
- MCP is an optional governed tool capability. It is not a workflow or Agent.

## Start Here

- `system/registries/workflows-index.md`: select the workflow.
- `workflow-lifecycle.md`: govern workflow state and transitions.
- `workflow-contract-template.md`: required structure for future workflows.
- `product-slice-workflow.md`: create one product slice.
- `change-request-workflow.md`: control a post-baseline change request.
- `component-governance-workflow.md`: create, review, or update system
  components through Component Factory.

## Required Shared Governance

Every workflow must:

1. Follow `system/executors/executor-contract.md`.
2. Use `system/handoff/` for continuity when work pauses, changes phase, or
   changes AI Executor.
3. Start each phase from its required runbook.
4. Use `system/registries/context-routing.md` and the active runbook for JIT
   context loading.
5. Use `system/registries/output-contracts.md` for project-output ownership.
6. Load MCP governance only when the active workflow phase explicitly requires
   an MCP capability.

## No Parallel Source Of Truth

Workflow contracts summarize routing and control state. They do not replace or
override existing runbooks, Agent definitions, rules, guardrails, skills,
templates, output contracts, approvals, or handoff evidence.
