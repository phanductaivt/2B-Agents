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

## Stage Model
- `clarification`: clarification
- `ba-core`: brd, process-bpmn, frs, user-story, acceptance-criteria, feature-list
- `design`: wireframe
- `fe-prototype`: ui
- `review`: review, test-cases, requirement-traceability-matrix, requirement-traceability-flow, risk-notes, dependency-map

Stage usage:
- Use full run for fast baseline package generation.
- Use stage run when you want controlled quality checks per stage.
- Use artifact run when one file needs focused refinement.

## Step Flow
1. Read `projects/<project-name>/inputs/requirements/<file>.md`
2. Assign requirement and artifact IDs
3. Generate BA package
4. Generate UXUI wireframe
5. Generate FE HTML
6. Generate test cases
7. Generate traceability files
8. Update `status.md`
9. Update project flow files
10. Update `projects/dashboard.md` and `projects/dashboard.html`

## Skip/Force Rule
- If output folder exists: skip by default.
- Use `--force` to regenerate.

## Controlled Governance Files
- `artifact-status.md`
- `artifact-checklist.md`
- `gate-report.md`
