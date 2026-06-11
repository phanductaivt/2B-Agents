---
file_type: "Factory Rule"
primary_agents: ["PO", "BA", "Architect", "Data", "BE", "UIUX", "FE", "QA", "Release"]
supporting_agents: []
activation_mode: "Always-On Shared"
lifecycle_stage: "System Core"
purpose: "Define when a new runtime component should be created through Component Factory."
---
# Component Creation Rules

Create a new component only when:
- an existing component does not already cover the capability
- extending an existing component would create confusion or overload
- the new component has a clear type:
  - Skill
  - Rule
  - Guardrail
  - Runbook
  - Template
  - Artifact
  - Agent
  - Workflow
- the new component has a clear runtime consumer
- the new component solves a repeatable need, not a one-off situation

Do not create a new component when:
- a current component can be updated safely
- the request is actually for a project output
- the only difference is wording, not behavior
