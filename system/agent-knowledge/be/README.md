---
file_type: "Agent Knowledge Guide"
primary_agents: ["BE"]
supporting_agents: []
activation_mode: "Optional Support"
lifecycle_stage: "Agent Support"
purpose: "Explain what optional reusable knowledge can be added for the BE agent."
---
# BE Agent Knowledge

Use this folder only when the BE agent needs extra reusable knowledge.

Examples:
- API style preferences
- backend boundary rules
- integration conventions
- security and validation patterns

Rules:
- optional only
- project-specific context in `projects/<project>/03-context/` still has higher priority
- if this folder is empty, proceed with best effort from BRD, BA outputs, rules, skills, and templates
