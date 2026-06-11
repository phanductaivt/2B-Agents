---
file_type: "Factory Artifact"
primary_agents: ["PO", "BA", "Architect", "Data", "BE", "UIUX", "FE", "QA", "Release"]
supporting_agents: []
activation_mode: "On-Demand Reference"
lifecycle_stage: "System Core"
purpose: "Provide the standard quality checklist used when judging a runtime component through Component Factory."
---
# Component Quality Checklist

- [ ] component type is correct
- [ ] purpose is clear
- [ ] naming is consistent
- [ ] scope is not overloaded
- [ ] dependency claims were checked
- [ ] overlap risk was checked
- [ ] no unsafe file operation occurred
- [ ] exact affected registry entries are aligned
- [ ] Agent identity, ownership, boundaries, inputs, outputs, dependencies,
      handoff, and usage examples are complete when type is Agent
- [ ] Workflow ID, phases, one Active Agent or `None`, one Active Runbook,
      routing, gates, recovery, handoff, and done criteria are complete when
      type is Workflow
- [ ] required report is produced
