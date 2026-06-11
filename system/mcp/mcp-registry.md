---
file_type: "MCP Registry Entrypoint"
primary_agents: ["Release"]
supporting_agents: ["PO", "BA", "Architect", "Data", "BE", "UIUX", "FE", "QA"]
activation_mode: "MCP Governance Only"
lifecycle_stage: "Infrastructure"
purpose: "Provide the Phase 4 MCP registry entrypoint without moving the existing MCP registry."
---
# MCP Registry

Use this file for MCP routing decisions. The detailed server registry remains in `system/mcp/mcp_registry.md` for compatibility with existing MCP documentation.

## MCP Scope

MCP tools are infrastructure/tooling integrations used to read, write, automate, or validate external or local resources through approved tool boundaries.

They are not product-flow artifact generators. Do not route `system/skills/mcp_connection_skill/SKILL.md` into BA, UIUX, FE, BE, QA, or Release product-slice runbooks unless the user explicitly asks for MCP setup, MCP validation, or MCP governance work.

## Current Registry Source

- Detailed registry: `system/mcp/mcp_registry.md`
- Governance rules: `system/mcp/mcp-governance.md`
- Policy rules: `system/mcp/mcp_policy.md`
- Test prompts: `system/mcp/mcp-test-prompts.md`

## Registered MCP Categories

| Category | Existing detail file | Use when | Do not use when |
| --- | --- | --- | --- |
| Local resource | `system/mcp/categories/local_resource.md` | Filesystem/Workspace MCP is explicitly required for controlled scoped file access. | A normal runbook can read the local file directly through declared Required Context. |
| Cloud workspace | `system/mcp/categories/cloud_workspace.md` | Cloud documents must be normalized into local project inputs. | Product-flow agents can work from local normalized files. |
| Browser automation | `system/mcp/categories/browser_automation.md` | UI smoke evidence, screenshots, or browser state are required. | QA is only planning tests and not executing browser evidence. |
| Communication | `system/mcp/categories/communication.md` | Future email/chat/calendar MCPs are approved. | No approved communication MCP exists. |
| Database | `system/mcp/categories/database.md` | Future database MCPs are approved. | Product data design can be done from routed artifacts. |
| Developer tools | `system/mcp/categories/developer_tools.md` | A future developer-tool MCP is explicitly approved through governance. | Git MCP is de-scoped and normal Git/GitHub use does not require MCP routing. |

## Registered MCP Foundations

| MCP | Detailed Contract | Governance Status | Availability Rule |
| --- | --- | --- | --- |
| Filesystem/Workspace MCP | `system/mcp/servers/filesystem/` | Approved | Must be verified and scoped by the active AI Executor. |
| Google Drive MCP / Bridge | `system/mcp/servers/google_drive/` | Restricted / Prefer Local Bridge | Existing policy unchanged. |
| Playwright MCP | `system/mcp/servers/playwright/` | Approved | Existing policy unchanged; availability remains Executor-bound. |

Git MCP is de-scoped. This does not remove or change local Git, IDE Git
features, repository history, the GitHub remote, or normal Git/GitHub usage
outside the MCP layer.

## New MCP Registration Rule

Register a new MCP only through an MCP governance task. Use `system/skills/mcp_connection_skill/SKILL.md` to prepare the classification, risk review, safe config proposal, validation prompt, and rollout recommendation. Keep product-flow runbooks unchanged unless a new MCP-specific runbook is intentionally added later.
