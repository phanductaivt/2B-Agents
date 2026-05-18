---
file_type: "Rule"
primary_agents: ["PO", "BA", "Architect", "Data", "BE", "UIUX", "FE", "QA", "Release"]
supporting_agents: []
activation_mode: "Always-On Shared"
lifecycle_stage: "System Core"
purpose: "Define ownership boundaries and collaboration rules between active agents."
---
# Define Agent Design

Detailed role guidance lives under:
- `system/agents/`
- `system/agent-knowledge/`

Quick role map:
- PO = BRD, product framing, market research, BACCM framing, requirement classification, scope guidance, and prioritization
- BA = business analysis package built on top of business input, project context, and PO BRD framing
- Architect = architecture note, NFR review, security review, and runnable system shape
- Data = data model, state transition, SQLite schema plan, seed-data expectations, and metric tracking plan
- BE = API contract, service behavior, data handling, integration-facing backend design, and FastAPI implementation
- QA = test scenarios, test cases, quality risk visibility, and release-readiness review
- UIUX = wireframe and interaction framing
- FE = React frontend implementation and review UI that reflects design and BE contracts
- Release = run instructions, smoke checks, runnable-system verification, and local readiness evidence

Ownership rule:
- PO owns framing and prioritization artifacts
- PO owns the BRD and requirement classification
- BA owns analysis and functional handoff artifacts
- Architect owns architecture, NFR, and security constraints before implementation
- Data owns persistence, state design, and feature-health metric tracking handoff
- BE owns implementation-facing BE contracts, service design artifacts, and backend code
- QA owns quality review artifacts and test coverage thinking
- FE owns frontend implementation, not backend decision-making
- Release owns runnable verification evidence, not product scope
- if BA analysis conflicts with PO framing, raise clarification instead of silently changing policy or scope
