---
file_type: "Factory Index"
primary_agents: ["PO", "BA", "Architect", "Data", "BE", "UIUX", "FE", "QA", "Release"]
supporting_agents: []
activation_mode: "Manual Navigation"
lifecycle_stage: "System Core"
purpose: "Explain the factory runbooks used to create, review, and update runtime components."
---
# Component Factory Runbooks

Use these runbooks when performing controlled component work inside `system/component-factory/`.

Each runbook includes:
- purpose
- when to use
- prerequisites
- steps
- validation checklist
- expected output
- recovery or rollback note

## Creation Routes

- Agent: `system/component-factory/runbooks/create-agent-runbook.md`
- Workflow: `system/component-factory/runbooks/create-workflow-runbook.md`
- Other supported component types:
  `system/component-factory/component-types-index.md`

Use `system/component-factory/runbooks/review-component-runbook.md` or
`system/component-factory/runbooks/update-component-runbook.md` for an existing
Agent or Workflow. Component Factory phases use `Active Agent: None`.
