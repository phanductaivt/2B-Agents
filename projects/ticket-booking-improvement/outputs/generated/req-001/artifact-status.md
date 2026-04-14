# Artifact Status

## Overview
- Project Name: ticket-booking-improvement
- Requirement Name: req-001
- Requirement ID: REQ-001
- Last Updated: 2026-04-15

## Artifact Table

| Artifact | Stage | Owner | Status | Dependencies | Gate | Notes |
|---------|------|------|--------|-------------|------|------|
| clarification | clarification | BA | Done | None | Pass | Artifact quality check passed. |
| brd | ba-core | BA | Done | clarification | Pass | Artifact quality check passed. |
| process-bpmn | ba-core | BA | Done | clarification | Pass | Artifact quality check passed. |
| frs | ba-core | BA | Done | clarification, brd, process-bpmn | Pass | Artifact quality check passed. |
| user-story | ba-core | BA | Done | clarification, frs | Pass | Artifact quality check passed. |
| acceptance-criteria | ba-core | BA | Done | user-story, frs | Pass | Artifact quality check passed. |
| feature-list | ba-core | BA | Done | frs | Pass | Artifact quality check passed. |
| wireframe | design | UXUI | Done | frs, feature-list | Pass | Artifact quality check passed. |
| ui | fe-prototype | FE | Done | frs, wireframe | Pass | Artifact quality check passed. |
| review | review | REVIEWER | Done | ui, wireframe, frs | Pass | Artifact quality check passed. |
| test-cases | review | REVIEWER | Done | frs, user-story, acceptance-criteria | Pass | Artifact quality check passed. |
| requirement-traceability-matrix | review | REVIEWER | Done | review, test-cases | Pass | Artifact quality check passed. |
| requirement-traceability-flow | review | REVIEWER | Done | review, test-cases | Pass | Artifact quality check passed. |
| risk-notes | review | REVIEWER | Done | review, dependency-map | Pass | Artifact quality check passed. |
| dependency-map | review | REVIEWER | Done | frs, feature-list | Pass | Artifact quality check passed. |

Suggested status values:
- Not Started
- In Progress
- Done
- In Review
- Blocked
- Rework Needed

Suggested gate values:
- Pass
- Warning
- Fail
- Not Allowed
- N/A

<!-- TODO: Add optional approval column when the governance model requires explicit sign-off. -->
