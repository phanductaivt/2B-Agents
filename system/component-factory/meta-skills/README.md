---
file_type: "Factory Index"
primary_agents: ["PO", "BA", "Architect", "Data", "BE", "UIUX", "FE", "QA", "Release"]
supporting_agents: []
activation_mode: "Manual Navigation"
lifecycle_stage: "System Core"
purpose: "Explain the factory-only meta-skills used to create and control AI operating components."
---
# Meta-Skills

`meta-skills/` contains factory-only skills.

They are not runtime delivery skills.

Use them to:
- create new components
- create bounded instruction-defined Agents
- create executor-neutral workflow contracts
- review component quality
- update components safely
- audit overlap, naming, and dependency integrity

Every meta-skill must:
- inspect existing runtime folders first
- avoid duplicates
- follow Component Factory rules
- follow Component Factory guardrails
- use the matching factory runbook
- use the matching factory template
- produce the right creation or review report

Creation routes:
- Agent: `system/component-factory/meta-skills/create-agent/SKILL.md`
- Workflow: `system/component-factory/meta-skills/create-workflow/SKILL.md`
- All supported types: `system/component-factory/component-types-index.md`

Meta-skills here should never:
- delete existing runtime files
- move existing runtime files
- rename existing runtime files
- overwrite existing files without explicit approval
