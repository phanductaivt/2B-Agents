# Task Routing

Use this guide to choose the right agent/process quickly.

## BA Agent (main owner)
Use for:
- Requirement clarification
- BPMN Mermaid process flow
- BRD, FRS, user story, acceptance criteria
- Feature hierarchy and scope structuring
- Initial traceability links

## UXUI Agent
Use for:
- Wireframe creation from BA FRS + feature scope
- UX notes for flows, states, and edge behavior

## FE Agent
Use for:
- `ui.html` implementation from wireframe + FRS
- Mapping UI elements to functional requirements

## Reviewer / Validators
Use for:
- Ambiguity checks
- Completeness and consistency checks
- Testability checks for acceptance criteria
- Review notes and gap reporting

## Process Routing (quick map)
- New requirement intake -> BA Agent first
- If BA output incomplete -> stop and fix BA outputs
- BA outputs ready -> UXUI Agent
- UXUI output ready -> FE Agent
- FE output ready -> Reviewer/validators

## Stage Routing
- clarification stage -> BA Agent
- ba-core stage -> BA Agent
- design stage -> UXUI Agent
- fe-prototype stage -> FE Agent
- review stage -> Reviewer / validators

## Output Routing
- BA writes analysis artifacts in requirement output folder
- UXUI writes `wireframe.md`
- FE writes `ui.html`
- Reviewer writes `review-notes.md`

<!-- TODO: Add a simple decision table for mixed requests (analysis + UI + risk in one task). -->
