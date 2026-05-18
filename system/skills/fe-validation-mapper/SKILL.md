---
file_type: "Skill"
primary_agents: ["FE"]
supporting_agents: []
activation_mode: "Triggered By Need"
lifecycle_stage: "System Core"
purpose: "Provide a reusable capability for FE when input and validation behavior must be mapped clearly."
---
# FE Validation Mapper

## Why This Skill Exists

This skill helps the FE agent translate BA rules and BE validation behavior into visible input handling and user feedback.

## When To Use It

Use this skill when the repository needs:
- field-level validation behavior
- form rules that must be visible before submission
- error message mapping based on BA rules or BE responses

## Inputs It Expects

- BA FRS
- BA acceptance criteria
- BE API contract
- BE spec when validation behavior is complex
- UIUX wireframe

## Output It Should Produce

A clear FE validation view that explains:
- what fields or interactions need validation
- where validation happens
- what the user sees when validation fails
- which cases are FE-only vs BE-confirmed

## Steps

1. Read BA and BE artifacts for rule-sensitive fields and actions.
2. List every field or interaction that has validation significance.
3. Separate pre-submit, submit-time, and post-response validation outcomes.
4. Map each validation failure to user-visible feedback.
5. Flag unclear cases instead of inventing error semantics.

## Limits

- do not invent new validation rules
- do not collapse multiple error meanings into one vague message
- do not assume FE can enforce a rule that only BE can confirm
