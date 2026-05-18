---
file_type: "Factory Rule"
primary_agents: ["PO", "BA", "Architect", "Data", "BE", "UIUX", "FE", "QA", "Release"]
supporting_agents: []
activation_mode: "Always-On Shared"
lifecycle_stage: "System Core"
purpose: "Define scope rules for runtime components created or updated through Component Factory."
---
# Component Scope Rules

Each component must have:
- one primary purpose
- one clear component type
- one clear runtime usage surface

Keep scope clean by:
- separating creation logic from runtime execution logic
- separating quality control from generation logic
- separating artifact definition from artifact execution

Scope failures include:
- a skill that behaves like a runbook
- a rule that behaves like a guardrail
- a template that tries to encode business output generation logic
- an artifact contract that tries to act like a project deliverable
