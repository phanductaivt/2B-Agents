# Filesystem MCP

Filesystem/Workspace MCP provides scoped local workspace file access for an
active AI Executor. Its availability and permission scope are session-specific;
registration does not prove that every Executor can use it.

Use it for reading inputs, writing local outputs, checking generated artifacts,
and preparing review packages. It must be configured with the narrowest
workspace root that still supports the project.

Source inputs should be treated as immutable unless the user approves an exact
edit.

It must not read or expose secrets by default, write outside approved project
paths, delete files without explicit approval, overwrite governance files
without a scoped governance task, or touch unrelated dirty files.

Canonical governance:

- `system/mcp/mcp-governance.md`
- `system/mcp/mcp_policy.md`
- `system/mcp/mcp_registry.md`
- `system/mcp/servers/filesystem/security_policy.md`
- `system/executors/executor-contract.md`
- `system/handoff/README.md`
