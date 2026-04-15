# Artifact Model

This file supports safe context sync using AUTO-SYNC markers.

<!-- AUTO-SYNC:START -->
## Level 1 Auto-Synced Artifact Model

### Stage Mapping
- `clarification`: clarification
- `ba-core`: brd, process-bpmn, frs, user-story, acceptance-criteria, feature-list
- `design`: wireframe
- `fe-prototype`: ui
- `review`: review, test-cases, requirement-traceability-matrix, requirement-traceability-flow, risk-notes, dependency-map

### Artifact Catalog Summary

| Artifact | Stage | Owner | Dependencies | Outputs | Gate Required |
|---------|-------|-------|--------------|---------|---------------|
| clarification | clarification | ba-agent | None | clarification.md | True |
| brd | ba-core | ba-agent | clarification | brd.md | True |
| process-bpmn | ba-core | ba-agent | clarification | process-bpmn.md | True |
| frs | ba-core | ba-agent | clarification, brd, process-bpmn | frs.md | True |
| user-story | ba-core | ba-agent | clarification, frs | user-story.md | True |
| acceptance-criteria | ba-core | ba-agent | user-story, frs | acceptance-criteria.md | True |
| feature-list | ba-core | ba-agent | frs | feature-list.md | True |
| wireframe | design | uxui-agent | frs, feature-list | wireframe.md | True |
| ui | fe-prototype | fe-agent | frs, wireframe | ui.html | True |
| review | review | reviewer-agent | ui, wireframe, frs | review-notes.md | True |
| test-cases | review | reviewer-agent | frs, user-story, acceptance-criteria | test-cases.md | True |
| requirement-traceability-matrix | review | reviewer-agent | review, test-cases | requirement-traceability-matrix.md | True |
| requirement-traceability-flow | review | reviewer-agent | review, test-cases | requirement-traceability-flow.md | True |
| risk-notes | review | reviewer-agent | review, dependency-map | risk-notes.md | True |
| dependency-map | review | reviewer-agent | frs, feature-list | projects/<project-name>/_ops/dependency-map.md | False |

### Gate and Approval Rules (from system/configs/gates.yaml)

| Artifact | Allowed Gate Results | Allowed Approval States |
|---------|----------------------|-------------------------|
| clarification | Pass, Warning | Approved, In Review |
| brd | Pass, Warning | Approved, In Review |
| process-bpmn | Pass, Warning | Approved, In Review |
| frs | Pass | Approved |
| user-story | Pass, Warning | Approved, In Review |
| acceptance-criteria | Pass, Warning | Approved, In Review |
| feature-list | Pass, Warning | Approved, In Review |
| wireframe | Pass | Approved |
| ui | Pass | Approved |
| review | Pass, Warning, Fail | Approved, In Review, Rework Needed |
| test-cases | Pass, Warning | Approved, In Review |
| requirement-traceability-matrix | Pass, Warning | Approved, In Review |
| requirement-traceability-flow | Pass, Warning | Approved, In Review |
| risk-notes | Pass, Warning, Fail | Approved, In Review, Rework Needed |
| dependency-map | Pass, Warning, Fail | Approved, In Review, Rework Needed |

<!-- TODO: Add lightweight artifact-level quality score when needed. -->
<!-- AUTO-SYNC:END -->
