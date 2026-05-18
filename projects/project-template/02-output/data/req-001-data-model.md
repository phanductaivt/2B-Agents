---
file_type: "Sample Data Artifact"
primary_agents: ["Data"]
supporting_agents: ["BE", "QA"]
activation_mode: "Reference Sample"
lifecycle_stage: "Project Sample Output"
purpose: "Show the data model expected for the runnable ticket-change sample."
---
# req-001 Data Model

## Entity: Ticket

- purpose: represent a confirmed travel ticket that may be changed before departure
- owner: customer
- fields:
  - `id`
  - `passenger_name`
  - `route`
  - `travel_date`
  - `departure_date`
  - `fare_amount`
  - `status`

## Field Rules

- `id` is unique.
- `travel_date` changes after successful confirmation.
- `departure_date` is used to enforce date-change eligibility.
- `status` starts as `confirmed` and becomes `changed` after confirmation.

## Seed Data

- `TCK-1001`: SGN to HAN
- `TCK-1002`: HAN to DAD
