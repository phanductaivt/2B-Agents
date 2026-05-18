---
file_type: "Agent Knowledge Guide"
primary_agents: ["QA"]
supporting_agents: []
activation_mode: "Optional Support"
lifecycle_stage: "Agent Support"
purpose: "Explain what optional reusable knowledge can be added for the QA agent."
---
# QA Agent Knowledge

Use this folder for QA-specific supporting knowledge that improves coverage quality and release judgment.

Examples:
- test strategy preferences
- risk taxonomy
- severity definitions
- regression heuristics
- environment or dependency test patterns

Rules:
- optional only
- project-specific context in `projects/<project>/03-context/` still has higher priority
- if this folder is empty, proceed with best effort from BRD, BA outputs, BE outputs, FE output, rules, guardrails, skills, and templates
