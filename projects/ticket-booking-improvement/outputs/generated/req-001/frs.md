# FRS: Ticket Booking Modification Improvement

- FR ID: `FR-001`
- Parent REQ ID: `REQ-001`
## Functional Summary
The portal must guide the customer through booking change eligibility, fees, and next steps.

## Actors
- customer
- business service

## Functional Requirements
- FR-1: The customer can open the booking change page and review eligibility for the selected booking.
- FR-2: The system displays allowed change options and the related fee before confirmation.
- FR-3: The page displays support or refund guidance when the booking is not eligible for online change.
- FR-4: The page prevents the customer from seeing or changing another customer's booking.

## Main Flow
- Customer opens the booking change page.
- System checks eligibility for the selected booking.
- System shows change options and fees.
- Customer confirms the change.
- System updates the booking and shows the confirmation.

## Alternative Flows
- If the booking is not eligible, show the reason and the support or refund path.
- If fare rules cannot be loaded, show a fallback message and stop the change flow.
- If the fee is zero, still show a clear confirmation step before updating.

## Business Rules
- Only eligible tickets can be changed online.
- The customer must see change fees before confirming the update.
- Refund or reissue steps must follow approved fare rules and channel policy.
- If online change is not allowed, the portal must guide the customer to support.
- Change eligibility must be checked against the latest fare and ticket rules.
- If a booking is not eligible, the system must show the reason and the next support path.

## Validations
- Show only valid change options for the selected booking.
- Show fee information before final confirmation.
- Do not show another customer's booking details.

## Edge Cases
- If the booking is not eligible for online change, display the reason and the next support path.
- If fare rules cannot be loaded, show a fallback message instead of invalid fee data.
- If the change fee is zero, still show a clear confirmation step.
- If the selected booking does not belong to the customer, do not display modification options.

## Dependencies
- Booking rules service is available.
- Fare rules and refund rules are approved by business stakeholders.

## Open Questions
- Are there any approvals, exceptions, or out-of-scope cases to capture?
