# Server Profile: Filesystem MCP

| Field | Value |
|---|---|
| Server name | Filesystem/Workspace MCP |
| Category | Local Resource |
| Governance status | Approved |
| Availability | Executor-bound; must be verified in the current session |
| Owner | Workspace owner |
| Allowed Agents | PO, BA, Product, UX, Architect, Data, BE, FE, QA, Release |
| Main use cases | Read local project files, write output artifacts, verify folder structure, package review outputs. |
| Disabled use cases | Secret/private-file access by default, broad home-directory access, delete without approval, writes outside approved paths, unscoped governance overwrite, unrelated dirty-file changes. |
| Risk level | High |
| Required environment variables | `WORKSPACE_ROOT`, `MCP_DRY_RUN`, `MCP_LOG_LEVEL` |
| Dependencies | `@modelcontextprotocol/server-filesystem`, Node.js, approved local path scope |

## Allowed Workspace Paths

- exact configured `WORKSPACE_ROOT`
- exact project paths approved by the active task
- exact governance paths only when a scoped governance task requires them

## Startup And Routing

Use only when the active task requires scoped file access, the AI Executor
declares current-session availability, the configured root is known, and the
requested paths fit the active permission profile.
