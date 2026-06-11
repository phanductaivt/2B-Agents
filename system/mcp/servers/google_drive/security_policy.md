# Security Policy: Google Drive MCP / Bridge

- Do not request full Drive access unless a future approved architecture
  decision explicitly allows it.
- Access only configured folders:
  - `GOOGLE_DRIVE_INPUT_FOLDER_ID`
  - `GOOGLE_DRIVE_OUTPUT_FOLDER_ID`
  - `GOOGLE_DRIVE_REVIEW_FOLDER_ID`
- Source-first projects should configure only
  `GOOGLE_DRIVE_WORKSPACE_ROOT_FOLDER_ID` in `.env`; project subfolder IDs are
  stored in `projects/google_drive/{project_id}/project.yaml`.
- Provisioning may create Drive folders only when the user explicitly runs
  `provision-project` and `GOOGLE_DRIVE_ALLOW_PROVISIONING=true`.
- Provisioning is not content write-back. It must not upload documents, delete,
  share, move, or overwrite Drive files.
- Do not delete files.
- Do not share files.
- Do not move files.
- Do not overwrite files without human approval.
- Do not commit OAuth tokens, API keys, client secrets, or credential files.
- Broad scans, governance audits, context discovery, and recursive searches
  must apply the runtime secret path exclusions in
  `system/mcp/mcp_policy.md`. Path/status checks must not read credential
  contents.
- Do not log sensitive file content.
- Log only required metadata: timestamp, operation, file ID, file name, MIME
  type, source folder, destination path, dry-run flag, result, and non-sensitive
  error summary.
- Dry-run mode is required for first execution and before cloud write-back.
- All output must be written to a review folder before it can be considered
  final.
- Sync from review to final/output folder requires human approval.
- When `MCP_DRY_RUN=true`, the bridge must not upload or write to Google Drive.
- When `MCP_DRY_RUN=true`, local artifact writes are allowed only when the tool
  call explicitly sets `allow_local_artifacts=True` or the script is documented
  as a local normalization test.
- Local artifact writes must always use unique paths.
- Local artifact writes must not overwrite existing files.
- Audit logs must redact token, client secret, access token, refresh token,
  authorization header, bearer value, password, API key, credential payload, and
  sensitive exception text.
- Real Drive upload is allowed only when all are true:
  - `MCP_DRY_RUN=false`
  - `approval_status=approved`
  - target is `drive_review` or `drive_output`
  - target folder ID is configured
- Local normalized files are written only under
  `projects/{project_name}/normalized`.
- Local agent outputs are written only under `projects/{project_name}/outputs`
  or `projects/{project_name}/review`.
- For source-first projects, local artifacts are written only under
  `projects/google_drive/{project_id}`. `normalized`, `manifests`,
  `sync_state`, and `logs` are local-only.
