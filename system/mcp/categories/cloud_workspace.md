# Cloud Workspace MCP Category

Use this category for cloud document systems such as Google Drive.

Primary server or bridge:

- `servers/google_drive`

Preferred pattern:

1. Google Drive Desktop Sync if the target folder is already safely synced.
2. Local Google Drive Bridge for folder-scoped export/download/sync.
3. Remote Google Drive MCP only after explicit approval and validation.

Cloud workspace rules:

- No full Drive access.
- No broad crawling.
- No delete, share, move, or overwrite without approval.
- Export cloud-native files to local normalized formats before processing.
- Send outputs to review before any final sync.
