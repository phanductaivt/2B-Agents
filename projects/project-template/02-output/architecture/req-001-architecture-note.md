---
file_type: "Sample Architecture Artifact"
primary_agents: ["Architect"]
supporting_agents: ["BE", "FE", "Data", "QA", "Release"]
activation_mode: "Reference Sample"
lifecycle_stage: "Project Sample Output"
purpose: "Show the architecture note expected for the runnable ticket-change sample."
---
# req-001 Architecture Note

## 1. Slice Summary

- Requirement: self-service ticket date change
- Runnable target: local FastAPI + SQLite + Vite React TypeScript
- Source BRD: `02-output/po/req-001-brd.md`
- Source BA package: `02-output/ba/`

## 2. Runtime Shape

- Backend: FastAPI service with SQLite persistence
- Database: SQLite file seeded with sample confirmed tickets
- Frontend: Vite React TypeScript UI
- Test approach: pytest for API behavior and smoke instructions for local app flow

## 3. Module Boundaries

- Backend API
  - owns ticket lookup, quote calculation, confirmation, validation, and persistence
- Frontend UI
  - owns ticket selection, date input, quote display, confirmation action, and user-visible states
- SQLite data layer
  - owns ticket records and changed status persistence

## 4. Data Flow

- FE loads tickets from BE
- user selects a ticket and date
- FE requests a quote from BE
- BE validates date-before-departure and returns fee breakdown
- FE confirms with payment flag
- BE updates ticket and returns confirmation status

## 5. Architecture Risks

- Payment is simulated with `payment_confirmed`; real payment integration is out of scope for sample runnable v1.
- Error reason codes are minimal and should be expanded before production use.
