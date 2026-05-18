---
file_type: "Template Index"
primary_agents: ["PO", "BA", "Architect", "Data", "BE", "UIUX", "FE", "QA", "Release"]
supporting_agents: []
activation_mode: "Manual Navigation"
lifecycle_stage: "System Core"
purpose: "Explain the available templates and checklists that standardize output quality."
---
# Templates

This folder stores reusable Markdown/HTML templates for final outputs.

Templates are grouped by `document type`, not by agent.

## Folder Structure

- `requirements/`
  - BRD
  - FRS
  - user story
  - acceptance criteria
- `architecture/`
  - architecture note
  - NFR review
  - security review
- `data/`
  - data model
  - state transition
  - schema plan
  - metric tracking plan
- `technical-design/`
  - BE spec
  - API contract
  - FE technical design
- `implementation/`
  - BE and FE implementation-plan templates used by the owning BE/FE output folders
- `design/`
  - wireframe
- `quality/`
  - test scenarios
  - test cases
  - release-readiness review
- `release/`
  - run instructions
  - runnable verification
- `change-control/`
  - change request intake
  - impact analysis
  - regeneration plan
  - rollback plan
  - change verification
  - change log
- `checklists/`
  - lightweight review checklists for artifact quality

## How To Use

- Use `requirements/` for business and analysis documents.
- Use `architecture/` for system shape, NFR, and security review.
- Use `data/` for persistence, state design, and feature metric tracking plans.
- Use `technical-design/` for BE behavior, API structure, and FE technical design.
- Use `implementation/` for BE and FE implementation planning.
- Use `design/` for low-detail interaction and screen structure.
- Use `quality/` for QA review artifacts.
- Use `release/` for local runnable verification and run instructions.
- Use `change-control/` for post-baseline change request governance.
- Use `checklists/` only as review support, not as final output.

Optional checklist references live in:
- `system/templates/checklists/`
