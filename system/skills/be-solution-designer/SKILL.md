---
file_type: "Skill"
primary_agents: ["BE"]
supporting_agents: []
activation_mode: "Triggered By Need"
lifecycle_stage: "System Core"
purpose: "Provide a reusable capability for BE during output generation."
---
# BE Solution Designer

## Why This Skill Exists

This skill helps the BE agent turn product framing and BA analysis into a practical backend design package.

## When To Use It

Use this skill when the repository needs:
- a BE spec for a feature slice
- service responsibility mapping
- validation and dependency behavior made explicit
- implementation-facing BE behavior that FE can coordinate with

## Inputs It Expects

- PO BRD
- BA FRS
- BA feature list
- BA BPMN when branching matters
- Data metric tracking plan when backend outcomes are needed for metrics
- relevant `03-context/` files

## Output It Should Produce

A Markdown BE spec that explains:
- service responsibilities
- entities or important records
- business actions
- validations and rule enforcement
- dependencies and integrations
- error and fallback behavior
- server-side tracking touchpoints when metric events depend on backend outcomes

## Steps

1. Read the BRD to understand the business slice and rule boundaries
2. Read the FRS and feature list to understand the functional behavior
3. Use BPMN only when process branching changes BE behavior
4. Group related actions into clear backend responsibilities
5. Make validation, status transitions, and dependency behavior explicit
6. Reflect server-side metric tracking touchpoints from the Data metric tracking plan when relevant
7. Flag unclear authorization, payment, tracking source, or external dependency behavior instead of inventing it

## Limits

- do not design infrastructure deeply unless the requirement truly needs it
- do not recreate the BRD or FRS
- do not invent hidden backend features outside the approved slice
- do not invent analytics payloads beyond the approved metric tracking plan
