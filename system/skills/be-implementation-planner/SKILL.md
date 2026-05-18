---
name: be-implementation-planner
description: Plan backend implementation tasks from BE spec, API contract, architecture, and data design. Use before creating FastAPI code.
---
# BE Implementation Planner

## Use When

- BE has spec/API contracts and is ready to become runnable code
- implementation order, validation, and error behavior need to be explicit

## Output

A Markdown implementation plan covering:
- files/modules to create
- API routes
- service functions
- validation logic
- persistence behavior
- test targets

## Rules

- do not change business scope
- keep implementation aligned to existing artifact names and endpoints
- flag missing behavior before coding
