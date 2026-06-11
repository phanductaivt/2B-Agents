---
file_type: "Factory Index"
primary_agents: []
supporting_agents: ["PO", "BA", "Architect", "Data", "BE", "UIUX", "FE", "QA", "Release"]
activation_mode: "Component Classification"
lifecycle_stage: "System Core"
purpose: "Route supported Component Factory types to their canonical runtime homes, creation procedures, templates, and registries."
---
# Component Types Index

Use this index to classify one component request before selecting a factory
runbook. `Active Agent` remains `None` for Component Factory governance.

| Component Type | Canonical Runtime Home | Creation Runbook | Creation Meta-Skill | Template Or Contract | Required Registry Update |
| --- | --- | --- | --- | --- | --- |
| Skill | `system/skills/` | `system/component-factory/runbooks/create-skill-runbook.md` | `system/component-factory/meta-skills/create-skill/SKILL.md` | `system/component-factory/templates/skill-template.md` | `system/registries/skills-index.md` |
| Rule | `system/rules/` | `system/component-factory/runbooks/create-rule-runbook.md` | `system/component-factory/meta-skills/create-rule/SKILL.md` | `system/component-factory/templates/rule-template.md` | `system/registries/rules-index.md` |
| Guardrail | `system/guardrails/` | `system/component-factory/runbooks/create-guardrail-runbook.md` | `system/component-factory/meta-skills/create-guardrail/SKILL.md` | `system/component-factory/templates/guardrail-template.md` | Exact routed references where required |
| Runbook | `system/runbooks/` or canonical subsystem runbook folder | `system/component-factory/runbooks/create-runbook-runbook.md` | `system/component-factory/meta-skills/create-runbook/SKILL.md` | `system/component-factory/templates/runbook-template.md` | `system/registries/runbooks-index.md` |
| Template | `system/templates/` | `system/component-factory/runbooks/create-template-runbook.md` | `system/component-factory/meta-skills/create-template/SKILL.md` | `system/component-factory/templates/template-template.md` | Exact template-routing documentation |
| Artifact | `system/artifacts/` | `system/component-factory/runbooks/create-artifact-runbook.md` | `system/component-factory/meta-skills/create-artifact/SKILL.md` | `system/component-factory/templates/artifact-contract-template.md` | Applicable artifact/output contracts |
| Agent | `system/agents/<role>/AGENT.md` | `system/component-factory/runbooks/create-agent-runbook.md` | `system/component-factory/meta-skills/create-agent/SKILL.md` | `system/component-factory/templates/agent-template.md` | `system/registries/agents-index.md`; usage matrix and routed references when applicable |
| Workflow | `system/workflows/<workflow-id>-workflow.md` | `system/component-factory/runbooks/create-workflow-runbook.md` | `system/component-factory/meta-skills/create-workflow/SKILL.md` | `system/workflows/workflow-contract-template.md` | `system/registries/workflows-index.md`; runbook/rule indexes only when their entries change |

## Selection Rules

- Select exactly one component type and one operation: create, review, or
  update.
- Use the creation route only when no existing component can be safely
  extended.
- Use `system/component-factory/runbooks/review-component-runbook.md` for any
  supported existing component.
- Use `system/component-factory/runbooks/update-component-runbook.md` for a
  narrow approved update to any supported existing component.
- Do not create a governance, router, or factory Agent merely to operate
  Component Factory.

## Registry Boundary

This index routes factory work but does not replace the canonical global
registries. The selected creation or update runbook must update only the exact
global registry entries affected by the component.
