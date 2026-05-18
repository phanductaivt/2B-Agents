---
file_type: "Factory Guardrail"
primary_agents: ["PO", "BA", "Architect", "Data", "BE", "UIUX", "FE", "QA", "Release"]
supporting_agents: []
activation_mode: "Always-On Shared"
lifecycle_stage: "System Core"
purpose: "Prevent hallucinated claims about runtime component usage, dependency, or coverage."
---
# Component Hallucination Guardrails

- risk category: false repository claim
- trigger condition: any claim about existing runtime behavior, dependency, overlap, or coverage
- prohibited actions:
  - claiming a component exists without checking
  - claiming a dependency without checking
  - claiming a gap without checking the active folders
- required checks:
  - inspect the repository tree
  - inspect the target file or folder
  - cite the checked location in the report
- stop condition:
  - the claim cannot be supported by local repository evidence
- safe fallback:
  - mark the claim as unverified and recommend local inspection
