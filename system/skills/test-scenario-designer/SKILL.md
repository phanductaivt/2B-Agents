---
file_type: "Skill"
primary_agents: ["QA"]
supporting_agents: []
activation_mode: "Triggered By Need"
lifecycle_stage: "System Core"
purpose: "Provide a reusable capability for QA during output generation."
---
# Test Scenario Designer

## Why This Skill Exists

This skill helps the QA agent define practical scenario-level coverage before detailed test cases are written.

## When To Use It

Use this skill when a feature slice needs:
- happy-path coverage
- negative-path coverage
- dependency and validation coverage
- visible quality risk framing across BA, BE, and FE behavior

## Inputs It Expects

- PO BRD
- BA FRS
- acceptance criteria
- BE spec
- API contract
- wireframe and FE output when available
- Data metric tracking plan when measurement is in scope

## Output It Should Produce

A Markdown test scenario set that explains:
- scenario name
- purpose
- path type
- main expected result
- tracking verification focus when relevant
- related source artifacts

## Steps

1. Read the BRD and FRS to identify the approved business slice
2. Identify the happy path first
3. Add negative, validation, authorization, dependency, tracking verification, and exception scenarios that materially affect quality
4. Keep each scenario mapped to the same approved slice
5. Flag unclear expected behavior instead of inventing hidden rules

## Limits

- do not jump straight into long step-by-step cases before the scenario map is clear
- do not add fantasy scenarios with no business or implementation relevance
- do not treat undefined behavior as implicitly passed
- do not turn every analytics event into a QA case; focus on events needed for key metrics and guardrails
