---
file_type: "Executor Contract"
primary_agents: []
supporting_agents: ["PO", "BA", "Architect", "Data", "BE", "UIUX", "FE", "QA", "Release"]
activation_mode: "Always-On Shared"
lifecycle_stage: "System Core"
purpose: "Define the minimum behavior required from any AI Executor operating this repository."
---
# AI Executor Contract

## Purpose

This contract makes repository execution independent of a specific AI model,
client, or vendor.

## Required Behavior

Every AI Executor must:

1. Treat Agents as instruction-defined roles, not separate AI models.
2. Select the active workflow, identify its active phase, then load the one
   active runbook and context just in time. Record an explicit standalone
   operation only when no registered workflow applies.
3. Activate only the Agent declared by the active workflow phase. Do not infer
   an Agent when the phase declares `Active Agent: None`.
4. Follow the active Agent's ownership and forbidden-responsibility boundaries.
5. Load only required rules, guardrails, skills, templates, inputs, and handoff
   outputs.
6. Respect user approval gates and stop conditions.
7. Preserve unrelated existing work and avoid destructive changes without
   explicit approval.
8. Record actual validation evidence and never invent command or tool results.
9. State uncertainty, missing context, unavailable capabilities, and permission
   limitations instead of guessing.
10. Update `system/handoff/latest-handoff.md` before pausing incomplete work or
    switching to another Executor.

## Capability Declaration

Before using tools or continuing handed-off work, the Executor must identify:

- Executor name or client.
- Available file read/write capability.
- Available command execution capability.
- Available network or browser capability.
- Available MCP tools.
- Executor limitations.
- Current permission profile.

Use `system/executors/executor-capability-template.md` when a formal capability
record is needed.

Capability availability is session-specific. A tool used by a previous
Executor must not be assumed available to the current Executor.

## Agent Activation Contract

When activating an Agent, the Executor must:

- identify the active Agent separately from the Executor identity
- load the exact `system/agents/<role>/AGENT.md`
- follow the active runbook's `## Required Context`
- preserve output ownership and handoff boundaries
- stop if the active Agent, runbook, or required input cannot be identified

The Executor must not silently switch Agent roles to bypass a boundary or
approval gate.

## Tool And MCP Contract

- MCP is a governed tool layer, not an Agent.
- Confirm an MCP is available to the current Executor before routing work to it.
- Follow `system/mcp/mcp-governance.md` and the target server contract.
- Do not broaden permissions because a previous Executor had broader access.
- For Filesystem/Workspace MCP, declare configured root, allowed read/write
  paths, secret/private-file restrictions, and delete/overwrite boundaries.
- Git MCP is de-scoped. Do not infer that local Git CLI, IDE Git features, or
  GitHub access are MCP capabilities.
- When a required tool is unavailable, report the limitation and use a safe
  non-tool fallback only when the active runbook allows it.

## Evidence And Claims

An Executor must distinguish:

- observed facts
- repository instructions
- assumptions
- recommendations
- actual tool or command evidence
- unverified claims

Do not claim that a file was changed, a command passed, an MCP worked, or an
output is approved without actual evidence.

## Handoff Contract

Before ending or pausing incomplete work, the Executor must record:

- active Executor
- active Agent
- active workflow, phase, and runbook
- active project and task ID
- available MCP tools and Executor limitations
- permission profile
- files created or modified
- validation performed
- risks and uncertainties
- recommended next step

The next Executor must read the handoff, verify its own capabilities, and
reconfirm the active task before editing.
