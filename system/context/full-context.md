# Full Context

## Included Sections
- system-overview
- architecture
- agent-design
- workflow-playbook
- output-standards
- traceability-rules
- id-system
- test-case-rules
- versioning-rules
- dependency-rules
- risk-rules

## System Overview
- BA-led project pipeline for requirement processing.
- Generates analysis, design, FE, review, tests, and traceability outputs.
- Updates status and dashboards automatically.

## Architecture
- Real work is project-based under `projects/<project-name>/`.
- `app.py` orchestrates scanning, generation, and updates.
- `system/tools/project/` contains focused helper managers.

## Agent Design
- BA creates primary business and functional artifacts.
- UXUI depends on FRS.
- FE depends on FRS + wireframe.
- Reviewer checks quality and consistency.

## Workflow
- Input -> BA -> UXUI -> FE -> Review -> Outputs -> Status -> Dashboard.
- Skip existing outputs by default; `--force` regenerates.

## Output Standards
- Markdown-first outputs plus one HTML output.
- Requirement-level and project-level flow/traceability docs are generated.
- Test case matrix generated per requirement.

## Traceability Rules
- Explicit ID-based mapping, not file checkmarks only.
- Requirement matrix + flow + project summary maintained.

## ID System
- Zero-padded IDs: REQ/BRD/FR/US/AC/FEAT/UI/RV/TC.
- IDs stored in `id-registry.yaml`.
- Requirement header ID is ensured in input files.

## Test Case Rules
- Test cases generated from FRS + AC + story context.
- Coverage categories: happy path, negative, edge, error handling.
- TC links to AC/US/FR IDs.

## Versioning Rules
- Current baseline uses file outputs and run logs.
- Recommended future files: `version-info.md` and `change-log.md`.

## Dependency Rules
- FRS blocks/unblocks downstream UXUI and FE work.
- Downstream outputs should not proceed when required upstream artifacts are missing.

## Risk Rules
- Risk categories: scope, clarity, dependency, delivery, quality.
- Severity: High/Medium/Low.
- Inputs: blockers, validators, missing outputs, traceability gaps.
