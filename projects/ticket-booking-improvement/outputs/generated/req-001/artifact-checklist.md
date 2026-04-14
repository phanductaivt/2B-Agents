# Artifact Checklist

- Requirement Name: req-001
- Requirement ID: REQ-001

## clarification.md
- [ ] Purpose reviewed: Clarify the requirement and list assumptions/questions.
- [ ] Dependencies reviewed: None
- [ ] Quality check completed
- [ ] Approval decision recorded in artifact-status.md

## process-bpmn.md
- [ ] Purpose reviewed: Show business flow in Mermaid.
- [ ] Dependencies reviewed: clarification.md
- [ ] Quality check completed
- [ ] Approval decision recorded in artifact-status.md

## user-story.md
- [ ] Purpose reviewed: Describe user value and scope in story format.
- [ ] Dependencies reviewed: clarification.md
- [ ] Quality check completed
- [ ] Approval decision recorded in artifact-status.md

## acceptance-criteria.md
- [ ] Purpose reviewed: Define testable acceptance conditions.
- [ ] Dependencies reviewed: user-story.md
- [ ] Quality check completed
- [ ] Approval decision recorded in artifact-status.md

## brd.md
- [ ] Purpose reviewed: Document business goals, scope, and rules.
- [ ] Dependencies reviewed: clarification.md
- [ ] Quality check completed
- [ ] Approval decision recorded in artifact-status.md

## frs.md
- [ ] Purpose reviewed: Document functional behavior, flows, and edge cases.
- [ ] Dependencies reviewed: brd.md, process-bpmn.md
- [ ] Quality check completed
- [ ] Approval decision recorded in artifact-status.md

## feature-list.md
- [ ] Purpose reviewed: Show hierarchical feature decomposition.
- [ ] Dependencies reviewed: frs.md
- [ ] Quality check completed
- [ ] Approval decision recorded in artifact-status.md

## wireframe.md
- [ ] Purpose reviewed: Provide UX structure based on FRS/feature scope.
- [ ] Dependencies reviewed: frs.md, feature-list.md
- [ ] Quality check completed
- [ ] Approval decision recorded in artifact-status.md

## ui.html
- [ ] Purpose reviewed: Provide FE demo implementation.
- [ ] Dependencies reviewed: frs.md, wireframe.md
- [ ] Quality check completed
- [ ] Approval decision recorded in artifact-status.md

## review-notes.md
- [ ] Purpose reviewed: Record quality review issues and next actions.
- [ ] Dependencies reviewed: frs.md, wireframe.md, ui.html
- [ ] Quality check completed
- [ ] Approval decision recorded in artifact-status.md

## test-cases.md
- [ ] Purpose reviewed: Provide test scenarios linked to AC/US/FR.
- [ ] Dependencies reviewed: frs.md, user-story.md, acceptance-criteria.md
- [ ] Quality check completed
- [ ] Approval decision recorded in artifact-status.md

<!-- TODO: Add role-based approval checklist (BA lead / reviewer) if the team needs it. -->
