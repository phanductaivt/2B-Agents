# Context Summary

## System
- Project-based BA-led generation pipeline.
- Inputs and outputs live under `projects/<project-name>/`.
- Main run command: `python3 app.py`.

## Agent Roles
- BA: clarification, BPMN, story, AC, BRD, FRS, feature list.
- UXUI: wireframe from FRS.
- FE: HTML from FRS + wireframe.
- Reviewer: quality and consistency checks.

## Workflow
- Input -> BA -> UXUI -> FE -> review
- Generate outputs, tests, and traceability
- Update `status.md`, project flow, dashboard markdown/html

## IDs
- REQ/BRD/FR/US/AC/FEAT/UI/RV/TC
- Stored in `id-registry.yaml`
- Requirement file includes `Requirement ID` header
- IDs appear in outputs and traceability

## Traceability
- Requirement-level matrix and Mermaid flow
- Project-level summary
- Chain: Requirement -> BRD -> FRS -> US -> AC -> Feature -> Wireframe -> UI -> Review -> Test Cases
