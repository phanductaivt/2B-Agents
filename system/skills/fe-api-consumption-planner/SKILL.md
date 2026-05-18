---
file_type: "Skill"
primary_agents: ["FE"]
supporting_agents: []
activation_mode: "Triggered By Need"
lifecycle_stage: "System Core"
purpose: "Provide a reusable capability for FE when API usage and FE dependency flow need explicit planning."
---
# FE API Consumption Planner

## Why This Skill Exists

This skill helps the FE agent plan how the UI will consume BE actions and responses without guessing request order or dependency flow.

## When To Use It

Use this skill when the repository needs:
- multiple API-dependent steps
- request/response sequencing
- dependency planning between UI actions and BE behavior
- explicit mapping from user action to BE action

## Inputs It Expects

- BA FRS
- BE API contract
- BE spec
- UIUX wireframe
- FE technical design notes when they exist

## Output It Should Produce

A clear FE API usage plan that explains:
- which user action triggers which BE action
- what request data is needed
- what response data is used in the UI
- what failure paths change the user flow

## Steps

1. Read the wireframe and user-facing flow first.
2. Map each important user action to a BE action or endpoint.
3. Identify the response fields that actually drive FE rendering.
4. Surface where sequencing, retry, blocking, or fallback behavior matters.
5. Flag unclear dependencies before implementation starts.

## Limits

- do not invent new endpoints
- do not assume hidden response data
- do not ignore failure cases that change the FE path
