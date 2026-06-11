---
file_type: "Factory Runbook"
primary_agents: []
supporting_agents: ["PO", "BA", "Architect", "Data", "BE", "UIUX", "FE", "QA", "Release"]
activation_mode: "Triggered By Workflow"
lifecycle_stage: "System Core"
purpose: "Create a new instruction-defined Agent through the isolated Component Factory workflow."
---
# Create Agent Runbook

## Purpose

Create one instruction-defined Agent with explicit ownership, boundaries,
context dependencies, outputs, and handoff obligations.

## When To Use

Use only when a durable role is required and no existing Agent can own the
responsibility without becoming overloaded or ambiguous.

## Required Context

- `system/executors/executor-contract.md`
- `system/handoff/README.md`
- `system/component-factory/component-types-index.md`
- `system/component-factory/meta-skills/create-agent/SKILL.md`
- `system/component-factory/templates/agent-template.md`
- `system/component-factory/rules/component-creation-rules.md`
- `system/component-factory/rules/component-dependency-rules.md`
- `system/component-factory/rules/component-naming-rules.md`
- `system/component-factory/rules/component-scope-rules.md`
- `system/component-factory/guardrails/component-file-operation-guardrails.md`
- `system/component-factory/guardrails/component-overlap-guardrails.md`
- `system/component-factory/guardrails/component-hallucination-guardrails.md`
- `system/component-factory/guardrails/component-breaking-change-guardrails.md`
- exact relevant entries from `system/registries/agents-index.md`
- exact relevant entries from `system/registries/skills-index.md`
- exact relevant entries from `system/registries/rules-index.md`
- only the existing Agent definitions needed for overlap and boundary checks

## Prerequisites

- proposed Agent identity and purpose are explicit
- overlap with existing Agents has been checked
- the user has approved any structural ownership change

## Steps

1. Confirm the request is for an instruction-defined Agent, not an AI Executor,
   skill, workflow, or temporary persona.
2. Check existing Agent responsibilities and output ownership for overlap.
3. Define identity, purpose, responsibilities, non-responsibilities, required
   inputs, required outputs, skills, rules, guardrails, applicable runbooks,
   output ownership, handoff requirements, boundaries, and valid/invalid usage.
4. Use `system/component-factory/templates/agent-template.md`.
5. Create the Agent at `system/agents/<role>/AGENT.md`.
6. Update `system/registries/agents-index.md`.
7. Update `system/agents/define-agent-usage-matrix.md`, workflow phases,
   runbook routing, output contracts, or other registries only when the new
   Agent is explicitly approved for those surfaces.
8. Record exact dependencies checked and registry changes in the Component
   Factory creation report.

## Validation Checklist

- Agent and AI Executor identities are not conflated
- purpose and ownership are distinct from existing Agents
- responsibilities and non-responsibilities are explicit
- inputs, outputs, skills, rules, guardrails, and applicable runbooks use exact
  paths where they exist
- authoritative and advisory outputs are distinguished
- handoff requirements and valid/invalid usage examples exist
- `system/registries/agents-index.md` is updated
- no new governance, router, or factory Agent was invented

## Expected Output

- `system/agents/<role>/AGENT.md`
- updated `system/registries/agents-index.md`
- only approved dependent registry or routing updates
- `system/component-factory/artifacts/component-creation-report.md`

## Stop / Approval Conditions

- Stop if responsibility or output ownership overlaps an existing Agent.
- Stop if required skills, rules, guardrails, runbooks, or outputs are missing
  or ambiguous.
- Stop before changing an existing Agent's ownership without explicit approval.

## Recovery / Rollback Note

If the proposed role is only a reusable capability or phase sequence, redirect
to Skill or Workflow creation instead of creating an Agent.
