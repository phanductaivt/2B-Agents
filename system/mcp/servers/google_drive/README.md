# Google Drive MCP / Bridge

Google Drive MCP / Bridge is used to bring approved Google Drive documents into
the local agent workspace, normalize them into agent-friendly formats, and
optionally sync reviewed outputs back to Google Drive.

## Why Agents Should Not Access The Whole Drive

Full Drive access creates unnecessary risk:

- Agents may discover unrelated private files.
- OAuth scopes become harder to audit.
- Accidental overwrite, move, share, or delete actions become more dangerous.
- Debugging remote permission issues is slower.
- Logs may accidentally expose sensitive metadata.

The workspace therefore requires folder-scoped access. Legacy mode uses
configured input/output/review folders. Source-first mode uses one configured
workspace root folder and stores project-level folder IDs in each project's
local `project.yaml`.

## Recommended Flow

```text
Google Drive input folder
-> Google Drive Desktop Sync or Local Google Drive Bridge
-> export Google Docs to Markdown/TXT
-> export Google Sheets to CSV/JSON
-> /projects/{project_name}/inputs
-> agent processing
-> /projects/{project_name}/outputs
-> /projects/{project_name}/outputs/review
-> optional approved sync to Google Drive output folder
```

## Source-First Project Workspace

New projects should use one Drive root:

```text
GOOGLE_DRIVE_WORKSPACE_ROOT_FOLDER_ID
```

Under that root, each project gets its own Drive folder:

```text
2B_Agents_Workspace
└── bbs_project
    ├── 00_Input
    ├── 01_Context
    ├── 02_Review
    ├── 03_Output
    └── 99_Archive
```

Local project state lives under:

```text
projects/google_drive/{project_id}
├── project.yaml
├── input
├── context
├── normalized
├── output
├── review
├── manifests
├── sync_state
└── logs
```

Provision a project explicitly:

```bash
python3 system/mcp/servers/google_drive/implementation/gdrive_mcp.py provision-project \
  --project-id bbs_project \
  --project-name "BBS Project"
```

Then run project-scoped commands:

```bash
python3 system/mcp/servers/google_drive/implementation/gdrive_mcp.py health --project-id bbs_project
python3 system/mcp/servers/google_drive/implementation/gdrive_mcp.py readonly --project-id bbs_project
python3 system/mcp/servers/google_drive/implementation/gdrive_mcp.py ingestion-test --project-id bbs_project
python3 system/mcp/servers/google_drive/implementation/gdrive_mcp.py dryrun-writeback --project-id bbs_project
```

`normalized`, `manifests`, `sync_state`, and `logs` are local-only. The bridge
does not mirror every local folder back to Drive.

## When To Use Google Drive Desktop Sync

Use Desktop Sync when:

- The user can manually scope which Drive folder is synced.
- Files are already available locally.
- The task is mostly read/process/write local output.
- OAuth and API export are not required for the first slice.

## When To Use Local Google Drive Bridge

Use a Local Bridge when:

- Google Docs need export to Markdown or TXT.
- Google Sheets need export to CSV or JSON.
- Folder-scoped API calls are required.
- Logs, dry-run, and review-package generation are needed.

## When To Consider Remote MCP

Consider remote Google Drive MCP only when:

- Local bridge cannot meet the requirement.
- Folder-scoped access has been proven.
- OAuth scopes are minimal and reviewed.
- Human approval is recorded.
- Read-only validation succeeds first.

## Local Implementation

A Python Local Google Drive Bridge now lives under:

```text
system/mcp/servers/google_drive/implementation
```

Codex-assisted setup is available, so you do not need to run every install and
test command manually:

```bash
python3 system/mcp/servers/google_drive/implementation/gdrive_mcp.py bootstrap
python3 system/mcp/servers/google_drive/implementation/gdrive_mcp.py setup
python3 system/mcp/servers/google_drive/implementation/gdrive_mcp.py status
```

Root Make targets are available:

```bash
make gdrive-bootstrap
make gdrive-setup
make gdrive-status
make gdrive-all-safe
```

Run health check:

```bash
python3 system/mcp/servers/google_drive/implementation/gdrive_mcp.py health
```

Run read-only ingestion test:

```bash
python3 system/mcp/servers/google_drive/implementation/gdrive_mcp.py readonly
```

Run write-back dry-run test:

```bash
python3 system/mcp/servers/google_drive/implementation/gdrive_mcp.py dryrun-writeback
```

## Read Flow

1. Load `.env`.
2. Validate folder IDs and OAuth token path.
3. Search only inside `GOOGLE_DRIVE_INPUT_FOLDER_ID`.
4. Read metadata and validate parent folder scope.
5. Export all supported Docs/Sheets or download allowed binary file types.
6. Write normalized files to `projects/{project_name}/normalized`.
7. Write the canonical manifest and audit log.

Readonly now processes all supported files found in the input folder:

- Google Docs -> Markdown.
- Google Sheets -> CSV.
- PDF/DOCX/XLSX/plain text/Markdown -> local binary/text download when Drive
  permits download.
- Unsupported files -> manifest record with `skipped_unsupported`.

PDF OCR/text extraction is not included. PDF records use
`normalized_type=binary_download` and `extraction_status=not_supported`.

Canonical manifest path:

```text
projects/{project_name}/logs/google_drive_manifest.json
```

For source-first projects the canonical manifest path is:

```text
projects/google_drive/{project_id}/manifests/google_drive_manifest.json
```

The old `readonly_test.py` entrypoint remains as a compatibility wrapper. New
usage should call `drive_readonly_local_normalize_test.py`, which means
"read-only against Google Drive, optional local normalization."

## Write-Back Flow

1. Agent writes local output under `projects/{project_name}/outputs`.
2. Output is copied or packaged under `projects/{project_name}/review`.
3. Drive write-back starts in dry-run mode.
4. Real upload is allowed only when `MCP_DRY_RUN=false` and
   `approval_status=approved`.
5. Target must be `drive_review` or `drive_output`, mapped to configured folder
   IDs.

## Dry-Run Semantics

- `MCP_DRY_RUN=true` blocks all real Google Drive upload/write-back actions.
- Local normalized artifacts are not written during dry-run unless
  `allow_local_artifacts=True`.
- If `allow_local_artifacts=False`, tools return planned paths/actions only.
- If `allow_local_artifacts=True`, tools may write local artifacts using unique
  paths only.
- Existing local files are never overwritten.
- Audit logs redact sensitive token, credential, authorization, password, key,
  and secret-like text.

## Security Warning

Do not configure My Drive root as an input, output, or review folder. Do not
store `.env`, token files, credential JSON, or client secret files in Git.
