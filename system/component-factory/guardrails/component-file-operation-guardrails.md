---
file_type: "Factory Guardrail"
primary_agents: ["PO", "BA", "Architect", "Data", "BE", "UIUX", "FE", "QA", "Release"]
supporting_agents: []
activation_mode: "Always-On Shared"
lifecycle_stage: "System Core"
purpose: "Prevent unsafe file operations during Component Factory work."
---
# Component File Operation Guardrails

- risk category: unsafe file operation
- trigger condition: create, update, or review work that could affect existing runtime files
- prohibited actions:
  - delete
  - rename
  - move
  - overwrite without explicit approval
- required checks:
  - inspect the current file first
  - verify the requested target path
  - confirm whether the action is additive or mutating
- stop condition:
  - the requested operation would alter runtime files without approval
- safe fallback:
  - create an additive proposal or report instead of mutating runtime files
