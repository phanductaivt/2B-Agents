---
file_type: "Runbook"
primary_agents: ["PO", "BA", "Architect", "Data", "BE", "UIUX", "FE", "QA", "Release"]
supporting_agents: []
activation_mode: "Triggered By Workflow"
lifecycle_stage: "System Core"
purpose: "Resolve a critical ambiguity before downstream work continues."
reads: ["requirement or upstream artifact", "03-context/", "system/guardrails/define-clarification-rules.md"]
produces: ["clarified source artifact or clarified output section"]
---
# Resolve Clarification

Use this runbook when a requirement is missing a business rule that materially changes the output.

## Required Skills

- no single skill is always required

## Skill Routing

- use `requirement-clarifier` when the wording is rough and needs a cleaner requirement statement
- use `ambiguity-checker-plus` when wording looks clear but business meaning is still unstable
- use `rule-coverage-checker` when the gap affects rule consistency across multiple artifacts
- route architecture, data, implementation, or runnable verification gaps to the owning agent before continuing

## Steps

1. Identify the missing rule or ambiguous business choice
2. Classify it as one of:
   - missing actor
   - missing business value
   - missing rule or policy
   - missing scope boundary
   - missing exception behavior
   - missing dependency or data semantics
3. Record the assumption, open question, or blocked decision inside the relevant artifact set
4. If the ambiguity changes feature slicing or handoff safety, mark the package as requiring review before downstream use
5. If the user answers, update every affected BA output, not only the first file where the gap appeared
