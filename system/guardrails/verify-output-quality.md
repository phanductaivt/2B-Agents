---
file_type: "Guardrail"
primary_agents: ["PO", "BA", "Architect", "Data", "BE", "UIUX", "FE", "QA", "Release"]
supporting_agents: []
activation_mode: "Always-On Shared"
lifecycle_stage: "System Core"
purpose: "Define the shared quality checks that outputs must pass before downstream use."
---
# Verify Output Quality

Before finishing an execution pass, verify:

1. the final output exists in `02-output/`
2. the output matches the requirement and project context
3. assumptions are visible where needed
4. the output is readable for review

## Best-Effort vs Clarification

Infer with best effort when:
- the business intent is clear enough to proceed safely
- a measurable success metric is missing but can be marked as missing
- wording or labels are incomplete without changing scope or behavior

Ask clarification when:
- a missing business rule would change the product behavior
- the business objective or primary actor is unclear
- the requested scope conflicts with stated policy, priority, or first-slice intent
- pricing, approval, eligibility, or exception handling logic is materially unclear

## Minimum Acceptable Quality

### PO BRD

- the problem statement is specific
- the business objective is measurable or explicitly marked as still missing
- affected users or stakeholders are visible
- BACCM framing is visible and understandable
- business, stakeholder, solution, and transition requirements are classified clearly
- in-scope and out-of-scope boundaries are clear
- success measures are not vague
- assumptions and open questions are separated
- priority or tradeoff notes are visible when scope pressure exists
- use `checklist-brd.md` as the final review support
- use `brd-drafter`, `baccm-product-framer`, and `requirement-classifier` as the expected generation path

### BRD
- the BA output set must not recreate a second BRD

### FRS

- functional requirements are observable
- main flow and alternative flows are consistent
- business rules, validations, dependencies, and edge cases are explicit
- unauthorized access, missing data, and unavailable dependencies are covered or flagged
- PO BRD scope and FRS scope do not conflict
- use `checklist-frs.md` as the final review support
- use `frs-drafter` as the expected generation path
- use `rule-coverage-checker` when rule-sensitive behavior spans multiple artifacts

### User Story

- the actor, need, and business value are clear
- the story fits the same scope as the PO BRD and FRS
- the story is focused on one first-slice outcome
- use `checklist-user-story.md` as the final review support
- use `user-story-writer` as the expected generation path

### Acceptance Criteria

- each criterion is testable and observable
- the main path is covered
- relevant exception or validation paths are covered
- wording is specific and free of vague quality terms
- use `checklist-acceptance-criteria.md` as the final review support
- use `acceptance-criteria-writer` as the expected generation path

### Feature List

- the hierarchy is logical and non-overlapping
- the list reflects the same scope as the FRS
- duplicate features are removed
- the first release slice is buildable and reviewable
- use `checklist-feature-list.md` as the final review support
- use `feature-breakdown-writer` as the expected generation path
- use `scope-boundary-checker` when scope still feels mixed or too broad

### BE Spec

- service responsibilities are explicit
- main business actions map back to the PO BRD and BA FRS
- validation, dependency, persistence, and integration behavior are visible
- BE behavior does not invent scope outside the BRD and BA package
- use `be-solution-designer` as the expected generation path

### Architecture Note

- runtime shape is explicit
- module boundaries are clear
- architecture matches the same slice as BRD and FRS
- BE, FE, Data, QA, and Release can consume it without guessing core constraints
- use `architecture-designer` as the expected generation path

### NFR Review

- performance, reliability, usability, observability, and maintainability expectations are visible
- missing NFRs are marked as gaps instead of invented
- use `nfr-reviewer` as the expected generation path

### Security Review

- actor access, data sensitivity, authorization, and safe error behavior are visible
- payment, ownership, privacy, and sensitive-data risks are flagged when relevant
- use `security-reviewer` as the expected generation path

### Data Model And Schema Plan

- entities, fields, ownership, relationships, and state transitions map to approved behavior
- SQLite schema supports the local runnable v1
- seed data is clearly sample data
- use `data-model-designer` and `sqlite-schema-planner` as the expected generation path

### Metric Tracking Plan

- selected metric framework or hybrid is stated with a reason tied to feature type and PO decision needs
- every metric supports a real PO decision and is not a vanity metric
- every metric has a clear type, calculation guidance, reading guidance, related tracking events, and decision scenarios
- every tracking event or action has a trigger, source, actor, required properties, expected timing, verification, and privacy note
- event properties avoid sensitive data unless a business reason and safe treatment are explicit
- gaps, missing baselines, missing targets, and proposed-only sources are marked instead of invented
- metric logic does not contradict BRD, FRS, acceptance criteria, API, FE behavior, NFR, security, or QA risks
- use `metric-framework-selector`, `feature-metrics-planner`, `tracking-event-planner`, and `metric-logic-checker` as the expected generation path

### Implementation Plans

- BE and FE implementation plans map back to approved architecture, data, API, wireframe, and QA expectations
- planned files, modules, routes, components, validations, and tests are visible
- use `be-implementation-planner` and `react-api-integration-planner` as expected planning support

### API Contract

- endpoints or actions are named consistently
- request inputs, response outputs, and error cases are visible
- status/result behavior is specific enough for FE handoff
- authentication, authorization, and payment-relevant steps are covered or flagged
- server-side tracking touchpoints from the metric tracking plan are referenced when backend outcome is needed for a metric
- use `api-contract-writer` as the expected generation path

### Test Scenarios

- happy path is covered
- important negative and exception paths are covered
- business-rule-sensitive areas are visible
- backend and FE interaction risks are represented
- use `checklist-test-scenarios.md` as the final review support
- use `test-scenario-designer` as the expected generation path
- use `exception-scenario-expander` when negative-path coverage is still thin

### Test Cases

- each case is specific, observable, and reproducible
- preconditions and expected results are visible
- evidence capture or execution-record expectations are visible
- automation candidate and automation priority are stated
- positive, negative, validation, and dependency-failure cases are included where relevant
- cases reflect the same slice as the BRD, FRS, API contract, and UI
- important tracking events from the metric tracking plan have verification checks when instrumentation is in scope
- use `checklist-test-cases.md` as the final review support
- use `test-case-writer` as the expected generation path

### QA Release Readiness

- major quality risks are stated clearly
- unresolved blockers are separated from acceptable known gaps
- readiness recommendation is explicit
- authorization, pricing, payment, dependency, and customer-impact risks are called out when relevant
- use `checklist-release-readiness.md` as the final review support
- use `release-readiness-reviewer` as the expected generation path

### Runnable System Verification

- backend install, run, or test command is recorded
- frontend install, run, or build command is recorded
- database setup or reset command is recorded
- at least one smoke or test command is recorded
- actual command results are visible
- a project is not described as runnable when verification is missing or failed
- use `runnable-system-verifier` as the expected generation path

### Release Readiness

- local runnable status, production gaps, and release recommendation are separated
- release readiness does not override QA risks or security blockers
- deploy-ready claims are avoided unless deployment checks exist
- use `release-runbook-writer` as the expected writing support

## Cross-Artifact Consistency

- ambiguity, scope boundaries, and open questions are visible in the BA package
- PO BRD framing does not conflict with BA analysis, or the conflict is raised clearly
- PO BRD and FRS describe the same business slice
- BE spec and API contract align with the same BRD and FRS slice
- user story and acceptance criteria match the PO BRD and FRS scope
- FE UI behavior does not conflict with backend contract behavior
- QA scenarios and cases align with the same BRD, FRS, BE, and FE slice
- metric tracking plan aligns with BRD success measures, BA behavior, FE/API sources, NFR risks, and QA verification
- architecture, data, implementation, and release outputs align with the same product slice
- runnable app behavior matches the documented API contract and FE plan
- feature list does not drift away from the FRS
- BPMN reflects the main path and relevant alternative flow structure

## Cross-Artifact Skill Support

- use `ambiguity-checker-plus` when cross-artifact meaning is unstable
- use `rule-coverage-checker` when business rules must stay aligned across BRD, FRS, AC, BPMN, BE, and QA
- use `scope-boundary-checker` when outputs appear to drift beyond the first slice
