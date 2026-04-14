# Test Cases

## Overview
- Project Name: loyalty-feature-expansion
- Requirement Name: req-001
- Linked Requirement ID: REQ-001
- Last Updated: 2026-04-14

## Test Case Matrix

| TC ID | Linked AC ID | Linked US ID | Linked FR ID | Test Type | Test Scenario | Preconditions | Test Steps | Expected Result | Priority | Notes |
|------|---------------|--------------|--------------|----------|---------------|---------------|------------|-----------------|----------|------|
| TC-002 | AC-001 | US-001 | FR-001 | Happy Path | Complete the main flow successfully | User is allowed to access the feature and has a valid record (booking/member/etc.) | 1. Member opens the loyalty overview page. 2. System loads points, tier progress, and recent activity. 3. System displays the loyalty summary to the member. | The system completes the main flow and shows a clear success outcome. | High | Core scenario based on FRS main flow. |
| TC-003 | AC-001 | US-001 | FR-001 | Validation / Negative | Validation prevents an invalid action | User is on the relevant screen with an invalid input or invalid state. | 1. Trigger the validation condition. 2. Attempt to continue. | The system blocks the action and shows a clear, actionable message. | High | Validation reference: Show only the current member's loyalty data. |
| TC-004 | AC-001 | US-001 | FR-001 | Edge Case | Edge case handling works as expected | User is in a special state that triggers an edge case. | 1. Set up the edge case state. 2. Run the flow step that triggers it. | The system behaves consistently and does not produce confusing results. | Medium | Edge case reference: If loyalty data is delayed, display a clear message instead of blank sections. |
| TC-005 | AC-001 | US-001 | FR-001 | Error Handling | Alternative flow is shown when main flow cannot continue | Main flow is blocked by a known condition. | 1. Trigger the alternative flow condition. 2. Attempt the main flow. | The system routes to the alternative flow and clearly explains next steps. | High | Alternative flow reference: If loyalty data is delayed, show a guidance message and hide incomplete totals. |

<!-- TODO: Expand test case generation to create one TC per acceptance criterion when needed. -->
