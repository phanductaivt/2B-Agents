---
file_type: "Skill"
primary_agents: ["BA", "QA"]
supporting_agents: []
activation_mode: "Triggered By Need"
lifecycle_stage: "System Core"
purpose: "Provide a reusable capability for BA, QA during output generation."
---
# Exception Scenario Expander

## Name

Exception Scenario Expander

## Purpose

Expand non-happy-path scenarios so the BA package covers realistic failure, restriction, and fallback behavior before design and implementation start.

## When To Use

Use this skill when:
- the requirement currently describes only the happy path
- a branch, exception, or fallback could materially affect delivery
- the BA package must cover realistic support, access, or data issues

## Input Format

- FRS
- business rules
- acceptance criteria
- BPMN or process notes

## Output Format

- exception scenarios
- missing-data cases
- unauthorized or blocked cases
- unavailable dependency cases
- invalid or out-of-scope state cases

## Step-by-Step Logic

1. Review the normal flow.
2. Enumerate where the flow can fail, branch, block, or degrade.
3. Add missing-data, unauthorized, unavailable-service, invalid-state, and out-of-scope cases.
4. Check that each exception belongs in FRS, acceptance criteria, or BPMN.
5. Flag any exception that still lacks business guidance.

## Constraints

- do not create fantasy failures that have no business relevance
- prioritize scenarios that change user outcome, support burden, or implementation logic
- keep exception wording observable and testable

## Expected Markdown Outputs

- stronger `frs.md`
- stronger `acceptance-criteria.md`
- optional support input to `process-bpmn.md`
