---
file_type: "Architecture Artifact"
primary_agents: ["Architect"]
supporting_agents: ["QA", "BE", "FE", "Release"]
activation_mode: "Generated Output"
lifecycle_stage: "Project Output"
purpose: "NFR review for req-001."
---
# req-001 NFR Review

## Usability

- UI should expose list, search, form, detail, quantity update, and delete confirmation on one understandable surface.
- Validation errors must be visible next to the workflow.

## Performance

- SQLite list/search is acceptable for local v1 and sample data.
- For 10,000 products, an index on product_code and product_name is recommended.

## Reliability

- Mutations must persist in SQLite.
- Soft delete avoids accidental loss in local demo and supports future recovery/audit.

## Maintainability

- Backend should separate validation/status calculation helper functions from route handlers where practical.
- Frontend should keep API wrappers explicit and easy to replace.

## Verification

- Backend pytest should cover create, duplicate code, validation, status update, search, and delete.
- Frontend build must pass.
