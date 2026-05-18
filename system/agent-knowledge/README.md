---
file_type: "Agent Knowledge Index"
primary_agents: ["PO", "BA", "Architect", "Data", "BE", "UIUX", "FE", "QA", "Release"]
supporting_agents: []
activation_mode: "Manual Navigation"
lifecycle_stage: "Agent Support"
purpose: "Explain where optional per-agent knowledge can be stored and how it should be used."
---
# Agent Knowledge

This folder stores optional supporting knowledge by agent role.

Rules:
- agent knowledge is optional
- if empty, Codex proceeds with best effort
- if files exist, Codex should read them as supporting context
- project-specific knowledge in `projects/<project>/03-context/` always has priority

Current notable BA support:
- `ba/ambiguity-ontology.md`
- `ba/question-strategy.md`

Current notable BE support:
- `be/README.md`

Current notable Architect support:
- `architect/README.md`

Current notable Data support:
- `data/README.md`

Current notable Release support:
- `release/README.md`

Current notable QA support:
- `qa/README.md`

Current notable PO support:
- `po/baccm-framing.md`
- `po/market-research-policy.md`
- `po/requirement-types.md`
