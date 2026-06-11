# MCP Policy

## Allowed Actions

- Read local project files inside approved workspace paths.
- Create or update project artifacts in approved input/output/review folders.
- Read Google Drive metadata and file content only from configured folder IDs.
- Export Google Docs to Markdown or TXT through a local bridge or approved tool.
- Export Google Sheets to CSV or JSON through a local bridge or approved tool.
- Run browser automation on local/dev or explicitly approved safe URLs.
- Record operation metadata in logs.
- Run dry-run checks before writes or sync operations.
- Use Filesystem/Workspace MCP only for exact approved workspace/project paths
  after the active AI Executor declares configured root and permission scope.

## Denied Actions

- Accessing an entire Google Drive.
- Using full Drive scope unless explicitly approved in a future architecture
  decision.
- Deleting cloud or local files without explicit human approval.
- Sharing files or changing permissions without explicit human approval.
- Moving files without explicit human approval.
- Overwriting source files or cloud files without explicit human approval.
- Committing OAuth tokens, API keys, client secrets, or credentials.
- Printing secrets or sensitive document content into logs.
- Running production-impacting browser flows without approval.
- Filesystem/Workspace MCP access to secret/private files by default.
- Filesystem/Workspace writes outside approved project paths, unscoped
  governance overwrites, or unrelated dirty-file changes.

## Human Approval Rules

Human approval is required before:

- Delete, share, move, publish, permission-change, or overwrite operations.
- Syncing local output back to Google Drive final/output folders.
- Using a new MCP server not listed in `mcp_registry.md`.
- Expanding Google Drive scope beyond configured folder IDs.
- Running against production systems.
- Writing to any folder outside the approved project workspace.
- Filesystem/Workspace secret/private-file access, delete/move, scope expansion,
  or governance overwrite outside a scoped governance task.

Approval must identify the target, action, expected result, and rollback plan.

## Credential Rules

- Store credentials only in user-local secret stores, local ignored config, or
  environment variables.
- Do not hardcode credentials in docs, code, prompts, or examples.
- `mcp_config.example.json` and `mcp_config.local.example.json` must use
  placeholders only.
- OAuth token paths must point outside committed source or to ignored local
  paths.
- If a secret is discovered, do not print it; report that it must be rotated.

## Runtime Secret Path Exclusion Rules

Broad repository scans, governance audits, context discovery, and recursive
searches must exclude these runtime-secret and dependency paths before
execution:

- `system/mcp/servers/google_drive/implementation/tokens/**`
- `system/mcp/servers/google_drive/implementation/credentials/**`
- `system/mcp/servers/google_drive/implementation/.env`
- `**/.env`
- `**/tokens/**`
- `**/credentials/*client*.json`
- `**/.venv/**`

Path existence, ignore status, and tracking status may be checked without
reading file contents. Content under an excluded path may be inspected only
when a separately approved credential-specific task explicitly requires it.
Even then, secret values must never be printed, copied, summarized, transformed,
or placed in prompts, logs, reports, outputs, or handoff documents.

## Logging Rules

- Log timestamp, actor/tool, action, target ID/path, dry-run status, result, and
  non-sensitive error summaries.
- Log metadata, not full document content, when content may contain business,
  personal, financial, legal, or confidential information.
- Store local logs under ignored runtime paths or `system/mcp/logs/` only if
  they are sanitized examples.
- Every Google Drive read, export, download, write, and sync operation must be
  logged.

## File Overwrite Rules

- Source input files are immutable by default.
- Generated outputs must be versioned or written to a review folder.
- Overwrite requires explicit approval naming the exact file.
- If overwrite is approved, create a backup or keep a recoverable previous
  version when technically possible.

## Git MCP Scope

Git MCP is currently de-scoped and is not an approved, pending, planned, or
governed MCP capability. Local Git CLI, IDE Git features, and the existing
GitHub remote remain available outside the MCP layer under the active task's
normal permission and safety constraints.

## Filesystem/Workspace MCP Rules

- Availability and configured root must be verified by the active AI Executor.
- Read only exact task-relevant paths; secret/private files are denied by
  default.
- Write only exact approved project paths.
- Governance files may be written only during a scoped governance task.
- Delete, move, scope expansion, secret/private-file access, overwrite, and
  out-of-project writes require explicit approval.
- Preserve unrelated dirty files.

## Cloud Access Rules

- Google Drive access is folder-scoped.
- Required folder variables:
  - `GOOGLE_DRIVE_INPUT_FOLDER_ID`
  - `GOOGLE_DRIVE_OUTPUT_FOLDER_ID`
  - `GOOGLE_DRIVE_REVIEW_FOLDER_ID`
- Agents may not broad-crawl Drive.
- Remote Google Drive MCP is lower priority than Google Drive Desktop Sync or a
  Local Google Drive Bridge.
- Cloud writes must go to review first, then wait for approval before final
  sync.

## Production Environment Rules

- Production systems are restricted by default.
- Read-only production checks require clear user intent.
- Any production write, submit, payment, send, publish, permission, or data
  mutation requires approval.

## Rollback Principle

Every write or sync workflow must identify how to reverse or recover the
change. Prefer append-only outputs, review folders, versioned filenames, and
dry-run previews.
