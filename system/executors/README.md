---
file_type: "Executor Governance Index"
primary_agents: []
supporting_agents: ["PO", "BA", "Architect", "Data", "BE", "UIUX", "FE", "QA", "Release"]
activation_mode: "Always-On Shared"
lifecycle_stage: "System Core"
purpose: "Explain the executor-neutral governance layer for AI systems that operate instruction-defined agents."
---
# AI Executors

## Purpose

`system/executors/` defines how an AI system operates this repository without
being confused with an instruction-defined Agent.

An **AI Executor** is the AI system or client currently reading repository
instructions, activating an Agent role, using approved tools, and performing the
active runbook. Examples may include Codex or another capable AI system.

An **Agent** is an instruction-defined role stored under `system/agents/`.
Agents are not assumed to be separate models or separate running processes.

## Core Distinction

| Concept | Meaning |
| --- | --- |
| AI Executor | The current AI system or client performing repository work. |
| Agent | The active instruction-defined role and ownership boundary. |
| Workflow | The multi-phase operating flow, when one is active. |
| Runbook | The procedure currently being executed. |
| Skill | A reusable capability instruction loaded by the active runbook. |
| MCP tool | An optional governed tool capability available to an Executor. |
| Handoff | The continuity record used when work pauses or the Executor changes. |

## Start Here

- `executor-contract.md`: required behavior for every AI Executor.
- `executor-capability-template.md`: capability and permission declaration.
- `executor-switching-policy.md`: continuity and safety rules when changing
  Executors.
- `system/registries/workflows-index.md`: select the active workflow.
- `system/workflows/workflow-lifecycle.md`: workflow state and transition rules.
- `system/handoff/latest-handoff.md`: current repository-wide continuity record.

## Operating Rule

The active runbook and Agent definition govern the work. Executor identity does
not change Agent ownership, approval gates, output contracts, or required
handoffs.

An Executor must not claim access to a tool, MCP server, command environment,
network, file path, or permission until that capability is available or
verified in the current session.
