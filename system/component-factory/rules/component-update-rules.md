---
file_type: "Factory Rule"
primary_agents: ["PO", "BA", "Architect", "Data", "BE", "UIUX", "FE", "QA", "Release"]
supporting_agents: []
activation_mode: "Always-On Shared"
lifecycle_stage: "System Core"
purpose: "Define how runtime components should be updated safely through Component Factory."
---
# Component Update Rules

Update a component safely by:
1. checking current usage first
2. identifying overlap and dependency effects
3. preferring targeted edits over broad rewrites
4. preserving naming consistency
5. producing a change report after the update

Do not update a component by:
- silently changing its scope
- rewriting downstream assumptions without review
- changing runtime behavior without checking linked runbooks, templates, or rules
