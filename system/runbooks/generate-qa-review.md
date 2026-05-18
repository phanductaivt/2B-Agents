---
file_type: "Runbook"
primary_agents: ["QA"]
supporting_agents: ["BA", "BE", "FE"]
activation_mode: "Triggered By Workflow"
lifecycle_stage: "System Core"
purpose: "Generate QA review outputs from BRD, BA, Data, BE, design, and FE artifacts."
reads: ["02-output/po/<req>-brd.md", "02-output/ba/", "02-output/data/", "02-output/be/", "02-output/design/", "02-output/fe/", "03-context/", "system/rules/", "system/guardrails/", "system/skills/", "system/templates/"]
produces: ["02-output/qa/<req>-test-scenarios.md", "02-output/qa/<req>-test-cases.md", "02-output/qa/<req>-release-readiness.md"]
---
# Generate QA Review

Use this runbook after the BA, Data, BE, design, and FE outputs are ready enough to review as one slice.

## Required Skills

- `test-scenario-designer`
- `test-case-writer`
- `release-readiness-reviewer`

## Optional Skills

- `exception-scenario-expander`
  - use when negative or fallback behavior is still too thin in upstream artifacts
- `rule-coverage-checker`
  - use when business-rule-sensitive behavior drives expected results

## Inputs

- `02-output/po/<req>-brd.md`
- `02-output/ba/<req>-frs.md`
- `02-output/ba/<req>-acceptance-criteria.md`
- `02-output/ba/<req>-process-bpmn.md` when branching matters
- `02-output/data/<req>-metric-tracking-plan.md` when measurement is in scope
- `02-output/be/<req>-be-spec.md`
- `02-output/be/<req>-api-contract.md`
- `02-output/design/<req>-wireframe.md`
- `02-output/fe/<req>-ui.html`
- relevant `03-context/` files

## Outputs

- `02-output/qa/<req>-test-scenarios.md`
- `02-output/qa/<req>-test-cases.md`
- `02-output/qa/<req>-release-readiness.md`

## Steps

1. Read the BRD first to understand the intended business slice and business risk
2. Read the BA package to understand functional behavior, rules, validations, and exception handling
3. Read the Data metric tracking plan to understand important tracking events and verification needs
4. Read the BE package to understand request, response, dependency, error behavior, and server-side tracking touchpoints
5. Read the wireframe and FE output to understand user-visible flow, interaction states, and UI tracking touchpoints
6. If upstream exception behavior is still under-specified:
   - invoke `exception-scenario-expander`
7. If business rules drive multiple expected-result branches:
   - invoke `rule-coverage-checker`
8. Invoke `test-scenario-designer` and write test scenarios that cover:
   - happy path
   - negative path
   - validation path
   - dependency failure path
   - authorization or ownership path
   - pricing or payment-sensitive path when relevant
   - tracking verification for important metric events when instrumentation is in scope
9. Invoke `test-case-writer` and write detailed test cases from those scenarios with preconditions, steps, expected results, and tracking verification when relevant
10. Invoke `release-readiness-reviewer` and write a release-readiness review that clearly separates:
   - blockers
   - major risks
   - acceptable known gaps
   - readiness recommendation
11. Ask clarification if a missing rule or tracking source would materially change expected results, measurement trust, or readiness judgment

## Self-Check Before Finishing

- QA coverage still matches the same slice as BRD, FRS, BE, and FE
- important negative and exception paths are visible
- expected results are concrete and reproducible
- important metric events have verification coverage or are explicitly marked out of instrumentation scope
- blockers are not hidden inside general risk wording
- release recommendation is explicit
