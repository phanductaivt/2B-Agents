# MCP Workspace Governance

`system/mcp` is the workspace control layer for Model Context Protocol (MCP)
servers and local bridge integrations used by BA, PO, Product, UX, FE, QA, and
Release agents.

This folder defines which MCPs may be used, how agents should choose them, what
actions are allowed, what requires human approval, and how Google Drive content
is safely moved into a local project workspace before agent processing.

## How To Read This Folder

Start with these files:

- `mcp-governance.md`: JIT routing and governance rules for MCP work.
- `mcp-registry.md`: Phase 4 registry entrypoint; links to the detailed
  existing registry.
- `mcp-test-prompts.md`: standard safe prompts for validating MCP setup.
- `mcp_registry.md`: source of truth for approved, restricted, pending, and
  deferred MCP servers.
- `mcp_policy.md`: workspace-wide security and operational rules.
- `mcp_decision_matrix.md`: routing guide for choosing the right MCP.
- `servers/{server_name}/`: server-specific profile, contract, security,
  tests, and runbook.
- `prompts/`: reusable prompts for health checks, debugging, routing, and
  Google Drive document processing.
- `templates/`: reusable structure for adding future MCP servers.
- `logs/README.md`: logging rules and local log folder guidance.

## How To Choose The Right MCP

1. Read the task goal and identify the target: local file, cloud document,
   browser UI, developer tool, communication system, or database.
2. Check `mcp_decision_matrix.md`.
3. Confirm the server status and risk in `mcp_registry.md`.
4. Apply `mcp_policy.md`.
5. Use the narrowest MCP or bridge that can complete the task.
6. Prefer local workspace processing over direct cloud processing.
7. For high-risk actions, stop and request human approval.

## Product-Flow Boundary

MCP work is infrastructure/tooling governance. Product-flow runbooks for PO,
BA, Architect, Data, BE, UIUX, FE, QA, and Release must not load MCP skills or
MCP files unless the active runbook is explicitly an MCP governance/setup/test
task. Normal product-slice phases should consume local project files and routed
handoff outputs, not MCP configuration material.

## How To Add A New MCP

1. Create `servers/{new_server}/`.
2. Copy the templates from `templates/`.
3. Fill in server profile, tool contract, security policy, test prompts, and
   runbook.
4. Add a safe placeholder-only entry to `mcp_config.example.json`.
5. Add a local-only sample to `mcp_config.local.example.json` if needed.
6. Register the server in `mcp_registry.md`.
7. Add category guidance under `categories/` if the server introduces a new
   category.
8. Run read-only validation first.
9. Keep status as `Pending` or `Restricted` until actual tool evidence exists.

## How To Test MCP

Use prompts in `prompts/` and server-specific checks in
`servers/{server}/test_prompts.md`.

Minimum test sequence:

1. Load or start the server.
2. List available tools.
3. Run one smallest safe read-only action.
4. Confirm output with actual evidence.
5. Verify denied actions are blocked or require approval.
6. Record non-sensitive metadata in logs.

Do not claim an MCP works unless an actual tool call or bridge command produced
evidence.

Current governed foundations include:

- Filesystem/Workspace MCP for scoped local file access
- Google Drive MCP / Bridge
- Playwright MCP

Registration is not availability. The active AI Executor must declare and
verify each MCP in the current session before use.

Git MCP is currently de-scoped. Local Git CLI, IDE Git features, and the
existing GitHub remote may still be used outside the MCP layer when the active
task and permission profile allow them. De-scoping Git MCP does not remove or
change Git, repository history, branches, remotes, or GitHub access.

## Security Principles

- Agents must not access an entire Google Drive.
- Google Drive access must be scoped to configured input, output, and review
  folders.
- Do not use full Drive scope unless a future human-approved architecture
  decision explicitly allows it.
- Do not hardcode credentials, OAuth tokens, API keys, or secrets.
- Do not commit OAuth tokens to Git.
- Apply the runtime secret path exclusions in `mcp_policy.md` before any broad
  repository scan, governance audit, context discovery, or recursive search.
- Do not read or expose secret/private files through Filesystem/Workspace MCP
  by default.
- Preserve unrelated dirty files during all Filesystem/Workspace MCP work.
- Do not delete, share, move, or overwrite files unless a human explicitly
  approves the exact action.
- Use dry-run mode for first execution and risky write operations.
- Log operations, but log metadata only when content may be sensitive.
- All generated outputs must go to a review folder before they are considered
  final.
- Production environments are restricted by default.

## Google Drive To Local Workspace Flow

Recommended flow:

```text
Google Drive input folder
-> Google Drive Desktop Sync or Local Google Drive Bridge
-> normalize Google Docs to Markdown/TXT
-> normalize Google Sheets to CSV/JSON
-> /projects/{project_name}/inputs
-> agent processing in local workspace
-> /projects/{project_name}/outputs
-> /projects/{project_name}/outputs/review
-> optional human-approved sync back to Google Drive output folder
```

Remote Google Drive MCP should only be considered after the local bridge path is
validated and folder-scoped permissions are confirmed.

## Migration Note

Old structure:

```text
system/mcp
├── README.md
├── categories/filesystem_mcp.md
├── categories/google_drive_mcp.md
├── categories/playwright_mcp.md
├── mcp_config.example.json
├── mcp_policy.md
├── mcp_prompt_library.md
└── mcp_registry.md
```

Migration mapping:

| Old file | New location or role |
|---|---|
| `README.md` | Rewritten as the main governance overview. |
| `mcp_registry.md` | Kept as the source of truth and expanded. |
| `mcp_policy.md` | Kept and expanded with approval, logging, overwrite, cloud, and rollback rules. |
| `mcp_config.example.json` | Kept and rewritten with placeholder-only filesystem, Google Drive bridge, and Playwright examples. |
| `mcp_prompt_library.md` | Split into focused files under `prompts/`. The old monolithic file should be archived outside this target tree if historical reference is needed. |
| `categories/filesystem_mcp.md` | Replaced by `categories/local_resource.md` and `servers/filesystem/*`. |
| `categories/google_drive_mcp.md` | Replaced by `categories/cloud_workspace.md` and `servers/google_drive/*`. |
| `categories/playwright_mcp.md` | Replaced by `categories/browser_automation.md` and `servers/playwright/*`. |

Post-migration tests:

1. Confirm the new tree exists.
2. Confirm no old category files remain as active guidance.
3. Confirm registry status for Google Drive is `Restricted / Prefer Local Bridge`.
4. Confirm config examples contain placeholders only.
5. Run Filesystem read-only health check.
6. Run Google Drive Bridge dry-run health check.
7. Run Playwright safe URL health check.
