# Output Checklists

Use these quick checks before marking an output as done.

## BRD Checklist
- [ ] Linked `REQ-ID` is shown.
- [ ] Business goal and scope are clear.
- [ ] Stakeholders and impacted users are listed.
- [ ] Key business rules are included.
- [ ] Out-of-scope items are stated.

## FRS Checklist
- [ ] Linked `REQ-ID` and `BRD-ID` are shown.
- [ ] Main flow is complete and ordered.
- [ ] Alternative/exception flows are included.
- [ ] Functional rules are specific and testable.
- [ ] Input/output behavior is clear.

## User Story Checklist
- [ ] Story follows: role, goal, value.
- [ ] Linked `US-ID` and parent `FR-ID` are shown.
- [ ] Story is small enough to deliver (not too broad).
- [ ] Story value is clear for business/user.

## Acceptance Criteria Checklist
- [ ] Linked `AC-ID` and parent `US-ID` are shown.
- [ ] Criteria are testable and unambiguous.
- [ ] Positive and negative conditions are covered.
- [ ] No vague words (fast, easy, normal, etc.).

## Feature List Checklist
- [ ] Linked `FEAT-ID` and parent `FR-ID` are shown.
- [ ] Level 1/2/3 hierarchy is clear.
- [ ] No duplicate or overlapping features.
- [ ] Feature names are short and specific.

## Test Cases Checklist
- [ ] Every test case has `TC-ID`.
- [ ] Each case links to at least one `AC-ID`.
- [ ] `US-ID`/`FR-ID` links are included when possible.
- [ ] Includes happy path, negative, and edge coverage.
- [ ] Steps and expected results are measurable.

## RTM Checklist
- [ ] `REQ -> BRD -> FR -> US -> AC -> FEAT -> UI -> RV -> TC` links are visible.
- [ ] Missing links are marked clearly.
- [ ] Status is set as `Complete`, `Partial`, or `Missing`.
- [ ] Notes explain any gap and next action.

## Gate Control Checklist
- [ ] Upstream artifact gates are checked before running downstream.
- [ ] Upstream approval state is checked before running downstream.
- [ ] `gate-results.md` is updated for each artifact run.
- [ ] Blocked downstream artifacts are marked `Not Allowed`.
- [ ] Gate warnings/failures include a practical reason and next action.
- [ ] Any `--override-gate` usage is documented in notes.

<!-- TODO: Add a compact scoring model (Ready / Needs Fix) for each checklist. -->
