# Completeness Checker

## Name

Completeness Checker

## Purpose

Check whether a Markdown document includes the sections needed for a useful BA-led review.

## What To Check

- problem statement
- business goal
- scope
- user impact
- dependencies or assumptions
- expected sections in `clarification.md`, `process-bpmn.md`, `user-story.md`, `acceptance-criteria.md`, `brd.md`, and `frs.md`
- expected sections in `feature-list.md`
- business rules such as approvals, allowed statuses, exception rules, validation rules, or scope limits
- whether missing business rules are clearly called out as open questions when they are not yet known
- whether FRS includes a clear main flow and alternative flows
- whether FRS includes realistic edge cases such as missing data, invalid state, unsupported state, or service unavailability
- whether `feature-list.md` exists when feature structuring is part of the request
- whether acceptance criteria are written in Given/When/Then or another clearly testable format

## Pass/Fail Logic

- pass: all key sections are present or clearly marked as unknown
- fail: important sections or business rules are missing with no note or follow-up action

## Example Issues

- PRD has no success measure
- story has no business value
- requirement has no named user or stakeholder
- acceptance criteria mention status updates but never say which statuses are allowed
- approval flow is referenced but no approval rule is explained
- FRS lists happy-path functions only and ignores invalid or missing status scenarios
- FRS is missing main flow or alternative flow sections
- feature hierarchy is missing even though downstream UXUI and FE outputs depend on it
