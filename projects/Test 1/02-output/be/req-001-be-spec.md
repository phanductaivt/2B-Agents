---
file_type: "BE Artifact"
primary_agents: ["BE"]
supporting_agents: ["Architect", "Data", "FE", "QA"]
activation_mode: "Generated Output"
lifecycle_stage: "Project Output"
purpose: "Backend specification for req-001."
---
# req-001 BE Spec

## Backend Responsibilities

- Provide Product CRUD APIs.
- Validate product input.
- Enforce product code uniqueness.
- Calculate stock status.
- Persist records in SQLite.
- Exclude soft-deleted products from list/search/detail.

## Error Handling

- Duplicate code: `409`.
- Validation failure: `400`.
- Product not found: `404`.
- Responses include business-readable `message`.

## Implementation Stack

- FastAPI.
- SQLite.
- Pydantic.
- Pytest.
