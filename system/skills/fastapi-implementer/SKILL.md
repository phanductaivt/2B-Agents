---
name: fastapi-implementer
description: Implement a local runnable FastAPI backend from approved BE, architecture, and data outputs. Use when backend code should be created under project 02-output/app/backend.
---
# FastAPI Implementer

## Use When

- the project needs a runnable Python API
- BE spec, API contract, and data design are available or can be safely inferred

## Output

FastAPI backend code with:
- app entrypoint
- API routes
- SQLite persistence
- seed/setup behavior
- pytest coverage for core behavior
- README run commands

## Rules

- keep dependencies minimal
- use SQLite for v1 unless project context says otherwise
- implement only the approved slice
- include tests for quote/confirmation or equivalent core actions
