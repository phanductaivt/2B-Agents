---
file_type: "Sample NFR Artifact"
primary_agents: ["Architect"]
supporting_agents: ["BE", "FE", "QA"]
activation_mode: "Reference Sample"
lifecycle_stage: "Project Sample Output"
purpose: "Show the NFR review expected for the runnable ticket-change sample."
---
# req-001 NFR Review

## 1. Scope

- Feature: self-service ticket date change
- Runtime target: local runnable demo

## 2. Performance

- The quote and confirmation actions should feel immediate for sample data.
- No production latency target is defined.

## 3. Reliability

- Backend should return clear errors for missing ticket, invalid date, and missing payment.
- SQLite seed should allow the app to run after a clean checkout.

## 4. Usability

- User must see fare difference, change fee, and total due before confirming.
- Success and error messages must be visible in the UI.

## 5. Observability

- Local sample does not include structured logging.
- Verification output must record command results.

## 6. Open Gaps

- Real payment integration and confirmation delivery are simulated.
