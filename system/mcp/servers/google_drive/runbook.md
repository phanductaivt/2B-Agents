# Runbook: Google Drive MCP / Bridge

## Prepare Google Cloud OAuth

1. Create or select a Google Cloud project.
2. Enable the Google Drive API.
3. Configure the OAuth consent screen.
4. Create an OAuth Desktop Client for the local bridge runtime.
5. Use the minimum Drive scopes required for shared/personal Drive setups.
   Full Drive scope is used only when the Drive account/workspace is dedicated
   to Agent operations.
6. Store client ID and client secret in local environment variables or a local
   secret manager, not in Git.
7. Store OAuth tokens at `GOOGLE_DRIVE_TOKEN_PATH` outside committed source.

For this local CLI bridge, use the OAuth Desktop Client credential. A Web
Application credential is not used for the local OAuth flow in this phase unless
the architecture later changes to a web-server callback model.

Store downloaded credentials only under the ignored folder:

```text
system/mcp/servers/google_drive/implementation/credentials/
```

Recommended local filenames:

```text
google_oauth_desktop_client.json
google_oauth_web_client.json
```

Do not commit credential files, `.env`, token files, or raw OAuth responses.
Keep `MCP_DRY_RUN=true` for setup and tests.

The current dedicated Agent Drive setup may use:

```text
https://www.googleapis.com/auth/drive
```

This grants broad OAuth capability, but runtime policy still blocks direct
Agent source edits and keeps content writeback dry-run by default.

Implementation path:

```text
system/mcp/servers/google_drive/implementation
```

## Prepare Google Drive Folders

Legacy mode can still create or identify:

- Input folder: source docs only.
- Review folder: human review of generated outputs.
- Output folder: final approved outputs.

Set:

- `GOOGLE_DRIVE_INPUT_FOLDER_ID`
- `GOOGLE_DRIVE_REVIEW_FOLDER_ID`
- `GOOGLE_DRIVE_OUTPUT_FOLDER_ID`

Do not use My Drive root as any of these folders.

For source-first project mode, configure one workspace root instead:

```bash
export GOOGLE_DRIVE_WORKSPACE_ROOT_FOLDER_ID="..."
export GOOGLE_DRIVE_ALLOW_PROVISIONING="true"
```

Then provision each project. The bridge creates or reuses a Drive project
folder and the standard subfolders `00_Input`, `01_Context`, `02_Review`,
`03_Output`, and `99_Archive`.

## Set Environment Variables

Required:

```bash
export GOOGLE_DRIVE_INPUT_FOLDER_ID="..."
export GOOGLE_DRIVE_OUTPUT_FOLDER_ID="..."
export GOOGLE_DRIVE_REVIEW_FOLDER_ID="..."
export GOOGLE_DRIVE_CLIENT_ID="..."
export GOOGLE_DRIVE_CLIENT_SECRET="..."
export GOOGLE_DRIVE_TOKEN_PATH="/path/outside/git/google-drive-token.json"
export GOOGLE_DRIVE_LOCAL_SYNC_ROOT="/path/to/scoped/local/sync"
export PROJECT_INPUT_DIR="/path/to/project/inputs"
export PROJECT_OUTPUT_DIR="/path/to/project/outputs"
export MCP_DRY_RUN="true"
export MCP_LOG_LEVEL="info"
export GOOGLE_DRIVE_WORKSPACE_ROOT_FOLDER_ID="..."
export GOOGLE_DRIVE_ALLOW_PROVISIONING="false"
```

Never commit actual values.

Create local env file:

```bash
cp system/mcp/servers/google_drive/implementation/.env.example \
  system/mcp/servers/google_drive/implementation/.env
```

Then fill real values in the local `.env` only.

## Provision Source-First Project

Provisioning is an explicit folder setup action. It is not content write-back,
does not upload content, and must not require `MCP_DRY_RUN=false`.

```bash
python3 system/mcp/servers/google_drive/implementation/gdrive_mcp.py provision-project \
  --project-id bbs_project \
  --project-name "BBS Project"
```

Before running it, `.env` must have:

- `GOOGLE_DRIVE_WORKSPACE_ROOT_FOLDER_ID`
- OAuth client values and token path.
- An existing OAuth token.
- `GOOGLE_DRIVE_ALLOW_PROVISIONING=true`
- `MCP_DRY_RUN=true`

If the project folder already exists once, it is reused. If multiple matching
folders exist, provisioning stops and writes
`projects/google_drive/{project_id}/logs/provisioning_conflict_report.json`.

Provisioning writes:

- `projects/google_drive/{project_id}/project.yaml`
- `projects/google_drive/{project_id}/sync_state/source_state.json`
- `projects/project_registry.yaml`
- `projects/google_drive/{project_id}/logs/provisioning.log`

## Install Dependencies

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r system/mcp/servers/google_drive/implementation/requirements.txt
```

Automated bootstrap:

```bash
python3 system/mcp/servers/google_drive/implementation/gdrive_mcp.py bootstrap
```

Or from repo root:

```bash
make gdrive-bootstrap
```

Bootstrap creates `implementation/.venv`, installs dependencies and pytest,
creates `.env` if missing, checks `.gitignore`, creates `tokens/`, and prepares
`projects/test_gdrive` runtime folders.

## Run Setup Wizard

```bash
python3 system/mcp/servers/google_drive/implementation/gdrive_mcp.py setup
```

The wizard asks for missing folder IDs and OAuth values, hides secret input when
possible, keeps `MCP_DRY_RUN=true`, and writes `.env` locally only.

## Create OAuth Token

```bash
python3 system/mcp/servers/google_drive/implementation/src/oauth_bootstrap.py
```

If the token is missing, health check will explain that `GOOGLE_DRIVE_TOKEN_PATH`
must be created through OAuth bootstrap. It will not invent or print token
values.

## Run Health Check

```bash
python3 system/mcp/servers/google_drive/implementation/src/health_check.py
```

Health check performs:

1. Load env.
2. Validate required env variables.
3. Check OAuth token path.
4. Check input/output/review folder access.
5. List up to 10 input files.
6. Print `PASS`, `PARTIAL_PASS`, or `FAIL`.
7. Write local audit log.

Runner command:

```bash
python3 system/mcp/servers/google_drive/implementation/gdrive_mcp.py health
python3 system/mcp/servers/google_drive/implementation/gdrive_mcp.py health --project-id bbs_project
```

If env is complete but the OAuth token is missing, `health` starts the Google
OAuth desktop/local-server flow. It does not print token values.

## Run Read-Only Test

1. Start with `MCP_DRY_RUN=true`.
2. Run `gdrive.health_check`.
3. Search files in `GOOGLE_DRIVE_INPUT_FOLDER_ID`.
4. Read metadata for one approved file.
5. Export one Google Doc or Sheet in dry-run mode.
6. Confirm no cloud write occurred.

Implementation command:

```bash
python3 system/mcp/servers/google_drive/implementation/src/drive_readonly_local_normalize_test.py \
  --project-name test_gdrive \
  --max-files 5
```

For source-first projects:

```bash
python3 system/mcp/servers/google_drive/implementation/gdrive_mcp.py readonly --project-id bbs_project
```

This reads from `project.yaml -> google_drive.input_folder_id`, writes
normalized artifacts under `projects/google_drive/bbs_project/normalized`, and
writes the manifest under `projects/google_drive/bbs_project/manifests`.

This test may write normalized local files under `projects/test_gdrive`; it does
not upload to Google Drive. It is read-only with respect to Drive. Local
artifacts are written only through unique paths and do not overwrite existing
files.

Readonly processes every supported file in the input folder:

- Google Docs -> Markdown.
- Google Sheets -> CSV.
- PDF/DOCX/XLSX/plain text/Markdown -> local download.
- Unsupported MIME types -> skipped manifest record.

PDF OCR is not implemented; PDF download records include
`extraction_status=not_supported`.

Plan only, without local normalized files:

```bash
python3 system/mcp/servers/google_drive/implementation/src/drive_readonly_local_normalize_test.py \
  --project-name test_gdrive \
  --max-files 5 \
  --no-local-artifacts
```

## Run Write-Back Dry-Run Test

```bash
python3 system/mcp/servers/google_drive/implementation/src/writeback_dry_run_test.py \
  --project-name test_gdrive
```

This test performs no Drive upload. It verifies that write-back is blocked by
dry-run unless approval and `MCP_DRY_RUN=false` are both present.

Runner command:

```bash
python3 system/mcp/servers/google_drive/implementation/gdrive_mcp.py dryrun-writeback
python3 system/mcp/servers/google_drive/implementation/gdrive_mcp.py dryrun-writeback --project-id bbs_project
```

## Run All Safe Checks

```bash
python3 system/mcp/servers/google_drive/implementation/gdrive_mcp.py all-safe
```

`all-safe` runs bootstrap, env validation, health, Drive read-only local
normalization, write-back dry-run, and ingestion test. It stops safely if env,
OAuth, dependency, or permission checks fail.

For a project-scoped Google Drive daily flow:

```bash
python3 system/mcp/servers/google_drive/implementation/gdrive_mcp.py project-all-safe --project-id bbs_project
```

This runs status, health, readonly pull/normalize, ingestion/routing, and
writeback dry-run. If `00_Input` is empty, it reports `READY_FOR_INPUT` instead
of treating the project as failed.

## Read Setup Status

```bash
python3 system/mcp/servers/google_drive/implementation/gdrive_mcp.py status
```

Status prints dependency, env, token, last log, security, next command, and
final readiness without printing secrets.

## OAuth Troubleshooting

- `invalid_client`: verify OAuth client ID and client secret.
- `redirect_uri_mismatch`: verify `GOOGLE_DRIVE_REDIRECT_URI` in Google Cloud
  and `.env`.
- `access_denied`: confirm the selected Google account has access to the
  configured folders.
- `scope_not_granted`: confirm requested scopes are approved on the consent
  screen.
- `token_path_invalid`: use `implementation/tokens/google_drive_token.json`.
- `missing_env`: run `gdrive_mcp.py setup`.
- `missing_dependency`: run `gdrive_mcp.py bootstrap`.

## Understand MCP_DRY_RUN

- `MCP_DRY_RUN=true` blocks all real Google Drive uploads.
- For tools that write local normalized files, dry-run returns planned paths
  unless `allow_local_artifacts=True`.
- When local artifacts are allowed, the bridge writes unique filenames and never
  overwrites existing files.
- Review package creation also honors dry-run and writes only when
  `allow_local_artifacts=True` or `MCP_DRY_RUN=false`.

## Check Log Redaction

Audit logs are written to:

```text
projects/{project_name}/logs/google_drive_mcp_audit.log
```

Verify logs do not contain:

- access tokens
- refresh tokens
- client secrets
- authorization headers
- bearer values
- raw credentials
- passwords
- API keys

## Check Canonical Manifest

The canonical manifest is:

```text
projects/{project_name}/logs/google_drive_manifest.json
```

It is an append/merge metadata store updated with an atomic temp-file replace.
It should contain:

```json
{
  "version": "1.0",
  "project_name": "test_gdrive",
  "updated_at": "...",
  "records": []
}
```

If the manifest becomes invalid JSON, the bridge backs it up as:

```text
google_drive_manifest.corrupt_backup.<timestamp>.json
```

Then it creates a new canonical manifest. Rerunning readonly is safe because
normalized artifacts use unique paths and the manifest deduplicates identical
`source_file_id + action + local_path` records.

## Test PDF Download

1. Put a PDF inside `GOOGLE_DRIVE_INPUT_FOLDER_ID`.
2. Run:

```bash
python3 system/mcp/servers/google_drive/implementation/gdrive_mcp.py readonly
```

3. Confirm a PDF local artifact exists under `projects/test_gdrive/normalized`.
4. Confirm manifest has `action=download_file`,
   `normalized_type=binary_download`, and `extraction_status=not_supported`.

## Debug OAuth Errors

- Confirm Google Drive API is enabled.
- Confirm OAuth client type matches the local bridge flow.
- Confirm redirect URI or local callback is configured correctly.
- Confirm token path is writable and outside Git.
- Delete the local token only when re-authentication is intended.
- Do not print token contents.

## Debug Permission Errors

- Confirm the file is inside the configured input, output, or review folder.
- Confirm the OAuth account can access that folder.
- Confirm folder IDs are not My Drive root.
- Confirm the bridge validates parent folders before action.

## Debug Export Errors

- Confirm MIME type is Google Doc or Google Sheet.
- Confirm requested export format is supported.
- For Sheets, confirm the target tab exists.
- Check file size and API quota.
- Retry dry-run before real export.

## Rollback

- For local outputs, remove or archive generated review artifacts if approved.
- For cloud outputs, use Drive version history or remove the synced copy only
  with human approval.
- Never delete source input files as part of rollback.

## Read Logs

Logs should show:

- Timestamp.
- Tool/action.
- Source file ID or folder ID.
- Destination local path or Drive folder ID.
- Dry-run flag.
- Result.
- Non-sensitive error summary.

Logs must not show OAuth tokens, client secrets, or sensitive document content.
