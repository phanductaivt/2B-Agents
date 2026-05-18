---
file_type: "Factory Rule"
primary_agents: ["PO", "BA", "Architect", "Data", "BE", "UIUX", "FE", "QA", "Release"]
supporting_agents: []
activation_mode: "Always-On Shared"
lifecycle_stage: "System Core"
purpose: "Define naming rules for runtime components created through Component Factory."
---
# Component Naming Rules

## Core Naming Pattern

- Skills:
  - lowercase slug with hyphens
  - example: `rule-coverage-checker`
- Rules:
  - `define-*` or `read-*` when the file defines or introduces a rule
- Guardrails:
  - `define-*` or `verify-*` when the file governs safety or quality checks
- Runbooks:
  - `verb-target`
  - example: `generate-brd.md`
- Templates:
  - `template-*`
- Checklists:
  - `checklist-*`
- Artifact contracts:
  - short noun-based names that match runtime artifact names

## Naming Constraints

- prefer short, behavior-oriented names
- avoid synonyms for an existing component concept
- avoid agent-name drift
- avoid mixing business output naming with component naming
