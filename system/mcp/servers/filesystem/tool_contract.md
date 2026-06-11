# Tool Contract: Filesystem MCP

Expected capabilities depend on the filesystem MCP implementation, but the
workspace allows only these behavior classes.

| Tool class | Purpose | Input | Output | Allowed scope | Risk | Failure cases |
|---|---|---|---|---|---|---|
| list | List approved directories. | Path under workspace root. | File/folder metadata. | `WORKSPACE_ROOT` only. | Low | Path outside scope, permission denied. |
| read | Read local project files. | File path under workspace root. | File content or metadata. | Approved task/project paths; secret/private files denied by default. | Medium | File missing, binary unsupported, secret/private path, permission denied. |
| write | Create output artifacts. | Target path and content. | Created/updated file result. | Output/review folders. | Medium | Parent missing, dry-run, overwrite blocked. |
| edit | Apply approved modifications. | Target path and patch. | Updated file result. | Approved task/project paths; governance paths only for scoped governance work. | High | Conflict, unrelated dirty file, overwrite blocked, source input protected. |
| search | Search local files. | Query and path scope. | Matching paths/snippets. | Approved project folders. | Low | Path outside scope, too broad query. |
| delete/move | Remove or relocate a file. | Exact approved path and action. | Result metadata. | None by default. | Critical | Explicit approval missing, unrelated dirty file, recovery unclear. |

Default example request:

```json
{
  "path": "/absolute/workspace/project/inputs"
}
```

Default example response:

```json
{
  "status": "ok",
  "items": ["requirements.md", "backlog.csv"]
}
```

## Contract Rules

- Verify the active AI Executor's Filesystem/Workspace MCP capability before
  use.
- Read only exact task-relevant paths.
- Treat secret/private paths and unrelated dirty files as denied by default.
- Write only to exact approved project paths.
- Governance file writes require a scoped governance task.
- Delete or move requires explicit user approval and a recovery approach.
- Record actual path/action/result evidence in the canonical handoff.
