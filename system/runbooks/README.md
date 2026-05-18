---
file_type: "Runbook Index"
primary_agents: ["PO", "BA", "Architect", "Data", "BE", "UIUX", "FE", "QA", "Release"]
supporting_agents: []
activation_mode: "Manual Navigation"
lifecycle_stage: "System Core"
purpose: "Explain which runbook to use for each stage of the delivery flow."
---
# Runbooks

Runbooks are the main reusable operating prompts for Codex.

Use:
- `generate-brd.md`
- `generate-ba-package.md`
- `generate-architecture.md`
- `generate-data-design.md`
- `generate-be-package.md`
- `implement-be.md`
- `generate-wireframe.md`
- `generate-fe-ui.md`
- `implement-fe.md`
- `generate-qa-review.md`
- `generate-product-slice.md`
- `integrate-runnable-app.md`
- `verify-runnable-system.md`
- `resolve-clarification.md`
- `regenerate-output.md`
- `handle-change-request.md`

Typical sequence:
- PO framing first: `generate-brd.md`
- BA package next: `generate-ba-package.md`
- architecture next: `generate-architecture.md`
- data design next: `generate-data-design.md`
- BE next: `generate-be-package.md`, then `implement-be.md`
- design next: `generate-wireframe.md`
- FE prototype and app next: `generate-fe-ui.md`, then `implement-fe.md`
- QA review last: `generate-qa-review.md`
- runnable integration and verification last: `integrate-runnable-app.md`, then `verify-runnable-system.md`

Use `generate-product-slice.md` when you want one master flow for a requirement.

Use `handle-change-request.md` when an existing stable project receives a customer change request or customization request. It controls CR intake, impact analysis, approval, baseline snapshot, targeted apply, verification, requirement merge, and rollback.
