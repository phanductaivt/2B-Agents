---
file_type: "MCP Test Prompts"
primary_agents: ["Release"]
supporting_agents: ["QA"]
activation_mode: "MCP Governance Only"
lifecycle_stage: "Infrastructure"
purpose: "Provide safe prompts for MCP validation without running product-flow phases."
---
# MCP Test Prompts

Use these prompts only for MCP setup, validation, or debugging. Do not use them inside normal product-flow runbooks.

## Read-Only Validation Prompt

```text
Validate the MCP server in read-only mode.

MCP:
- <mcp-name>

Allowed action:
- list available tools
- run one smallest safe read-only action

Rules:
- Do not write, delete, share, move, overwrite, publish, or change permissions.
- Do not print secrets or sensitive content.
- Record only non-sensitive evidence.
- Stop if the server, tool list, permission, or read-only action fails.
```

## Configuration Review Prompt

```text
Review this MCP configuration for governance compliance.

Files:
- system/mcp/mcp-registry.md
- system/mcp/mcp_policy.md
- system/skills/mcp_connection_skill/SKILL.md
- <target MCP config/profile file>

Report:
- required scopes
- risk level
- missing environment variables
- unsafe permissions
- approval requirements
- read-only validation plan
```

## Debug Prompt

```text
Debug the MCP connection without changing configuration yet.

MCP:
- <mcp-name>

Failure:
- <non-sensitive failure summary>

Rules:
- Do not print secrets.
- Do not broaden scope.
- Do not mark the MCP approved without actual read-only evidence.
- Recommend the smallest next step.
```

## Filesystem/Workspace MCP Test Route

Use:
- `system/mcp/servers/filesystem/test_prompts.md`

Required coverage:
- capability detection
- read-only status/scope check
- scoped file read
- scoped diff review
- permission denial
- prohibited action
- handoff evidence

Do not read secret/private files, write outside approved paths, delete files,
overwrite unscoped governance files, or touch unrelated dirty files during
validation.
