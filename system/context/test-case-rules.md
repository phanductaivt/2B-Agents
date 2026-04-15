# Test Case Rules

## Source Inputs
- FRS main flow, alternative flows, validations, edge cases
- User Story context
- Acceptance Criteria

## Test Case File
- `outputs/generated/<requirement-name>/test-cases.md`
- Matrix includes: TC ID, linked AC/US/FR IDs, scenario, steps, expected result, priority, notes.

## Coverage Types
- Happy Path
- Validation / Negative
- Edge Case
- Error Handling

## Rules
- Every test case has a `TC-###` ID.
- Every test case links to at least one AC ID.
- Prefer linking US and FR IDs too.
- Keep steps practical and testable.
