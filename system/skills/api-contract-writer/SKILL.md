---
file_type: "Skill"
primary_agents: ["BE"]
supporting_agents: []
activation_mode: "Triggered By Need"
lifecycle_stage: "System Core"
purpose: "Provide a reusable capability for BE during output generation."
---
# API Contract Writer

## Why This Skill Exists

This skill helps the BE agent define the request and response behavior that FE and downstream builders need.

## When To Use It

Use this skill when a feature needs:
- endpoint or action definitions
- request field structure
- response field structure
- visible error behavior
- FE/backend coordination without guesswork

## Inputs It Expects

- PO BRD
- BA FRS
- BE spec
- Data metric tracking plan when backend outcome events are in scope
- relevant `03-context/` files

## Output It Should Produce

A Markdown API contract that explains:
- endpoint or action name
- purpose
- request fields
- response fields
- status or result behavior
- business errors and important failure cases
- server-side tracking touchpoints when backend outcomes are needed for metrics

## Steps

1. Read the BRD and FRS to understand the user-facing business action
2. Read the BE spec to stay aligned with backend responsibilities
3. Define one contract section per important action
4. Keep request and response fields practical and reviewable
5. Expose errors that change FE behavior
6. Reference metric tracking events when backend confirmation, rejection, or dependency outcome is the source of truth
7. Flag missing rule detail when it would change contract behavior materially

## Limits

- do not optimize for framework-specific syntax
- do not invent extra endpoints beyond the approved slice
- do not hide important business errors behind vague wording
- do not invent tracking events that contradict the Data metric tracking plan
