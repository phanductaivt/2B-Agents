# Server Profile: Google Drive MCP / Bridge

| Field | Value |
|---|---|
| Server name | Google Drive MCP / Google Drive Bridge |
| Category | Cloud Workspace |
| Status | Restricted / Prefer Local Bridge |
| Owner | Workspace owner |
| Allowed Agents | PO, BA, Product, UX, QA, Release; Architect/FE when source docs are required |
| Main use cases | Read folder-scoped Drive files, export Google Docs/Sheets, sync normalized input locally, write review packages, optionally sync reviewed output back. |
| Disabled use cases | Full Drive crawl, delete, share, move, unapproved overwrite, unapproved final sync, production credential handling. |
| Risk level | High |
| Required environment variables | `GOOGLE_DRIVE_INPUT_FOLDER_ID`, `GOOGLE_DRIVE_OUTPUT_FOLDER_ID`, `GOOGLE_DRIVE_REVIEW_FOLDER_ID`, `GOOGLE_DRIVE_CLIENT_ID`, `GOOGLE_DRIVE_CLIENT_SECRET`, `GOOGLE_DRIVE_TOKEN_PATH`, `GOOGLE_DRIVE_LOCAL_SYNC_ROOT`, `PROJECT_INPUT_DIR`, `PROJECT_OUTPUT_DIR`, `MCP_DRY_RUN`, `MCP_LOG_LEVEL` |
| Dependencies | Google Cloud OAuth client, Google Drive API, local bridge runtime or Google Drive Desktop Sync, ignored token storage |
