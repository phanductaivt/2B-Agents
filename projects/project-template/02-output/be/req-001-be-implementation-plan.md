---
file_type: "Sample Implementation Artifact"
primary_agents: ["BE"]
supporting_agents: ["Architect", "Data", "QA"]
activation_mode: "Reference Sample"
lifecycle_stage: "Project Sample Output"
purpose: "Show the BE implementation plan expected for the runnable ticket-change sample."
---
# req-001 BE Implementation Plan

## Files

- `02-output/app/backend/app/main.py`
  - FastAPI app, SQLite setup, routes, quote logic, confirmation logic
- `02-output/app/backend/tests/test_ticket_change.py`
  - pytest coverage for quote and confirmation behavior

## Routes

- `GET /health`
- `GET /tickets`
- `GET /tickets/{ticket_id}`
- `POST /tickets/{ticket_id}/change-quote`
- `POST /tickets/{ticket_id}/confirm-change`

## Tests

- quote returns fare difference, change fee, and total due
- confirm without payment is rejected
- confirm with payment updates ticket and returns confirmation sent
