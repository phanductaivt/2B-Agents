---
file_type: "Runbook"
primary_agents: ["BE"]
supporting_agents: ["BA", "Architect", "Data", "FE"]
activation_mode: "Triggered By Workflow"
lifecycle_stage: "System Core"
purpose: "Generate backend design and API contract outputs from BA and PO artifacts."
reads: ["02-output/po/<req>-brd.md", "02-output/ba/", "02-output/architecture/", "02-output/data/", "03-context/", "system/rules/", "system/guardrails/", "system/skills/", "system/templates/"]
produces: ["02-output/be/<req>-be-spec.md", "02-output/be/<req>-api-contract.md"]
---
# Generate BE Package

Use this runbook after the PO BRD and BA package are ready.
For runnable delivery, use it after architecture and data design are also ready.

## Required Skills

- `be-solution-designer`
- `api-contract-writer`

## Optional Skills

- `rule-coverage-checker`
  - use when rules, validations, or policy branches materially affect BE behavior

## Inputs

- `02-output/po/<req>-brd.md`
- `02-output/ba/<req>-frs.md`
- `02-output/ba/<req>-feature-list.md`
- `02-output/ba/<req>-process-bpmn.md` when flow branching matters
- `02-output/architecture/` when runnable implementation is requested
- `02-output/data/` when persistence or state matters
- relevant `03-context/` files

## Outputs

- `02-output/be/<req>-be-spec.md`
- `02-output/be/<req>-api-contract.md`

## Steps

1. Read the PO BRD first to understand business intent, scope, rules, and priority boundaries
2. Read the BA package to understand functional behavior, branching, validations, dependencies, and first-slice scope
3. Read architecture and data outputs when runnable implementation is expected, including the metric tracking plan when backend outcomes are needed for metrics
4. Invoke `be-solution-designer` to define the BE responsibilities needed to support that slice
5. Write a BE spec that covers:
   - service responsibilities
   - core entities or records
   - main business actions
   - validations and rule enforcement
   - dependencies and integrations
   - error and fallback behavior
   - server-side tracking touchpoints when metric events depend on backend outcomes
6. Invoke `api-contract-writer` and write an API contract that covers:
   - endpoint or action name
   - purpose
   - request fields
   - response structure
   - business errors or important failure cases
   - server-side tracking touchpoints from the metric tracking plan when relevant
7. If business rules are dense or spread across BRD, FRS, and BPMN:
   - invoke `rule-coverage-checker`
8. Keep the BE package implementation-facing but still readable for FE review
9. Ask clarification if missing rules would materially change BE behavior, authorization, payment flow, or integration contracts

## Self-Check Before Finishing

- backend scope still matches the PO BRD and BA package
- no hidden behavior is invented outside the defined slice
- request and response behavior is clear enough for FE handoff
- validation, dependency, and exception paths are visible
- server-side metric tracking touchpoints are referenced or explicitly marked out of scope
