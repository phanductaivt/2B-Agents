---
file_type: "Skill"
primary_agents: ["PO"]
supporting_agents: []
activation_mode: "Triggered By Need"
lifecycle_stage: "System Core"
purpose: "Provide a reusable capability for PO during output generation."
---
# BACCM Product Framer

## Name

BACCM Product Framer

## Purpose

Help the PO agent frame product work using BACCM so the team understands the change, need, solution intent, stakeholder, value, and context before BA analysis expands the package.

## When To Use

Use this skill when:
- the product problem is still broad or ambiguous
- the team needs a strong business framing before BA analysis
- requirement direction is clear enough to discuss change and value, but not yet structured

## Input Format

- business requirement
- stakeholder notes
- project context
- optional market research

## Output Format

- Change
- Need
- Solution
- Stakeholder
- Value
- Context

## Step-by-Step Logic

1. Define the change the business wants to make.
2. Clarify the need or problem driving that change.
3. Describe the intended solution direction at a product level.
4. Identify the stakeholders affected by the change.
5. State the value the business expects.
6. Describe the surrounding context that constrains or influences the work.

## Constraints

- keep the framing business-facing
- do not turn BACCM into detailed functional specification
- if a BACCM element is unclear, mark it as assumption or open question

## Expected Markdown Outputs

- a `BACCM Framing` section inside `brd.md`
