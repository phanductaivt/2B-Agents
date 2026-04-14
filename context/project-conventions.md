# Project Conventions

Use these conventions to keep projects consistent and easy to manage.

## Project Folder Naming
- Format: lowercase + hyphen, for example `ticket-booking-improvement`.
- One project folder per business initiative.

## Project Structure
- Use only: `projects/<project-name>/...`
- Required files:
  - `README.md`
  - `project-config.yaml`
  - `status.md`
  - `decision-log.md`
  - `task-tracker.md`
- Required folders:
  - `inputs/requirements/`
  - `inputs/meeting-notes/`
  - `inputs/raw/`
  - `outputs/generated/`
  - `knowledge/`

## Input File Naming
- Requirements: `req-001.md`, `req-002.md`
- Meeting notes: `meeting-001.md`
- Raw notes: `raw-001.txt`

## Output Folder Naming
- One output folder per requirement:
  - `outputs/generated/req-001/`
- Keep file names standard:
  - `clarification.md`
  - `process-bpmn.md`
  - `user-story.md`
  - `acceptance-criteria.md`
  - `brd.md`
  - `frs.md`
  - `feature-list.md`
  - `wireframe.md`
  - `ui.html`
  - `review-notes.md`
  - `test-cases.md`

## ID Conventions
- Zero-padded IDs:
  - `REQ-001`, `BRD-001`, `FR-001`, `US-001`, `AC-001`, `FEAT-001`, `UI-001`, `RV-001`, `TC-001`
- IDs are unique within each project.
- Keep ID source of truth in `id-registry.yaml`.

<!-- TODO: Add a simple naming lint checklist for CI/local pre-check. -->
