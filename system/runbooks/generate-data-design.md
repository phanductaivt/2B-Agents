---
file_type: "Runbook"
primary_agents: ["Data"]
supporting_agents: ["Architect", "BE", "QA"]
activation_mode: "Triggered By Workflow"
lifecycle_stage: "System Core"
purpose: "Generate data model, state transition, SQLite schema plan, and metric tracking plan for a runnable feature slice."
reads: ["02-output/po/", "02-output/ba/", "02-output/architecture/", "02-output/design/", "02-output/be/", "02-output/fe/", "02-output/qa/", "03-context/", "system/rules/", "system/guardrails/", "system/skills/", "system/templates/"]
produces: ["02-output/data/<req>-data-model.md", "02-output/data/<req>-state-transition.md", "02-output/data/<req>-schema-plan.md", "02-output/data/<req>-metric-tracking-plan.md"]
---
# Generate Data Design

Use this runbook after architecture is ready and before BE implementation. If wireframe, API, FE, or QA outputs already exist, read them to make metric tracking sources more concrete.

## Required Skills

- `data-model-designer`
- `sqlite-schema-planner`
- `metric-framework-selector`
- `feature-metrics-planner`
- `tracking-event-planner`
- `metric-logic-checker`

## Steps

1. Read PO BRD, BA package, architecture note, NFR review, and security review.
2. Read wireframe, BE/API, FE, and QA outputs when available; if they are missing, mark tracking sources as proposed.
3. Invoke `data-model-designer` and define entities, fields, relationships, ownership, and seed data.
4. Define important state transitions for workflow-sensitive entities.
5. Invoke `sqlite-schema-planner` and create a SQLite schema plan.
6. Invoke `metric-framework-selector` and choose the measurement framework or hybrid that fits the feature and PO decision.
7. Invoke `feature-metrics-planner` and define outcome, behavior, funnel/task, quality/health, and guardrail metrics.
8. Invoke `tracking-event-planner` and map metrics to events/actions with trigger, source, actor, properties, timing, verification, dev notes, and privacy notes.
9. Invoke `metric-logic-checker` before finalizing the metric tracking plan.
10. Write outputs to `02-output/data/`.
11. Ask clarification when missing data ownership, state transition rules, PO decision goals, or sensitive tracking needs would change implementation or QA expected results.

## Validation

- every stored entity supports a defined behavior
- state transitions match BA and BE behavior
- SQLite schema is simple enough for local runnable v1
- seed data is safe sample data, not production policy
- every metric supports a PO decision and has at least one tracking event or action
- every tracking event has trigger, source, properties, verification, and privacy notes
- metrics and events do not contradict BRD, FRS, acceptance criteria, API, FE, NFR, security, or QA outputs
