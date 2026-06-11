# Runbook: Filesystem/Workspace MCP

## Startup And Routing Conditions

1. Confirm the active task requires Filesystem/Workspace MCP rather than normal
   declared-context file access.
2. Confirm the active AI Executor declares the MCP available.
3. Load `system/mcp/mcp-governance.md`, `system/mcp/mcp_policy.md`,
   `system/mcp/mcp_registry.md`, and the Filesystem server contract.
4. Declare the exact workspace root, allowed paths, and permission profile.
5. Identify unrelated dirty files and secret/private path restrictions.

## Setup

1. Install Node.js.
2. Configure the filesystem MCP with the narrowest `WORKSPACE_ROOT`.
3. Set `MCP_DRY_RUN=true` for first validation.
4. Set `MCP_LOG_LEVEL=info`.

## Read-Only Test

1. Start the MCP client.
2. List tools.
3. List the workspace root.
4. Read `system/mcp/README.md`.

## Scoped Write

1. Confirm the exact approved project output/review path.
2. Check whether the target exists or is dirty.
3. Use dry-run when supported.
4. Stop before overwrite, governance mutation, or unrelated-file changes unless
   the scoped task and required approval allow them.
5. Record actual evidence in `system/handoff/latest-handoff.md`.

## Debug

- If server load fails, check Node.js and package install.
- If path access fails, confirm the configured root.
- If writes fail, check dry-run mode and folder permissions.

## Rollback

Remove generated test files from review/output folders after confirming they are
not needed and receiving explicit approval for deletion. Do not delete source
inputs or unrelated files.
