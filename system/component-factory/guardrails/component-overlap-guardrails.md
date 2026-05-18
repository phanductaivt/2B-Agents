---
file_type: "Factory Guardrail"
primary_agents: ["PO", "BA", "Architect", "Data", "BE", "UIUX", "FE", "QA", "Release"]
supporting_agents: []
activation_mode: "Always-On Shared"
lifecycle_stage: "System Core"
purpose: "Prevent duplicate or overlapping runtime components from being created through Component Factory."
---
# Component Overlap Guardrails

- risk category: duplication and semantic overlap
- trigger condition: request to create a new component similar to an existing one
- prohibited actions:
  - creating a near-duplicate component
  - splitting one capability across two weak overlapping components
- required checks:
  - search related runtime folders
  - compare purpose, scope, and target usage
- stop condition:
  - overlap remains unresolved
- safe fallback:
  - recommend updating an existing component instead of creating a new one
