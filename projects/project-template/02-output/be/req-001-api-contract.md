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

This contract supports the runnable first-slice ticket change experience implemented by the sample FastAPI backend and consumed by the sample React frontend.

The implemented sample flow is:

1. Load available tickets.
2. Select one ticket.
3. Request a date-change quote.
4. Confirm the date change after payment confirmation when payment is required.

## 2. Shared Conventions

- Base URL is environment-specific. The local frontend uses `VITE_API_BASE_URL`.
- Request and response bodies are JSON.
- Dates use ISO `YYYY-MM-DD` format.
- Error responses use FastAPI's standard `detail` wrapper with a stable business error code:

```json
{
  "detail": {
    "code": "payment_required",
    "message": "Payment is required before confirming this change."
  }
}
```

## 3. Action Or Endpoint

### Name

- `GET /health`

### Purpose

- verify that the backend process is running and can initialize local data

### Request

- none

### Response

- status
  - type: string
  - notes: `ok` when the API is available

### Business Errors

- none expected for the local sample

## 4. Action Or Endpoint

### Name

- `GET /tickets`

### Purpose

- load the ticket list displayed by the frontend

### Request

- none

### Response

- array of ticket objects
  - type: array
- ticket.id
  - type: string
  - notes: ticket identifier used by later endpoints
- ticket.passengerName
  - type: string
  - notes: passenger display name
- ticket.route
  - type: string
  - notes: route display label
- ticket.travelDate
  - type: string
  - notes: current ticket travel date
- ticket.departureDate
  - type: string
  - notes: original departure date used for validation
- ticket.fareAmount
  - type: number
  - notes: current fare amount in the sample currency
- ticket.status
  - type: string
  - notes: current ticket status

### Business Errors

- none expected for the local sample

## 5. Action Or Endpoint

### Name

- `GET /tickets/{ticket_id}`

### Purpose

- load a single ticket by ID

### Request

- ticket_id
  - type: string
  - required: yes
  - notes: ticket identifier returned by `GET /tickets`

### Response

- same ticket object shape as `GET /tickets`

### Business Errors

- ticket_not_found
  - status: 404
  - when: no ticket exists for the requested `ticket_id`
  - FE impact: show backend error state

## 6. Action Or Endpoint

### Name

- `POST /tickets/{ticket_id}/change-quote`

### Purpose

- calculate fare difference, change fee, total due, and payment requirement for a requested new travel date

### Request

- ticket_id
  - type: string
  - required: yes
  - notes: ticket identifier returned by `GET /tickets`
- new_travel_date
  - type: string
  - required: yes
  - notes: requested new travel date in `YYYY-MM-DD` format

### Response

- ticketId
  - type: string
  - notes: selected ticket identifier
- newTravelDate
  - type: string
  - notes: requested new travel date
- fareDifference
  - type: number
  - notes: positive, zero, or negative fare delta
- changeFee
  - type: number
  - notes: rule-based change fee
- totalDue
  - type: number
  - notes: amount that must be paid before confirmation when positive
- paymentRequired
  - type: boolean
  - notes: whether confirmation requires payment confirmation

### Business Errors

- ticket_not_found
  - status: 404
  - when: no ticket exists for the requested `ticket_id`
  - FE impact: show backend error state
- change_after_departure
  - status: 400
  - when: requested `new_travel_date` is on or after the ticket departure date
  - FE impact: show backend validation error and do not allow confirmation

## 7. Action Or Endpoint

### Name

- `POST /tickets/{ticket_id}/confirm-change`

### Purpose

- confirm the ticket date change after required payment confirmation

### Request

- ticket_id
  - type: string
  - required: yes
  - notes: ticket identifier returned by `GET /tickets`
- new_travel_date
  - type: string
  - required: yes
  - notes: requested new travel date in `YYYY-MM-DD` format
- payment_confirmed
  - type: boolean
  - required: no
  - default: false
  - notes: must be true when the quote requires payment

### Response

- ticketId
  - type: string
  - notes: changed ticket identifier
- status
  - type: string
  - notes: `changed` after successful update
- newTravelDate
  - type: string
  - notes: confirmed new travel date
- confirmationSent
  - type: boolean
  - notes: whether the sample flow simulated confirmation delivery
- totalPaid
  - type: number
  - notes: amount paid according to the quote calculation

### Business Errors

- ticket_not_found
  - status: 404
  - when: no ticket exists for the requested `ticket_id`
  - FE impact: show backend error state
- change_after_departure
  - status: 400
  - when: requested `new_travel_date` is on or after the ticket departure date
  - FE impact: show backend validation error and do not confirm
- payment_required
  - status: 402
  - when: the quote requires payment but `payment_confirmed` is false
  - FE impact: require payment confirmation before retrying confirmation

## 8. Contract Alignment Notes

- This contract intentionally matches the sample backend routes in `02-output/app/backend/app/main.py`.
- This contract intentionally matches the sample frontend API calls in `02-output/app/frontend/src/main.tsx`.
- The local sample simulates payment confirmation with `payment_confirmed`; it is not a real payment integration.
