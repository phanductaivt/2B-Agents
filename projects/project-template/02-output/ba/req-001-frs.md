---
file_type: "Sample BA Artifact"
primary_agents: ["BA"]
supporting_agents: ["PO"]
activation_mode: "Reference Sample"
lifecycle_stage: "Project Sample Output"
purpose: "Show the expected quality and structure of the BA artifact for frs."
---
# Requirement: req-001

# FRS: Ticket Booking Modification Improvement

- FR ID: `FR-001`
- Parent REQ ID: `REQ-001`
- Parent BRD ID: `BRD-001`

## Functional Summary
The portal must guide customers through booking change eligibility, fees, and next steps.

## Actors
- customer
- booking rules service
- fee calculation service

## Functional Requirements
- `FR-1` The customer can open the booking change page for their own booking.
- `FR-2` The system checks whether the selected booking is eligible for online change.
- `FR-3` The system shows available change options and the related fee before confirmation.
- `FR-4` The system shows support guidance when the booking is not eligible for online change.
- `FR-5` The system blocks access to another customer's booking.

## Main Flow
1. Customer opens the booking change page.
2. System loads the selected booking and validates ownership.
3. System checks whether the booking is eligible for online change.
4. System shows the allowed change options and related fee details.
5. Customer reviews the fee and confirms the selected change.
6. System proceeds to the next approved booking update step.

## Alternative Flows
- If the booking is not eligible, show the reason and support guidance instead of change options.
- If the fee service cannot be loaded, show a fallback message and stop the change flow.
- If the change fee is zero, still show the confirmation step before the change continues.
- If the booking does not belong to the customer, block access and show an authorization message.

## Business Rules
- Only eligible tickets can be changed online.
- The customer must see change fees before confirming the update.
- Refund or reissue steps must follow approved fare rules and channel policy.
- If online change is not allowed, the portal must guide the customer to support.

## Validations
- Only valid change options for the selected booking are shown.
- Fee details appear before the customer can confirm.
- The page never exposes another customer's booking data.

## Edge Cases
- Booking not eligible for online change.
- Fee or rules service unavailable.
- Zero fee change still needs confirmation.
- Unauthorized booking access attempt.

## Dependencies
- Booking rules service is available.
- Fee calculation service is available.
- Fare and channel policy wording is approved.

## Open Questions
- Is payment collection part of the first slice when a positive fare difference exists?
- Which rejection reasons must be visible to customers in the first release?
