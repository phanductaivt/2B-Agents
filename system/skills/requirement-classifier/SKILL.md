---
file_type: "Skill"
primary_agents: ["PO"]
supporting_agents: []
activation_mode: "Triggered By Need"
lifecycle_stage: "System Core"
purpose: "Provide a reusable capability for PO during output generation."
---
# Requirement Classifier

## Name

Requirement Classifier

## Purpose

Help the PO agent classify requirement statements into business, stakeholder, solution, and transition requirements so the team can reason about scope and handoff more clearly.

## When To Use

Use this skill when:
- the requirement contains mixed statements
- the team needs cleaner ownership between PO and BA
- the BRD must show requirement types explicitly

## Input Format

- raw requirement
- project context
- clarified notes
- optional BRD draft

## Output Format

- business requirements
- stakeholder requirements
- solution requirements
- transition requirements
- short rationale where classification is not obvious

## Step-by-Step Logic

1. Extract the major requirement statements.
2. Group each statement by intent:
   - business requirement
   - stakeholder requirement
   - solution requirement
   - transition requirement
3. Flag mixed statements that contain more than one type.
4. Rewrite only when needed to make the classification understandable.
5. Record any uncertain classifications as assumptions or open questions.

## Constraints

- do not force every sentence into one type if it clearly mixes concerns
- do not rewrite product intent beyond what is needed for classification
- keep the classification understandable to non-technical reviewers

## Expected Markdown Outputs

- a `Requirement Classification` section inside `brd.md`
