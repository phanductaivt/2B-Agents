---
file_type: "Factory Template"
primary_agents: []
supporting_agents: ["PO", "BA", "Architect", "Data", "BE", "UIUX", "FE", "QA", "Release"]
activation_mode: "On Agent Creation Or Review"
lifecycle_stage: "System Core"
purpose: "Provide the minimum definition required for a bounded instruction-defined Agent."
---
# <Agent Name> Agent

## Agent Identity

- role name:
- canonical path: `system/agents/<role>/AGENT.md`
- phase-specific or supporting:

## Purpose

- why this Agent exists
- distinct ownership need it satisfies

## Responsibilities

- allowed responsibility:

## Non-Responsibilities

- forbidden responsibility:

## Context Loading Rules

- Start from the active workflow phase and its one active runbook.
- Load only the active runbook's Required Context.
- Read only `system/agent-knowledge/<role>/INDEX.md` first when reusable role
  knowledge is needed.
- Do not bulk-read system directories or previous output folders.

## Required Inputs

- exact input or handoff type:

## Required Outputs

- exact authoritative output:
- advisory output, if any:

## Required Skills

- exact skill path, or `None`:

## Required Rules / Guardrails

- exact rule path:
- exact guardrail path:

## Required Runbooks

- exact runbook path when applicable, or `None`:

## Output Ownership

- authoritative ownership:
- advisory-only contribution:
- ownership conflict stop condition:

## Handoff Requirements

- required upstream handoff:
- required downstream handoff:
- canonical continuity update condition:

## Boundaries

- collaboration boundary:
- stop or approval boundary:

## Valid Usage Examples

- valid:

## Invalid Usage Examples

- invalid:

## Registry Update Requirements

- update `system/registries/agents-index.md`
- update `system/agents/define-agent-usage-matrix.md` when the Agent enters
  runtime phase routing
- update exact workflow, runbook, output-contract, or context-routing references
  only when explicitly approved and applicable

## Uncertainty

- unresolved ownership or dependency question:
