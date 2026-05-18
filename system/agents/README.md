---
file_type: "Agent Index"
primary_agents: ["PO", "BA", "Architect", "Data", "BE", "UIUX", "FE", "QA", "Release"]
supporting_agents: []
activation_mode: "Manual Navigation"
lifecycle_stage: "System Core"
purpose: "Explain the active agents and point readers to agent definitions and usage mapping."
---
# Agents

This folder defines the active role guidance for the AI Operating Repository.

Key navigation:
- `define-agent-usage-matrix.md`

Active agents:
- BA
- BE
- Architect
- Data
- QA
- PO
- UIUX
- FE
- Release

Typical ownership:
- PO creates the BRD first
- BA creates the analysis package
- Architect creates architecture, NFR, and security outputs
- Data creates data model, state transition, SQLite schema planning, and metric tracking plans
- BE creates API and service design from the BRD and BA package
- UIUX creates the wireframe
- FE creates the review UI and runnable frontend using design and BE contracts
- QA creates the quality review package using PO, BA, Data, BE, Design, and FE outputs
- Release verifies local runnable status and writes run instructions
