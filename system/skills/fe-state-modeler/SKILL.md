---
file_type: "Skill"
primary_agents: ["FE"]
supporting_agents: []
activation_mode: "Triggered By Need"
lifecycle_stage: "System Core"
purpose: "Provide a reusable capability for FE when the UI slice needs explicit state planning."
---
# FE State Modeler

## Why This Skill Exists

This skill helps the FE agent make UI states explicit before HTML implementation starts guessing hidden transitions.

## When To Use It

Use this skill when the repository needs:
- multiple user-visible states for one screen
- loading, success, empty, validation, or business-error handling
- explicit transition mapping between BE responses and FE display states

## Inputs It Expects

- BA FRS
- BA feature list
- BE API contract
- BE spec
- UIUX wireframe
- relevant `03-context/`

## Output It Should Produce

A clear FE state view that explains:
- state names
- trigger conditions
- what the user sees in each state
- how the state exits

## Steps

1. Read the BA and BE outputs that define business flow and response behavior.
2. Identify the minimum state set needed for the slice.
3. Separate data-loading states from business-rule states.
4. Map each BE outcome or validation outcome to a visible FE state.
5. Flag missing behavior when the FE state cannot be derived safely.

## Limits

- do not invent business rules
- do not create decorative states with no user or delivery value
- do not hide unclear response behavior behind generic placeholders
