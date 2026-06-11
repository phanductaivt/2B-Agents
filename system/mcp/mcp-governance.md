---
file_type: "MCP Governance"
primary_agents: ["Release"]
supporting_agents: ["PO", "BA", "Architect", "Data", "BE", "UIUX", "FE", "QA"]
activation_mode: "MCP Governance Only"
lifecycle_stage: "Infrastructure"
purpose: "Define how MCP work is routed without leaking into normal product-flow phases."
---
# MCP Governance

## Purpose

MCP governance controls setup, validation, use, and risk boundaries for Model Context Protocol tools. It keeps infrastructure/tooling work separate from product-flow artifact generation.

## When MCP Skills Are Used

Use `system/skills/mcp_connection_skill/SKILL.md` only when the active task is to:

- add a new MCP server
- review MCP configuration
- debug MCP connection or permissions
- write MCP validation prompts
- update MCP registry or policy
- classify MCP security and operational risk

## When MCP Skills Are Not Used

Do not use MCP skills for normal product-slice phases:

- PO product framing
- BA analysis package
- Architecture, Data, BE, UIUX, FE, QA, or Release product-flow outputs
- QA quality planning
- Release runnable verification, unless the verification explicitly depends on an approved MCP tool and the active runbook declares it

## Routing Rule

1. Start from the active workflow phase and its one active runbook.
2. If the active runbook is not MCP-specific, do not load MCP files.
3. If the task is MCP-specific, load this file, `system/mcp/mcp-registry.md`, `system/mcp/mcp_policy.md`, and `system/skills/mcp_connection_skill/SKILL.md`.
4. Load server-specific MCP files only for the target MCP server.
5. Do not read all MCP server folders.
6. Confirm the active AI Executor actually has the required MCP tool available
   and permitted in the current session.
7. Stop if the required MCP registry entry, policy, server profile, Executor
   capability, or permission is missing.
8. Before any broad repository scan, governance audit, context discovery, or
   recursive search, apply the runtime secret path exclusions defined in
   `system/mcp/mcp_policy.md`. Do not read excluded path contents during normal
   governance work.

For Filesystem/Workspace MCP, also declare the exact workspace root, allowed
paths, write restrictions, unrelated dirty-work boundary, and
approval-required actions before use.

Git MCP is currently de-scoped. Local Git CLI, IDE Git features, and GitHub
remote usage remain outside the MCP layer and are unchanged by this governance.

MCP registration does not prove availability to every AI Executor. When work
moves between Executors, follow `system/executors/executor-switching-policy.md`
and re-verify MCP availability before use.

## Approval Rule

Human approval is required before any MCP action that can delete, share, move, overwrite, publish, change permissions, access production, expand OAuth scope, or sync output back to a cloud system.

Filesystem/Workspace delete, move, out-of-scope write, secret/private-file
access, and unscoped governance overwrite require explicit user approval.

## Product-Flow Isolation Rule

Product-flow agents consume local project inputs, routed handoff outputs, and active runbook Required Context. MCP tools may help prepare or normalize those inputs only through an MCP governance task or a future MCP-specific ingestion runbook.
