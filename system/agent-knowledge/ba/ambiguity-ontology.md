---
file_type: "Agent Knowledge"
primary_agents: ["BA"]
supporting_agents: []
activation_mode: "Optional Support"
lifecycle_stage: "Agent Support"
purpose: "Provide optional supporting knowledge for the BA agent when extra depth is needed."
---
# BA Ambiguity Ontology

Use this note to help the BA agent reduce ambiguity systematically instead of relying on instinct alone.

## Ambiguity Types To Check

- actor ambiguity
  - unclear primary user, stakeholder, owner, or approver
- problem ambiguity
  - requested feature is clear but business pain or expected value is weak
- scope ambiguity
  - in-scope and out-of-scope boundaries are not visible
- release ambiguity
  - first release slice is not defined or is too large
- rule ambiguity
  - business policy, approval logic, eligibility, or status rules are missing or conflicting
- flow ambiguity
  - main path exists but branches, exception paths, or end states are unclear
- data ambiguity
  - source, freshness, ownership, visibility, or required fields are unclear
- permission ambiguity
  - access control, authorization, or ownership boundaries are missing
- success ambiguity
  - words such as `better`, `faster`, `simple`, `support`, or `user-friendly` are used without measurable meaning
- dependency ambiguity
  - external system, team, approval, or operational dependency is present but underspecified

## Response Strategy

- if ambiguity materially changes scope or behavior, turn it into an `open question`
- if a reasonable temporary interpretation exists, mark it as an `assumption`
- if the ambiguity can be bounded safely, state the chosen default and its impact
- if the ambiguity blocks design or implementation, stop and mark the package as requiring review before downstream use

## Vocabulary Discipline

Always separate:
- `fact`
- `assumption`
- `open question`
- `decision`
- `constraint`
- `out-of-scope`

Do not collapse these categories into one narrative paragraph.
