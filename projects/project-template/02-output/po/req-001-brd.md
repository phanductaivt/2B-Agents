---
file_type: "Sample PO Artifact"
primary_agents: ["PO"]
supporting_agents: ["BA"]
activation_mode: "Reference Sample"
lifecycle_stage: "Project Sample Output"
purpose: "Show the expected quality and structure of a PO-owned BRD output."
---
# Requirement: req-001

# BRD: Ticket Booking Modification Improvement

- BRD ID: `BRD-001`
- Parent REQ ID: `REQ-001`

## Business Problem
Customers contact support because they cannot clearly understand whether a booking can be changed online, what the change will cost, or what to do next when online change is not allowed.

## Business Objective
Reduce avoidable booking-change support contacts by giving web customers a clearer self-service first slice for eligibility, fee visibility, and next-step guidance.

## Stakeholders
- Customer
- Product Owner
- Support Team
- Business Operations

## BACCM Framing

### Change
Move common booking change understanding from assisted support to a clearer self-service web experience.

### Need
Customers lack confidence and clarity around booking change eligibility, fees, and next steps, which increases avoidable support demand.

### Solution
Provide a first-slice self-service booking change flow that shows eligibility, fee visibility, and guidance when online change cannot continue.

### Value
- Fewer avoidable support contacts
- Better customer understanding before a booking change decision
- Stronger alignment between product intent and downstream delivery

### Context
- The first release is web-only.
- Fare and channel policy constrain what can be changed online.
- Some decisions still depend on whether payment collection is part of the first slice.

## Scope

### In Scope
- Web customer booking change entry point
- Eligibility check visibility
- Change option visibility
- Fee visibility before confirmation
- Guidance when online change is not allowed

### Out Of Scope
- Full refund workflow
- Call-center operating procedure redesign
- Native mobile-specific journey

## Requirement Classification

### Business Requirements
- Reduce avoidable booking-change support contacts.
- Improve customer understanding of booking change eligibility and cost before confirmation.

### Stakeholder Requirements
- Customers need to know whether their booking can be changed online.
- Support teams need fewer avoidable contacts about basic booking change eligibility and fee visibility.
- Product stakeholders need a narrow first slice that can be reviewed and released safely.

### Solution Requirements
- The product must show whether a booking is eligible for online change.
- The product must show available change options and fees before confirmation.
- The product must guide customers when online change is not allowed.

### Transition Requirements
- Customer-visible rejection wording must be approved.
- Fare and channel policy wording must be aligned with the web experience.
- The team must confirm whether payment collection is part of release one.

## Market Context

### Observed Market Signals
- Airline and travel self-service flows commonly show eligibility and fee visibility before final confirmation.
- Customers generally expect self-service modification clarity before they decide whether to continue or contact support.

### Inference
- If the product hides eligibility or fee information too late, customers are more likely to abandon the self-service path and contact support.

### Recommendation
- Prioritize clarity and guidance in the first slice before adding broader exception handling depth.

## Business Rules
- Only eligible tickets can be changed online.
- The customer must see change fees before confirming the update.
- Refund or reissue steps must follow approved fare rules and channel policy.
- If online change is not allowed, the portal must guide the customer to support.

## Success Measures
- A measurable reduction target for avoidable support contacts is still missing and must be confirmed.
- Customers can see eligibility and fee information before deciding whether to continue.

## Priority / Tradeoff Notes
- First release favors clarity and guidance over broad exception-handling depth.
- If payment collection for a positive fare difference is not ready, fee visibility still remains a priority for the first slice.

## Assumptions
- The first release is web-only.
- Refund and reissue policy wording already exists outside this repository.

## Expected Benefits
- Fewer avoidable booking-change support contacts.
- Better customer understanding of booking change eligibility and cost.

## Open Questions
- Is payment collection included in the first slice when the fare difference is positive?
- Which rejection reasons must be shown directly to customers?
