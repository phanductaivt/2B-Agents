---
name: create-agent
description: Use when a new instruction-defined Agent is justified and no existing Agent can safely own the responsibility; do not use to define an AI Executor, temporary persona, or governance/factory Agent.
---
# Create Agent

## Purpose

Create a bounded instruction-defined Agent through Component Factory.

## Steps

1. Check `system/registries/agents-index.md` and only relevant existing
   `system/agents/<role>/AGENT.md` files for overlap.
2. Read the exact relevant entries in the skills and rules registries.
3. Use `system/component-factory/runbooks/create-agent-runbook.md`.
4. Use `system/component-factory/templates/agent-template.md`.
5. Update the Agent registry and only approved dependent routing references.
6. Produce the Component Factory creation report.

## Required Checks

- clear identity, purpose, responsibilities, and non-responsibilities
- explicit inputs, outputs, skills, rules, guardrails, runbooks, ownership,
  handoff, and boundaries
- valid and invalid usage examples
- no overlap with existing Agent ownership

## Prohibited Actions

- do not conflate Agent and AI Executor
- do not invent a Router, Governance, or Factory Agent
- do not silently reassign another Agent's outputs or responsibilities
