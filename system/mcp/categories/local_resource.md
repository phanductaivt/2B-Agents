# Local Resource MCP Category

Use this category for local filesystem access and project workspace artifacts.

Primary server:

- `system/mcp/servers/filesystem/`

Use local resource MCP when:

- Reading local inputs.
- Writing agent outputs.
- Verifying generated files.
- Preparing review packages.
- Running local documentation or release checks.

Filesystem/Workspace MCP is capability-bound to the active AI Executor. Confirm
the configured root and exact read/write scope before use.

Do not use local resource MCP to:

- Read outside approved workspace scope.
- Modify credentials or secret files.
- Delete files without approval.
- Overwrite source inputs without approval.
- Read or expose secret/private files by default.
- Overwrite governance files without a scoped governance task.
- Touch unrelated dirty files.
