# Validators

Validators check output quality before it is shared or published.

This framework includes validators for:
- ambiguity
- completeness
- consistency
- template alignment

They help BA-led teams catch common issues early.

In this project, validators mainly review the Markdown files written to `projects/<project-name>/_ops/generated/`.

Common issues now checked include:
- vague wording and unclear assumptions
- missing business rules
- non-testable acceptance criteria
- inconsistent story and criteria wording
- feature list hierarchy that does not align with BRD and FRS
- BA outputs that do not stay aligned across BPMN, BRD, FRS, user story, and acceptance criteria
