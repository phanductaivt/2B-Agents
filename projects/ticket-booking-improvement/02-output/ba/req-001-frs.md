# Requirement: req-001

# FRS: Ticket Booking Modification Improvement

- FR ID: `FR-001`
- Parent REQ ID: `REQ-001`
## Functional Summary
The portal must guide customers through booking change eligibility, fees, and next steps.

## Actors
- customer
- business service

## Functional Requirements
- {'FR-1': 'User can open booking change page and review eligibility.'}
- {'FR-2': 'System displays allowed change options and related fee before confirmation.'}
- {'FR-3': 'Page displays support/refund guidance when booking is not eligible.'}
- {'FR-4': "Page blocks access to another customer's booking."}

## Main Flow
- Customer opens booking change page.
- System checks change eligibility for selected booking.
- System shows available change options and fee.
- Customer confirms change.
- System updates booking and displays confirmation.

## Alternative Flows
- If booking is not eligible, show reason and support/refund path.
- If fare rules cannot be loaded, show fallback message and stop change flow.
- If change fee is zero, still show final confirmation step.

## Business Rules
- Only eligible tickets can be changed online.
- The customer must see change fees before confirming the update.
- Refund or reissue steps must follow approved fare rules and channel policy.
- If online change is not allowed, the portal must guide the customer to support.
- Show change fees before final confirmation.
- Refund or reissue steps must follow approved fare rules.
- Show ineligibility reason and next support path when change is not allowed.

## Validations
- Show only valid options for selected booking.
- Show fee details before confirmation.
- Do not expose another customer's booking data.

## Edge Cases
- Booking not eligible for online change.
- Fare rules service unavailable.
- Zero fee change still needs confirmation.
- Unauthorized booking access attempt.

## Dependencies
- Booking rules service is available.
- Fare/refund policy is approved.

## Open Questions
- Are there any approvals, exceptions, or out-of-scope cases to capture?
