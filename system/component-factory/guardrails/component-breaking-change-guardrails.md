---
file_type: "Factory Guardrail"
primary_agents: ["PO", "BA", "Architect", "Data", "BE", "UIUX", "FE", "QA", "Release"]
supporting_agents: []
activation_mode: "Always-On Shared"
lifecycle_stage: "System Core"
purpose: "Prevent breaking changes to existing runtime components during Component Factory work."
---
# Component Breaking Change Guardrails

- risk category: runtime breakage
- trigger condition: update request affecting components already referenced by runtime layers
- prohibited actions:
  - silent scope change
  - silent naming change
  - silent dependency change
- required checks:
  - inspect related Agents, workflows, runbooks, rules, guardrails, templates,
    output contracts, registries, and matrix references as applicable
  - inspect whether filenames or component names are already used elsewhere
- stop condition:
  - the update would break current runtime assumptions without approval
- safe fallback:
  - propose a staged update plan or additive extension instead
