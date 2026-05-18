---
file_type: "Runbook"
primary_agents: ["UIUX"]
supporting_agents: ["BA", "FE"]
activation_mode: "Triggered By Workflow"
lifecycle_stage: "System Core"
purpose: "Generate a wireframe from BA outputs and relevant project context."
reads: ["02-output/ba/", "03-context/", "system/rules/", "system/guardrails/", "system/skills/", "system/templates/"]
produces: ["02-output/design/<req>-wireframe.md"]
---
# Generate Wireframe

Use this runbook after the BA package is ready.

## Required Skills

- `wireframe-writer`

## Optional Skills

- `process-analyzer`
  - use when a complex process needs clearer screen sequencing before drawing the wireframe

## Inputs

- `02-output/po/<req>-brd.md`
- `02-output/ba/<req>-frs.md`
- `02-output/ba/<req>-feature-list.md`
- `02-output/ba/<req>-process-bpmn.md` when useful
- project context from `03-context/`

## Steps

1. Read the PO BRD and the BA outputs that define the flow, rules, and screen needs
2. If the user flow is hard to map from artifacts to screens:
   - invoke `process-analyzer`
3. Stop and resolve BA gaps first if the FRS, BPMN, or feature list still conflict materially
4. Invoke `wireframe-writer` and create a simple Markdown wireframe
5. Write it to `02-output/design/<req>-wireframe.md`
