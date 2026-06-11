# MCP Logs

This folder documents logging expectations. Do not store unsanitized runtime
logs here unless the repository ignore rules allow it and the logs contain no
secrets or sensitive document content.

## Required Fields

- Timestamp.
- Actor or agent.
- MCP server or bridge.
- Tool/action.
- Target file ID, folder ID, URL, or local path.
- Dry-run flag.
- Result.
- Non-sensitive error summary.

## Redaction Rules

- Do not log OAuth tokens.
- Do not log client secrets.
- Do not log API keys.
- Do not log full sensitive document content.
- Prefer file metadata and content hashes over raw content.

## Google Drive Logs

Every Google Drive search, metadata read, export, download, local sync, review
package creation, and optional cloud sync must create a metadata log entry.
