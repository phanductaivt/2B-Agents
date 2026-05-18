---
file_type: "Sample BE Artifact"
primary_agents: ["BE"]
supporting_agents: ["BA", "FE"]
activation_mode: "Reference Sample"
lifecycle_stage: "Project Sample Output"
purpose: "Show the expected quality and structure of the backend artifact for BE spec."
---
# Requirement: req-001

# BE Spec: Ticket Booking Modification Improvement

- BE Spec ID: `BE-001`
- Parent BRD ID: `BRD-001`
- Parent FR ID: `FR-001`

## 1. Scope

- Feature: self-service ticket date change
- First-slice boundary: eligibility check, option visibility, fee visibility, confirmation handoff, and support fallback

## 2. BE Responsibilities

- load and validate the selected booking against the current customer
- evaluate online change eligibility using booking rules and fare policy
- return allowed change options for eligible bookings
- calculate fee and fare difference before confirmation
- return support guidance when online change cannot continue

## 3. Core Records Or Entities

- Booking
  - purpose: source record for ownership, itinerary, ticket status, and fare constraints
  - important fields: bookingId, customerId, departureDate, fareRuleCode, channelCode, bookingStatus
- Change Option
  - purpose: candidate travel-date change the customer may choose
  - important fields: optionId, newTravelDate, availabilityState, fareDifference, changeFee
- Change Quote
  - purpose: priced summary returned before customer confirmation
  - important fields: bookingId, selectedOptionId, fareDifference, changeFee, totalDue, currency

## 4. Main Business Actions

### Load Booking Change Context
- trigger: customer opens booking change page
- BE behavior: validate ownership, read booking, and return summary context
- output/result: booking summary plus ability to continue or block

### Evaluate Eligibility
- trigger: booking change context is requested
- BE behavior: apply booking rules and fare policy to determine whether online change is allowed
- output/result: eligibility status plus reason when blocked

### List Change Options
- trigger: booking is eligible
- BE behavior: return allowed date-change options for the selected booking
- output/result: option list the customer can review

### Price Selected Change
- trigger: customer selects a change option
- BE behavior: calculate fare difference and fee before confirmation
- output/result: change quote with total due

## 5. Validation And Rule Enforcement

- the booking must belong to the signed-in customer
- departure must not already have passed
- only options allowed by fare and channel policy may be returned
- fee and fare difference must be returned before confirmation can continue

## 6. Dependencies And Integrations

- booking rules service
  - purpose: determine eligibility and allowed change behavior
  - failure impact: online change must stop with a clear fallback response
- fee calculation service
  - purpose: calculate fee and fare difference
  - failure impact: the customer cannot confirm the change online

## 7. Error And Fallback Behavior

- unauthorized booking access
  - BE response: deny access and return an authorization message code
  - visible effect: FE shows a blocked state instead of booking details
- booking not eligible for online change
  - BE response: return blocked eligibility plus rejection reason and support guidance key
  - visible effect: FE shows why online change cannot continue and what to do next
- fee service unavailable
  - BE response: return a temporary pricing failure state
  - visible effect: FE stops before confirmation and shows fallback guidance

## 8. Open Questions

- Is payment collection included in the first slice when total due is positive?
- Which rejection reason codes must be exposed directly to customers in release one?
