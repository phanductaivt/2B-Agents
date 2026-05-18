---
file_type: "Skill"
primary_agents: ["BA", "PO"]
supporting_agents: []
activation_mode: "Triggered By Need"
lifecycle_stage: "System Core"
purpose: "Provide a reusable capability for BA, PO during output generation."
---
# Ambiguity Checker Plus

## Name

Ambiguity Checker Plus

## Purpose

Detect material ambiguity in a requirement or BA artifact before the ambiguity spreads into BRD, FRS, feature slicing, or handoff.

## When To Use

Use this skill when:
- the requirement looks clear on the surface but may hide weak business meaning
- a BA artifact needs an ambiguity review before downstream handoff
- vague words, missing actors, or missing rule boundaries could distort scope

## Input Format

- raw requirement note or BA artifact
- optional business context
- optional existing assumptions or questions

## Output Format

- ambiguity findings grouped by type
- impacted artifact or decision area
- recommended action
- explicit facts, assumptions, and open questions

## Step-by-Step Logic

1. Check for missing actor, value, rule, scope, release, data, permission, and dependency meaning.
2. Highlight vague wording such as `simple`, `fast`, `better`, `support`, or `user-friendly`.
3. Separate business facts from assumptions and wishes.
4. Explain which ambiguities materially change scope, flow, or acceptance criteria.
5. Recommend whether to ask, assume, or block handoff.

## Constraints

- do not invent missing answers
- focus on ambiguity that changes business meaning or delivery behavior
- keep findings concrete and reviewable

## Expected Markdown Outputs

- ambiguity findings section in `clarification.md`
- optional support input to the BRD or FRS open questions section
