---
file_type: "Guardrail"
primary_agents: ["PO", "BA", "Architect", "Data", "BE", "UIUX", "FE", "QA", "Release"]
supporting_agents: []
activation_mode: "Always-On Shared"
lifecycle_stage: "System Core"
purpose: "Define when an agent must ask clarification instead of guessing silently."
---
# Define Clarification Rules

Ask for clarification only when a missing business rule would materially change the final output.

## Required Discovery Before Downstream Work

Before downstream artifacts expand, PO/BA must check:
- problem insight
- current pain point
- primary actor or stakeholder
- expected business value
- first-slice scope boundary
- missing or conflicting business rules

The clarification artifact must show the question decision even when there are no blocking questions.

The agent may recommend a decision, but only the user can approve downstream execution.

## Ask When

- a pricing rule is ambiguous
- an approval rule is ambiguous
- a business outcome has more than one materially different interpretation
- the problem insight or pain point is too unclear to define value
- a required actor, data field, or decision step is missing
- the first release boundary is missing or too broad to slice safely
- success language is vague enough to distort scope or acceptance criteria

## Do Not Ask When

- a reasonable default can be stated clearly in the output
- the missing detail can be recorded as an assumption without breaking the flow
- the question is useful for later but does not change safe product behavior; record it as non-blocking with its assumption

## Ambiguity Handling

- convert vague words into open questions, assumptions, or measurable interpretations
- separate `fact`, `assumption`, `blocking question`, `non-blocking question`, `recommended decision`, and `user approval status` explicitly
- classify each clarification question as `blocking`, `non-blocking`, or `assumption-backed`
- if no clarification questions are needed, state why the requirement is safe to proceed
- if a non-blocking question remains, state the assumption that allows downstream work to continue
- if more than one major ambiguity affects the same artifact, mark the package as requiring review before downstream use
- stop downstream work while `User Approval Status` is `Pending User Approval` or `Blocked`
- continue downstream work only after explicit user approval of `Approved - Proceed` or `Approved - Proceed with assumptions`
- when waiting for approval, the response must identify the exact review file, the sections to inspect, the recommended decision, and the allowed approval replies

## Skill Binding

- use `requirement-clarifier` when the source wording is too rough to structure safely
- use `ambiguity-checker-plus` when wording seems clear but business meaning is still unstable
- use `rule-coverage-checker` when a clarification changes rules across multiple artifacts
