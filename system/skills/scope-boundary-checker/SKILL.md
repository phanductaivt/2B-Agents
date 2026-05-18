---
file_type: "Skill"
primary_agents: ["PO", "BA"]
supporting_agents: []
activation_mode: "Triggered By Need"
lifecycle_stage: "System Core"
purpose: "Provide a reusable capability for PO, BA during output generation."
---
# Scope Boundary Checker

## Name

Scope Boundary Checker

## Purpose

Force the BA package to show what is included, excluded, and deferred so the first release stays small, understandable, and buildable.

## When To Use

Use this skill when:
- the requirement contains several ideas mixed together
- the first release slice feels too large
- stakeholders request a feature but out-of-scope boundaries are not visible

## Input Format

- clarification
- BRD
- FRS
- feature list
- optional release notes

## Output Format

- in-scope items
- out-of-scope items
- deferred items
- first release slice guidance
- scope risk notes

## Step-by-Step Logic

1. Identify the main business outcome.
2. Remove items that do not support the first release outcome directly.
3. Mark what is in scope, out of scope, and deferred.
4. Check that the feature list reflects the same boundary.
5. Flag any feature group that is too broad to review or build safely.

## Constraints

- do not confuse related ideas with committed scope
- keep release-one slice narrow and testable
- explain scope cuts in business language

## Expected Markdown Outputs

- scope notes inside `brd.md`
- optional support input to `clarification.md`
