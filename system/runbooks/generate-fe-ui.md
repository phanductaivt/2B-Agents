---
file_type: "Runbook"
primary_agents: ["FE"]
supporting_agents: ["UIUX", "BE", "BA", "Architect", "Data"]
activation_mode: "Triggered By Workflow"
lifecycle_stage: "System Core"
purpose: "Generate a frontend review prototype from BA, BE, and design outputs."
reads: ["02-output/ba/", "02-output/data/", "02-output/be/", "02-output/design/", "02-output/architecture/", "03-context/", "system/rules/", "system/guardrails/", "system/skills/", "system/templates/"]
produces: ["02-output/fe/<req>-ui.html"]
---
# Generate FE UI

Use this runbook after BA and wireframe outputs are ready.

## Required Skills

- `html-implementer`

## Optional Skills

- `fe-state-modeler`
  - use when the UI slice has multiple visible states or state transitions
- `fe-validation-mapper`
  - use when validation or error feedback is important to the slice
- `fe-api-consumption-planner`
  - use when the FE flow depends on multiple BE actions or response branches
- use `resolve-clarification.md` instead of guessing when BA, BE, and design still conflict

## Inputs

- `02-output/po/<req>-brd.md`
- `02-output/ba/<req>-frs.md`
- `02-output/ba/<req>-feature-list.md`
- `02-output/be/<req>-api-contract.md`
- `02-output/be/<req>-be-spec.md`
- `02-output/data/<req>-metric-tracking-plan.md` when measurement is in scope
- `02-output/design/<req>-wireframe.md`
- `02-output/architecture/` when runnable implementation is requested
- relevant `03-context/` files

## Steps

1. Read the PO BRD, BE package, Data metric tracking plan when relevant, and the functional and UI inputs
2. Use `template-fe-technical-design.md` as a planning structure when interaction, state, validation, tracking, or API dependencies are complex enough to cause FE guesswork
3. If the slice has multiple visible states or state transitions:
   - invoke `fe-state-modeler`
4. If validation or error feedback is important to the slice:
   - invoke `fe-validation-mapper`
5. If the FE flow depends on multiple BE actions or response branches:
   - invoke `fe-api-consumption-planner`
6. Stop and resolve BA or BE gaps first if the FRS, feature list, wireframe, and API behavior still conflict materially
7. Invoke `html-implementer` and build a simple reviewable HTML page
8. Write it to `02-output/fe/<req>-ui.html`
