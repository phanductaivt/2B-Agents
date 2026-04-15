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
- Update `_ops/status.md`, project flow, dashboard markdown/html
- Scenario defaults are loaded from `system/scenarios/` (catalog + YAML files)

## IDs
- REQ/BRD/FR/US/AC/FEAT/UI/RV/TC
- Stored in `_ops/runtime/id-registry.yaml`
- Requirement file includes `Requirement ID` header
- IDs appear in outputs and traceability

## Traceability
- Requirement-level matrix and Mermaid flow
- Project-level summary
- Chain: Requirement -> BRD -> FRS -> US -> AC -> Feature -> Wireframe -> UI -> Review -> Test Cases

<!-- AUTO-SYNC:START -->
## Level 1 Auto-Synced Summary

### Current System Snapshot
- Project-based pipeline under `projects/<project-name>/...`.
- BA-led artifact generation with UXUI, FE, and Reviewer stages.
- Artifact count: 15.
- Stages: clarification, ba-core, design, fe-prototype, review.

### Execution Model
- Full mode: generate all artifacts in dependency order.
- Controlled mode: run by artifact/stage with gate + approval checks.
- Governance files per requirement:
  - `artifact-status.md`
  - `artifact-checklist.md`
  - `gate-results.md`
  - `gate-report.md`
  - `artifact-reviews/*.md`

### Gate and Approval Model
- Gate states: Pass, Warning, Fail, Not Allowed.
- Approval states: Draft, In Review, Approved, Rework Needed, Blocked.
- Downstream execution depends on both gate and approval rules in `system/configs/gates.yaml`.

### Quick Links
- [artifact-model.md](./artifact-model.md)
- [workflow-playbook.md](./workflow-playbook.md)
- [load-profiles.md](./load-profiles.md)
- [output-standards.md](./output-standards.md)
- [id-system.md](./id-system.md)

<!-- TODO: Add sample command snippets for common controlled-run cases. -->
<!-- AUTO-SYNC:END -->
