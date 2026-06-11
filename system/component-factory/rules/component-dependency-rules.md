---
file_type: "Factory Rule"
primary_agents: ["PO", "BA", "Architect", "Data", "BE", "UIUX", "FE", "QA", "Release"]
supporting_agents: []
activation_mode: "Always-On Shared"
lifecycle_stage: "System Core"
purpose: "Define how Component Factory should manage dependencies between runtime components."
---
# Component Dependency Rules

Before creating or updating a component:
- check upstream runtime folders first
- identify which runtime layers will read or depend on the component
- prefer explicit dependency over implied dependency

Dependency rules:
- a runbook may depend on skills, templates, rules, and guardrails
- a skill may depend on rules, guardrails, templates, and examples
- a guardrail may depend on templates or checklists for validation support
- a template may support multiple agents but should stay document-type-oriented
- an Agent may depend on exact skills, rules, guardrails, runbooks, input
  handoffs, output contracts, and registry entries
- a Workflow may depend on exact Agents, runbooks, skills, rules, guardrails,
  output contracts, workflow lifecycle, handoff, and registry entries

Do not:
- claim a dependency that is not checked locally
- create circular dependency language between components
- assign multiple active runbooks to one Workflow phase
- invent an Agent for governance or orchestration when `Active Agent: None`
  is correct
