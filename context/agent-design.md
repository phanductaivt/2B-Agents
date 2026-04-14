# Agent Design

## BA Agent
- Clarifies requirement and drafts analysis outputs.
- Produces: `clarification.md`, `process-bpmn.md`, `user-story.md`, `acceptance-criteria.md`, `brd.md`, `frs.md`, `feature-list.md`.
- Primary source for UXUI and FE downstream work.

## UXUI Agent
- Uses BA FRS and feature context.
- Produces: `wireframe.md`.

## FE Agent
- Uses BA FRS plus UXUI wireframe.
- Produces: `ui.html`.

## Reviewer / Validators
- Checks ambiguity, completeness, consistency, template fit.
- Produces: `review-notes.md`.
- Supports traceability and readiness checks.
