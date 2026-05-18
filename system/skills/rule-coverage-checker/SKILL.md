---
file_type: "Skill"
primary_agents: ["BA", "QA"]
supporting_agents: []
activation_mode: "Triggered By Need"
lifecycle_stage: "System Core"
purpose: "Provide a reusable capability for BA, QA during output generation."
---
# Rule Coverage Checker

## Name

Rule Coverage Checker

## Purpose

Check that important business rules appear consistently across BRD, FRS, acceptance criteria, BPMN branches, and feature slicing.

## When To Use

Use this skill when:
- business rules are critical to the feature behavior
- multiple BA artifacts may describe the same rule differently
- the team needs confidence that downstream work will not miss a policy or restriction

## Input Format

- BRD
- FRS
- acceptance criteria
- BPMN
- feature list

## Output Format

- rule inventory
- coverage findings
- missing or inconsistent rule references
- recommended fixes

## Step-by-Step Logic

1. List the core business rules from the BA package.
2. Check whether each rule appears where it should matter.
3. Compare BPMN branches with FRS alternative flows.
4. Flag rules that are missing, conflicting, or implied only indirectly.
5. Recommend the smallest artifact updates needed for consistency.

## Constraints

- focus on business rules that materially change behavior
- do not treat wording differences as defects unless meaning changes
- call out missing coverage explicitly

## Expected Markdown Outputs

- rule coverage notes inside `clarification.md` or `frs.md`
