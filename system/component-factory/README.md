---
file_type: "Factory Guide"
primary_agents: ["PO", "BA", "Architect", "Data", "BE", "UIUX", "FE", "QA", "Release"]
supporting_agents: []
activation_mode: "Manual Navigation"
lifecycle_stage: "System Core"
purpose: "Explain the isolated Component Factory layer for creating and controlling AI operating components."
---
# Component Factory

## What It Is

`system/component-factory/` is an isolated factory layer for creating, reviewing, updating, and quality-controlling AI operating components.

It governs only these component types:
- Skill
- Rule
- Guardrail
- Runbook
- Template
- Artifact
- Agent
- Workflow

Use `system/component-factory/component-types-index.md` to select one supported
component type and its exact creation route.

It does **not** create business delivery outputs such as:
- BRD
- FRS
- test cases for a project slice
- wireframes
- API contracts for a project slice
- HTML screens

## When To Use It

Use Component Factory when you need to:
- create a new system skill
- create a new rule or guardrail
- create a new runbook
- create a new template
- define or revise an artifact contract
- create or revise an instruction-defined Agent
- create or revise an executor-neutral workflow contract
- review an existing system component for quality, overlap, or safety
- update a component without breaking runtime behavior

## When Not To Use It

Do not use Component Factory when you need to:
- generate project outputs in `projects/<project>/02-output/`
- execute runtime delivery flows directly
- bypass runtime `system/rules/`, `system/guardrails/`, `system/runbooks/`, `system/skills/`, or `system/templates/`
- redesign active runtime folders without explicit approval

## Runtime System vs Component Factory

- Runtime system:
  - `system/rules/`
  - `system/guardrails/`
  - `system/runbooks/`
  - `system/skills/`
  - `system/templates/`
  - `system/artifacts/`
  - used by an AI Executor to operate instruction-defined Agents and execute delivery work

- Component Factory:
  - `system/component-factory/`
  - used to create or control the runtime components themselves

Runtime is for **using** components.
Component Factory is for **making and maintaining** components.

## Folder Map

- `meta-skills/`
  - factory-only skills that create or review components
- `rules/`
  - rules for when and how to create or update components
- `guardrails/`
  - safety controls for component work
- `runbooks/`
  - step-by-step workflows for component creation, review, and update
- `templates/`
  - reusable templates for component definitions and reports
- `artifacts/`
  - standard reports, checklists, and maps used after component work
- `component-types-index.md`
  - routes supported component types to canonical runtime homes, creation
    procedures, templates, and registries

## Component Creation Workflow

1. Start with the relevant meta-skill in `meta-skills/`
2. Read the relevant Component Factory rules
3. Read the relevant Component Factory guardrails
4. Use the matching Component Factory runbook
5. Use the matching Component Factory template
6. Check the existing runtime folders before creating anything
7. Create or update the target component only after overlap and safety checks
8. Produce the required Component Factory report artifact

Agent and Workflow component work must also follow:
- `system/executors/executor-contract.md`
- `system/handoff/`
- `system/workflows/component-governance-workflow.md`

Agent creation updates `system/registries/agents-index.md`. Workflow creation
updates `system/registries/workflows-index.md`. Update other registries only
when their exact entries actually change.

## Safety Rules

- never delete runtime files without explicit approval
- never rename runtime files without explicit approval
- never move runtime files without explicit approval
- never overwrite existing files blindly
- never create a duplicate component when an existing one can be extended safely
- never claim a dependency, capability, or usage path without checking the current repository first

## Required Report After Any Component Change

After creating, reviewing, or updating any component, produce:
- `component-creation-report.md` for creation
- `component-review-report.md` for review
- `component-change-log.md` for update tracking

Use `component-quality-checklist.md` and `component-dependency-map.md` as supporting control artifacts.
