# MCP Decision Matrix

## Priority Order

When several MCPs can solve the same task, use this order:

1. Filesystem/Workspace MCP for explicitly required scoped local file access.
2. Normal declared-context file access when no MCP capability is needed.
3. Google Drive Desktop Sync for Drive files already synced locally.
4. Local Google Drive Bridge for folder-scoped export/download/sync.
5. Remote Google Drive MCP only after approval and folder-scoped validation.
6. Playwright MCP only when the task requires browser interaction or UI
   verification.

## Matrix

| Task | Preferred MCP | Use when | Approval required |
|---|---|---|---|
| Read or write local project artifacts | Filesystem/Workspace MCP | Active task explicitly requires MCP file access and the Executor verifies configured scope. | Required for delete, move, secret/private-file access, overwrite, governance overwrite outside scoped task, or writing outside approved project scope. |
| Process Google Docs or Sheets | Google Drive Desktop Sync or Local Bridge | Source is in configured Drive input folder and must be normalized locally. | Required for cloud write-back, overwrite, move, delete, or scope expansion. |
| Export Google Docs to Markdown/TXT | Local Google Drive Bridge | Document is in `GOOGLE_DRIVE_INPUT_FOLDER_ID`. | Required if exporting from outside configured folder. |
| Export Google Sheets to CSV/JSON | Local Google Drive Bridge | Spreadsheet is in `GOOGLE_DRIVE_INPUT_FOLDER_ID`. | Required if exporting from outside configured folder. |
| Sync agent output back to Drive | Local Google Drive Bridge | Output has passed review and target is configured output folder. | Always required before final sync. |
| Browser UI smoke test | Playwright MCP | Need navigation, click/type, screenshot, console, or visible state evidence. | Required for production-impacting flows. |
| Inspect website or app behavior | Playwright MCP | Need actual browser observation. | Required for authenticated, sensitive, or production flows. |

## High-Risk Rule

If a task can delete, share, move, overwrite, publish, change permissions, expose
sensitive data, or affect production, the AI Executor must request human approval
before execution.

Filesystem/Workspace secret/private-file access, delete/move, out-of-scope
writes, and unscoped governance overwrite are high-risk.

## Git Boundary

Git MCP is de-scoped. Use local Git CLI, IDE Git features, or GitHub outside
the MCP layer only when the active task and permission profile allow them.

## Google Drive Rule

Do not use a remote Google Drive MCP to browse the whole Drive. The approved
pattern is folder-scoped input/output/review plus local normalization.

If a task processes Google Drive files, route it through an Ingestion Agent,
Router Agent, or the Local Google Drive Bridge first. BA, UX, FE, QA, and
Release agents should consume normalized local files unless direct Drive access
is explicitly required and approved.
