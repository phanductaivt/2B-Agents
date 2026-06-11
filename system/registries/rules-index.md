---
file_type: "Rules Index"
primary_agents: []
supporting_agents: ["PO", "BA", "Architect", "Data", "BE", "UIUX", "FE", "QA", "Release"]
activation_mode: "Routing Reference"
lifecycle_stage: "System Core"
purpose: "Map workflows and runbooks to exact rule files without loading entire rule folders."
---
# Rules Index

Use this index to find candidate rules. Load a rule only when the active
workflow or runbook declares it.

## Runtime Delivery Rules

| Rule | Purpose | Used By | Load When |
| --- | --- | --- | --- |
| `system/rules/read-rules-start-here.md` | Provide the shared rule entrypoint. | Product delivery and change-control runbooks | The active runbook declares the shared rule entrypoint. |
| `system/rules/define-system-overview.md` | Define the repository operating flow. | Repository governance and orientation | The system model itself is under review; not every product phase. |
| `system/rules/define-agent-design.md` | Define Agent ownership and collaboration boundaries. | Agent governance or an ownership conflict | Agent boundaries must be interpreted or reviewed. |
| `system/rules/define-output-standards.md` | Define output quality and consistency standards. | Artifact-generating and review runbooks | The active runbook declares output standards. |
| `system/rules/define-project-conventions.md` | Define project paths, naming, and repository conventions. | Implementation, Release, and change control | The active runbook creates or updates project files. |

## Component Factory Rules

These rules apply only to `component-governance`. Do not route them into normal
product delivery.

| Rule | Purpose | Load When |
| --- | --- | --- |
| `system/component-factory/rules/component-creation-rules.md` | Decide whether a new component is justified. | Creating a component. |
| `system/component-factory/rules/component-dependency-rules.md` | Govern checked dependencies between components. | Creating, reviewing, or updating a component with dependencies. |
| `system/component-factory/rules/component-naming-rules.md` | Govern component naming. | Creating or renaming is proposed. |
| `system/component-factory/rules/component-scope-rules.md` | Keep component purpose and type boundaries clean. | Classifying, creating, reviewing, or updating a component. |
| `system/component-factory/rules/component-update-rules.md` | Govern targeted component updates. | Updating an existing component. |

## Boundaries

- Rules guide repeatable behavior.
- Guardrails prohibit unsafe behavior and define stop conditions.
- Skills provide reusable capability instructions.
- Workflow contracts select phases and gates.
- Runbooks define executable procedures.
