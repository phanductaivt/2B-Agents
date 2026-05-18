---
file_type: "Architecture Artifact"
primary_agents: ["Architect"]
supporting_agents: ["Data", "BE", "FE", "QA", "Release"]
activation_mode: "Generated Output"
lifecycle_stage: "Project Output"
purpose: "Architecture note for the inventory management runnable slice."
---
# req-001 Architecture Note

## Runtime Stack

- Backend: Python FastAPI.
- Persistence: SQLite.
- Frontend: Vite React TypeScript.
- Delivery target: local runnable demo.

## Module Boundaries

- Frontend owns screen state, form input, delete confirmation, and API calls.
- Backend owns validation, product status calculation, uniqueness, persistence, and soft delete.
- SQLite stores product records and seeded review data.

## Data Flow

1. Browser calls FastAPI `/api/products`.
2. FastAPI validates input with Pydantic and business logic.
3. FastAPI reads/writes SQLite.
4. FastAPI returns normalized JSON using camelCase response fields.
5. React refreshes list/detail after mutations.

## Implementation Implications

- Status calculation must be centralized in backend.
- Frontend may display status but must not be the source of truth.
- Search can be implemented server-side using case-insensitive query.
- Delete should be soft delete to satisfy "not visible" without physical loss in demo.

## Constraints

- No authentication in v1.
- No multi-warehouse support.
- No stock movement history.
- Local SQLite is not production persistence.
