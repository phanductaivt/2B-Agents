# Workflow Playbook

## Standard Pipeline
- Input requirement read
- BA generation
- UXUI generation
- FE generation
- Review/validation
- Output write
- Status update
- Dashboard update

## Execution Modes
- Full mode: generate full package in one run.
- Controlled mode: generate one artifact at a time with dependency gates.

## Stage Grouping
- `clarification`: clarification
- `ba-core`: brd, process-bpmn, frs, user-story, acceptance-criteria, feature-list
- `design`: wireframe
- `fe-prototype`: ui
- `review`: review, test-cases, requirement-traceability-matrix, requirement-traceability-flow, risk-notes, dependency-map

## Step Flow
1. Read `projects/<project-name>/01-input/requirements/<file>.md`
2. Assign requirement and artifact IDs
3. Resolve scenario from project config and scenario catalog
4. Generate BA package
5. Generate UXUI wireframe
6. Generate FE HTML
7. Generate test cases
8. Generate traceability files
9. Update `_ops/status.md`
10. Update project flow files
11. Update `workspace/dashboard.md` and `workspace/dashboard.html`

## Skip/Force Rule
- Input hash in `_ops/runtime/processing-state.yaml` decides:
  - new or changed -> process
  - unchanged -> skip
- Use `--force` to regenerate.

## Controlled Governance Files
- `artifact-status.md`
- `artifact-checklist.md`
- `gate-results.md`
- `gate-report.md`
- `artifact-reviews/*.md`

<!-- AUTO-SYNC:START -->
## Level 1 Auto-Synced Playbook View

### High-Level Project Flow
1. Read requirement input from `projects/<project-name>/01-input/requirements/`.
2. Run BA artifacts.
3. Run UXUI artifact (`wireframe`).
4. Run FE artifact (`ui`).
5. Run review/quality artifacts.
6. Write outputs to `projects/<project-name>/_ops/generated/<requirement-name>/` and curated copies in `02-output/`.
7. Update project status and dashboards.

### Stage Flow (from artifact catalog)
- `clarification`: clarification
- `ba-core`: brd, process-bpmn, frs, user-story, acceptance-criteria, feature-list
- `design`: wireframe
- `fe-prototype`: ui
- `review`: review, test-cases, requirement-traceability-matrix, requirement-traceability-flow, risk-notes, dependency-map

### Artifact Execution Logic
- Full run mode uses dependency order.
- Controlled run mode supports `--artifact` and `--stage`.
- Existing outputs can be skipped unless `--force` is used.

### Gate-Aware Flow
- Before each artifact, dependency gate and approval are checked.
- If not allowed, artifact is marked blocked/not allowed.
- Optional `--override-gate` allows manual continuation with notes.

<!-- TODO: Add a compact visual snippet linking stages to gate checkpoints. -->
<!-- AUTO-SYNC:END -->
