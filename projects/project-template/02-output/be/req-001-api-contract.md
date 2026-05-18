---
file_type: "Sample BE Artifact"
primary_agents: ["BE"]
supporting_agents: ["BA", "FE"]
activation_mode: "Reference Sample"
lifecycle_stage: "Project Sample Output"
purpose: "Show the expected quality and structure of the backend artifact for api contract."
---
# Requirement: req-001

# API Contract: Ticket Booking Modification Improvement

- API Contract ID: `API-001`
- Parent BRD ID: `BRD-001`
- Parent FR ID: `FR-001`

## 1. Contract Summary

This contract supports the first-slice booking change experience for eligibility, option review, fee visibility, and confirmation handoff.

## 2. Action Or Endpoint

### Name

- `GET /booking-change/{bookingId}`

### Purpose

- load booking summary and initial eligibility context for the current customer

### Request

- bookingId
  - type: string
  - required: yes
  - notes: booking identifier from the current user's booking list

### Response

- bookingId
  - type: string
  - notes: selected booking reference
- eligible
  - type: boolean
  - notes: whether online change can continue
- eligibilityReasonCode
  - type: string | null
  - notes: rejection code when not eligible
- supportGuidanceKey
  - type: string | null
  - notes: FE uses this to show fallback guidance

### Business Errors

- unauthorized-booking
  - when: the booking does not belong to the current customer
  - FE impact: show blocked state and hide booking details

## 3. Action Or Endpoint

### Name

- `GET /booking-change/{bookingId}/options`

### Purpose

- return allowed date-change options for an eligible booking

### Request

- bookingId
  - type: string
  - required: yes
  - notes: booking must already be eligible

### Response

- options
  - type: array
  - notes: list of allowed change options
- options[].optionId
  - type: string
  - notes: selected by FE before pricing
- options[].newTravelDate
  - type: string
  - notes: ISO date shown to the customer

### Business Errors

- booking-not-eligible
  - when: eligibility fails or changes before options load
  - FE impact: move user to fallback guidance state

## 4. Action Or Endpoint

### Name

- `POST /booking-change/{bookingId}/quote`

### Purpose

- calculate fee and fare difference for the selected change option before confirmation

### Request

- optionId
  - type: string
  - required: yes
  - notes: selected option for pricing

### Response

- optionId
  - type: string
  - notes: echoes the selected option
- fareDifference
  - type: number
  - notes: positive, zero, or negative fare delta
- changeFee
  - type: number
  - notes: rule-based change fee
- totalDue
  - type: number
  - notes: amount the customer must pay before change can continue
- currency
  - type: string
  - notes: display currency for FE

### Business Errors

- pricing-unavailable
  - when: fee calculation service is unavailable
  - FE impact: stop before confirmation and show retry/support guidance
- invalid-option
  - when: the selected option is no longer valid
  - FE impact: ask the customer to reselect an option

## 5. Notes

- Confirmation submission endpoint is intentionally deferred until payment-scope decision is confirmed.
