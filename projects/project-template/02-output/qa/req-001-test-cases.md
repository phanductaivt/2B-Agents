---
file_type: "Sample QA Artifact"
primary_agents: ["QA"]
supporting_agents: ["BA", "BE", "FE"]
activation_mode: "Reference Sample"
lifecycle_stage: "Project Sample Output"
purpose: "Show the expected quality and structure of the QA artifact for test cases."
---
# Requirement: req-001

# Test Cases: Ticket Booking Modification Improvement

- Test Case Set ID: `TC-001`
- Parent Scenario Set ID: `TS-001`

## Test Case 1

- Test Case ID: `TC-001-01`
- Scenario ID: `TS-001-01`
- Objective: Verify eligible booking change happy path
- Priority: High

### Preconditions

- customer is signed in
- booking belongs to the customer
- booking is eligible for online change
- fee service is available

### Steps

1. Open the booking change page for the selected booking.
2. Review the eligibility result.
3. Load change options.
4. Select one valid change option.
5. Review the fee summary before confirmation.

### Expected Result

- the page shows the booking as eligible
- one or more valid change options are visible
- the fee summary shows fare difference, change fee, and total due before confirmation

### Evidence / Execution Record

- Evidence to capture: screenshot of the eligible flow with the fee summary visible, or API/browser response showing quote data.
- Actual result: not run in this QA artifact; runnable verification is recorded separately under `02-output/release/`.
- Status: `not-run`

### Automation Candidate

- Automation level: `ui-e2e`
- Automation priority: High
- Automation notes: automate after stable booking seed data and selector IDs exist.

### Tracking Verification

- Event/action: `booking_change_started`, `booking_change_eligibility_returned`, `booking_change_fee_viewed`
- Verification method: confirm the fee-view event fires only after fare difference, change fee, and total due are visible.

## Test Case 2

- Test Case ID: `TC-001-02`
- Scenario ID: `TS-001-02`
- Objective: Verify ineligible booking fallback behavior
- Priority: High

### Preconditions

- customer is signed in
- booking belongs to the customer
- booking is not eligible for online change

### Steps

1. Open the booking change page for the selected booking.
2. Wait for eligibility evaluation to complete.

### Expected Result

- the page shows that online change is not allowed
- a rejection reason is shown
- support guidance is shown
- change options are not displayed

### Evidence / Execution Record

- Evidence to capture: screenshot of the fallback message and response payload with rejection reason.
- Actual result: not run in this QA artifact.
- Status: `not-run`

### Automation Candidate

- Automation level: `ui-e2e`
- Automation priority: High
- Automation notes: requires an ineligible booking fixture and stable rejection reason categories.

### Tracking Verification

- Event/action: `booking_change_eligibility_returned`, `booking_change_support_fallback_shown`
- Verification method: confirm fallback event includes `fallback_reason` and `eligibility_status`.

## Test Case 3

- Test Case ID: `TC-001-03`
- Scenario ID: `TS-001-03`
- Objective: Verify unauthorized booking access is blocked
- Priority: Critical

### Preconditions

- customer is signed in
- selected booking belongs to a different customer

### Steps

1. Attempt to open the booking change page for the other customer's booking.

### Expected Result

- access is blocked
- booking details are not shown
- an authorization message is returned or displayed

### Evidence / Execution Record

- Evidence to capture: API response or screenshot proving another customer's booking details are not exposed.
- Actual result: not run in this QA artifact.
- Status: `not-run`

### Automation Candidate

- Automation level: `api-test`
- Automation priority: Critical
- Automation notes: automate once authentication and ownership fixtures exist; current local demo does not implement real ownership checks.

### Tracking Verification

- Event/action: none expected for sensitive denied access unless security logging is approved.
- Verification method: confirm no customer or passenger data appears in denied response.

## Test Case 4

- Test Case ID: `TC-001-04`
- Scenario ID: `TS-001-04`
- Objective: Verify fee service failure stops the flow safely
- Priority: High

### Preconditions

- customer is signed in
- booking belongs to the customer
- booking is eligible for online change
- fee service is unavailable

### Steps

1. Open the booking change page.
2. Load change options.
3. Attempt to review pricing for a selected option.

### Expected Result

- pricing does not load successfully
- the flow does not continue to confirmation
- a fallback or retry guidance message is shown

### Evidence / Execution Record

- Evidence to capture: mocked fee-service failure response and screenshot of retry/fallback guidance.
- Actual result: not run in this QA artifact.
- Status: `not-run`

### Automation Candidate

- Automation level: `ui-e2e`
- Automation priority: High
- Automation notes: automate with a mock or test flag that forces fee-service failure.

### Tracking Verification

- Event/action: `booking_change_support_fallback_shown`
- Verification method: confirm fallback event separates technical failure from policy ineligibility.

## Test Case 5

- Test Case ID: `TC-001-05`
- Scenario ID: `TS-001-05`
- Objective: Verify zero-fee changes still require confirmation
- Priority: Medium

### Preconditions

- customer is signed in
- booking belongs to the customer
- selected option returns zero fee and zero or acceptable fare difference

### Steps

1. Open the booking change page.
2. Select a valid zero-fee change option.
3. Review the quote.

### Expected Result

- the quote shows zero change fee
- the user still sees a distinct confirmation step before continuation

### Evidence / Execution Record

- Evidence to capture: screenshot showing zero fee and visible confirmation step before final submit.
- Actual result: not run in this QA artifact.
- Status: `not-run`

### Automation Candidate

- Automation level: `ui-e2e`
- Automation priority: Medium
- Automation notes: automate after a stable zero-fee option fixture exists.

### Tracking Verification

- Event/action: `booking_change_fee_viewed`
- Verification method: confirm fee event has `fee_available` and fee bucket behavior agreed with analytics policy.

## Notes

- Payment submission itself is not covered because that slice is still intentionally deferred.
