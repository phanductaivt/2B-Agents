---
file_type: "Sample Schema Artifact"
primary_agents: ["Data"]
supporting_agents: ["BE"]
activation_mode: "Reference Sample"
lifecycle_stage: "Project Sample Output"
purpose: "Show the SQLite schema plan expected for the runnable ticket-change sample."
---
# req-001 Schema Plan

## Database Target

- Engine: SQLite
- Setup: seed automatically on first backend startup

## Table: tickets

- `id text primary key`
- `passenger_name text not null`
- `route text not null`
- `travel_date text not null`
- `departure_date text not null`
- `fare_amount integer not null`
- `status text not null`

## Seed Data

- two confirmed sample tickets for local testing

## Migration Notes

- no migration tool is used for v1 sample
- production implementation should introduce explicit migrations
