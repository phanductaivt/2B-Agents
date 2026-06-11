# Google Drive Bridge Strategy

## Architecture Decision

The initial architecture will not use a remote Google Drive MCP directly for
agent document processing.

The workspace will prefer:

1. Google Drive Desktop Sync for manually scoped local access.
2. Local Google Drive Bridge for API-based folder-scoped export and sync.
3. Remote Google Drive MCP only after the local pattern is validated and a
   human approves the scope.

## Processing Flow

```text
Google Drive Folder
-> Local Google Drive Bridge
-> Normalize Markdown/CSV/JSON
-> /projects/{project_name}/inputs
-> Agent Processing
-> /projects/{project_name}/outputs
-> Review
-> Optional Sync back to Google Drive
```

## Reasons

- OAuth complexity is easier to control locally.
- Folder-scoped permission boundaries are clearer.
- File overwrite risk is lower when outputs pass through review folders.
- Google Docs and Sheets export behavior can be normalized before agents read
  content.
- Remote MCP debugging is harder when auth, scope, export, and agent behavior
  fail at the same time.

## Required Guardrails

- Folder IDs must come from environment variables.
- Tokens must live outside committed source.
- Every operation must be logged.
- Dry-run must be supported.
- Source files must remain unchanged.
- Review folder is mandatory before final sync.
