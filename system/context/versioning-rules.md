# Versioning Rules

## Current State
- Versioning is file-based and project-based.
- Project-level log: `projects/<project-name>/_ops/change-log.md`
- Requirement-level file: `projects/<project-name>/_ops/generated/<requirement-name>/version-info.md`

## Version Increment Rule
- First generation of one requirement package: `v1.0`
- Regeneration with meaningful output changes: `v1.1`, `v1.2`, ...
- Larger structural changes (for example BRD + FRS + Feature List updated together): move to next major such as `v2.0`

## What To Track
- Date
- Scope
- Summary of changes
- Affected requirement(s)
- Reason
- Impacted IDs (`REQ`, `BRD`, `FR`, `US`, `AC`, `FEAT`, `UI`, `RV`, `TC`)

## Key Artifact Change Tracking
- `brd.md`
- `frs.md`
- `user-story.md`
- `acceptance-criteria.md`
- `feature-list.md`
- `wireframe.md`
- `ui.html`
- `test-cases.md`
- `review-notes.md`

<!-- TODO: Add optional auto-snapshot to _ops/generated/<requirement-name>/history/ when strict audit storage is required. -->
