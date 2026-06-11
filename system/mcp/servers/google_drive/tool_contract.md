# Tool Contract: Google Drive MCP / Local Bridge

The current implementation is a Python Local Google Drive Bridge under
`system/mcp/servers/google_drive/implementation`. Tool names below describe the
approved behavior contract implemented by `implementation/src/tools.py`.

All tools must enforce folder-scoped access, metadata-only logging, no
delete/share/move behavior, and no uncontrolled overwrite.

## Source-First Project Mapping

Commands may run in legacy mode or source-first project mode:

- Legacy mode: no `--project-id`; folders come from
  `GOOGLE_DRIVE_INPUT_FOLDER_ID`, `GOOGLE_DRIVE_REVIEW_FOLDER_ID`, and
  `GOOGLE_DRIVE_OUTPUT_FOLDER_ID`.
- Source-first mode: `--project-id` is provided; folder IDs come from
  `projects/google_drive/{project_id}/project.yaml`.

Source-first local paths:

```text
projects/google_drive/{project_id}/normalized
projects/google_drive/{project_id}/output
projects/google_drive/{project_id}/review
projects/google_drive/{project_id}/manifests/google_drive_manifest.json
projects/google_drive/{project_id}/logs
```

## `gdrive.provision_project`

- Type: explicit provisioning action.
- Purpose: Create or reuse Drive project folders under
  `GOOGLE_DRIVE_WORKSPACE_ROOT_FOLDER_ID` and write local project mapping.
- Input:
  ```json
  {
    "project_id": "bbs_project",
    "project_name": "BBS Project"
  }
  ```
- Output:
  ```json
  {
    "status": "success",
    "project_yaml": "projects/google_drive/bbs_project/project.yaml",
    "drive_project_root_folder_id": "folder-id",
    "content_upload_attempted": false
  }
  ```
- Drive folders created/reused: `00_Input`, `01_Context`, `02_Review`,
  `03_Output`, `99_Archive`.
- Allowed scope: workspace root folder only.
- Requires approval: command must be called explicitly and
  `GOOGLE_DRIVE_ALLOW_PROVISIONING=true`.
- Dry-run rule: `MCP_DRY_RUN` remains true. Provisioning folder creation is not
  content write-back. It must not upload content.
- Denied behavior: no delete, share, move, overwrite, or content upload.
- Failure cases: missing root folder ID, missing token, duplicate Drive folder
  conflict, permission denied.

## `gdrive.health_check`

- Type: read-only diagnostic.
- Purpose: Validate config, OAuth/token path, folder IDs, and read-only listing.
- Input: none, or optional env path for CLI.
- Output:
  - `status`: `PASS | PARTIAL_PASS | FAIL`
  - `config_check`
  - `auth_check`
  - `folder_check`
  - `readonly_list_check`
  - `issues`
  - `recommended_fixes`
  - `log_path`
- Allowed scope: configured folder IDs only; in source-first mode, configured
  folder IDs are read from project `project.yaml`.
- Requires approval: no.
- Risk level: low.
- Failure cases: missing env, missing token, missing dependency, OAuth failure,
  permission denied, folder inaccessible.

## `gdrive.search_files`

- Type: read-only.
- Purpose: Search files inside the configured input folder. In source-first
  mode this is `project.yaml -> google_drive.input_folder_id`.
- Input:
  ```json
  {
    "query": "requirements",
    "mime_type": "application/vnd.google-apps.document",
    "max_results": 10,
    "modified_after": "2026-01-01T00:00:00Z"
  }
  ```
- Output:
  ```json
  {
    "files": [
      {
        "file_id": "file-id",
        "file_name": "Requirements",
        "mime_type": "application/vnd.google-apps.document",
        "modified_time": "2026-05-25T00:00:00Z",
        "web_view_link": "https://...",
        "suggested_processing_method": "export_google_doc_to_md_or_txt"
      }
    ]
  }
  ```
- Allowed scope: input folder only.
- Requires approval: no.
- Risk level: medium.
- Failure cases: OAuth failure, permission denied, query too broad, API quota.

## `gdrive.get_file_metadata`

- Type: read-only.
- Purpose: Read metadata for one file.
- Input:
  ```json
  { "file_id": "file-id" }
  ```
- Output:
  ```json
  {
    "file_id": "file-id",
    "file_name": "Backlog",
    "mime_type": "application/vnd.google-apps.spreadsheet",
    "size": null,
    "modified_time": "2026-05-25T00:00:00Z",
    "owner": "Owner display name if available",
    "capabilities": {},
    "suggested_processing_method": "export_google_sheet_to_csv_or_json"
  }
  ```
- Allowed scope: metadata is validated before processing actions.
- Requires approval: no.
- Risk level: low.
- Failure cases: file not found, permission denied, OAuth failure.

## `gdrive.export_google_doc`

- Type: read from Drive, write local normalized file.
- Purpose: Export Google Docs to TXT or Markdown-like text without editing the
  source file.
- Input:
  ```json
  {
    "file_id": "doc-id",
    "output_format": "md",
    "project_name": "test_gdrive",
    "dry_run": null,
    "allow_local_artifacts": false
  }
  ```
- Output:
  ```json
  {
    "local_output_path": "projects/test_gdrive/normalized/Requirements__doc-id__normalized.md",
    "export_status": "success",
    "source_file_id": "doc-id",
    "source_file_name": "Requirements"
  }
  ```
- Allowed scope: Google Docs inside `GOOGLE_DRIVE_INPUT_FOLDER_ID`.
- Requires approval: no for local normalized export.
- Dry-run behavior: uses `config.dry_run` when `dry_run` is null. If dry-run is
  active and `allow_local_artifacts=false`, returns planned path/action only.
  If `allow_local_artifacts=true`, writes a unique local normalized file and
  never overwrites existing files.
- Risk level: medium.
- Failure cases: file outside input folder, unsupported format, export API
  failure, local write conflict.

## `gdrive.export_google_sheet`

- Type: read from Drive, write local normalized file.
- Purpose: Export Google Sheets to CSV or JSON without editing the source file.
- Input:
  ```json
  {
    "file_id": "sheet-id",
    "output_format": "csv",
    "project_name": "test_gdrive",
    "dry_run": null,
    "allow_local_artifacts": false
  }
  ```
- Output:
  ```json
  {
    "local_output_path": "projects/test_gdrive/normalized/Backlog__sheet-id__normalized.csv",
    "export_status": "success",
    "source_file_id": "sheet-id",
    "source_file_name": "Backlog"
  }
  ```
- Allowed scope: Google Sheets inside `GOOGLE_DRIVE_INPUT_FOLDER_ID`.
- Requires approval: no for local normalized export.
- Dry-run behavior: uses `config.dry_run` when `dry_run` is null. If dry-run is
  active and `allow_local_artifacts=false`, returns planned path/action only.
  If `allow_local_artifacts=true`, writes a unique local normalized file and
  never overwrites existing files.
- Risk level: medium.
- Failure cases: file outside input folder, unsupported format, export API
  failure, local write conflict.

## `gdrive.download_file`

- Type: read from Drive, write local normalized file.
- Purpose: Download regular files such as PDF, DOCX, XLSX, TXT, or Markdown
  from the input folder. PDF is downloaded only; OCR/text extraction is not
  included.
- Input:
  ```json
  {
    "file_id": "file-id",
    "project_name": "test_gdrive",
    "dry_run": null,
    "allow_local_artifacts": false
  }
  ```
- Output:
  ```json
  {
    "local_output_path": "projects/test_gdrive/normalized/Report__file-id__normalized.pdf",
    "download_status": "success",
    "source_file_id": "file-id",
    "source_file_name": "Report.pdf"
  }
  ```
- Allowed scope: files inside `GOOGLE_DRIVE_INPUT_FOLDER_ID`.
- Requires approval: no for local normalized download.
- Dry-run behavior: uses `config.dry_run` when `dry_run` is null. If dry-run is
  active and `allow_local_artifacts=false`, returns planned path/action only.
  If `allow_local_artifacts=true`, writes a unique local normalized file and
  never overwrites existing files.
- Manifest behavior: writes a record to the canonical manifest at
  `projects/{project_name}/logs/google_drive_manifest.json` in legacy mode, or
  `projects/google_drive/{project_id}/manifests/google_drive_manifest.json` in
  source-first mode, with
  `action=download_file`, `normalized_type=binary_download`, and for PDF
  `extraction_status=not_supported`.
- Risk level: medium.
- Failure cases: file outside input folder, unsupported binary size,
  permission denied, local write conflict.

## `gdrive.sync_folder_to_project`

- Type: read from Drive, write local normalized files.
- Purpose: Sync allowed input folder files into a local project.
- Input:
  ```json
  {
    "project_name": "test_gdrive",
    "max_files": 5,
    "include_mime_types": ["application/vnd.google-apps.document"],
    "dry_run": null,
    "allow_local_artifacts": false
  }
  ```
- Output:
  ```json
  {
    "synced_files": [],
    "skipped_files": [],
    "failed_files": [],
    "log_path": "projects/test_gdrive/logs/google_drive_mcp_audit.log"
  }
  ```
- Allowed scope: input folder only.
- Requires approval: no for local normalized sync; use dry-run first for large
  syncs.
- Dry-run behavior: uses `config.dry_run` when `dry_run` is null. Local
  normalized files are created only when `allow_local_artifacts=true`.
- Unsupported MIME types must not fail the whole flow. They should be recorded
  in the canonical manifest with `action=skip`, `status=skipped_unsupported`,
  and a reason.
- Risk level: high.
- Failure cases: partial export, mixed unsupported types, quota failure, local
  write conflict.

## `gdrive.write_markdown_output`

- Type: local write and optional Drive upload.
- Purpose: Write Markdown output to local output/review folder first, and only
  optionally upload reviewed output to Drive.
- Input:
  ```json
  {
    "project_name": "test_gdrive",
    "file_name": "ba-summary.md",
    "markdown_content": "# BA Summary\n",
    "target": "drive_review",
    "approval_status": "approved",
    "dry_run": null,
    "allow_local_artifacts": false
  }
  ```
- Output:
  ```json
  {
    "local_path": "projects/test_gdrive/review/ba-summary.md",
    "drive_file_id": "",
    "status": "dry_run",
    "dry_run_result": {
      "allowed": false,
      "dry_run": true,
      "reason": "dry-run mode is active",
      "required_approval": "Set MCP_DRY_RUN=false and provide approval for real write."
    },
    "log_path": "projects/test_gdrive/logs/google_drive_mcp_audit.log"
  }
  ```
- Allowed targets: `local_review`, `local_output`, `drive_review`,
  `drive_output`.
- Requires approval: yes for `drive_review` and `drive_output`.
- Requires `MCP_DRY_RUN=false` for real write/upload.
- Dry-run behavior: Drive upload is blocked. A local artifact is written only
  when `allow_local_artifacts=true`, and it uses a unique path.
- Risk level: high.
- Failure cases: missing approval, dry-run active, target not allowed, missing
  target folder ID, OAuth failure.

## `gdrive.create_review_package`

- Type: local write.
- Purpose: Create review package manifest for generated outputs.
- Input:
  ```json
  {
    "project_name": "test_gdrive",
    "agent_name": "ba_agent",
    "source_file_ids": ["doc-id"],
    "output_paths": ["projects/test_gdrive/outputs/ba-summary.md"],
    "dry_run": null,
    "allow_local_artifacts": false
  }
  ```
- Output:
  ```json
  {
    "review_package_path": "projects/test_gdrive/review",
    "manifest_path": "projects/test_gdrive/review/ba_agent_review_package.json",
    "status": "success"
  }
  ```
- Allowed scope: local project review folder.
- Requires approval: no for local package creation.
- Dry-run behavior: uses `config.dry_run` when `dry_run` is null. If dry-run is
  active and `allow_local_artifacts=false`, returns planned review/manifest
  paths only. If `allow_local_artifacts=true`, writes a unique local manifest.
- Risk level: medium.
- Failure cases: output path missing, local permission denied, manifest conflict.

## Canonical Manifest Contract

The bridge writes one canonical Google Drive manifest:

```text
projects/{project_name}/logs/google_drive_manifest.json
```

Source-first path:

```text
projects/google_drive/{project_id}/manifests/google_drive_manifest.json
```

Structure:

```json
{
  "version": "1.0",
  "project_name": "test_gdrive",
  "updated_at": "2026-05-26T00:00:00Z",
  "records": [
    {
      "source_file_id": "file-id",
      "source_file_name": "Source",
      "mime_type": "application/vnd.google-apps.document",
      "action": "export_google_doc",
      "local_path": "projects/test_gdrive/normalized/source.md",
      "status": "success",
      "timestamp": "2026-05-26T00:00:00Z",
      "normalized_type": "md",
      "error": null
    }
  ]
}
```

The canonical manifest is the only file allowed to update the same path. It is
updated via atomic temp-file replace and deduplicates identical
`source_file_id + action + local_path` records. Normalized artifacts still use
unique paths and are never overwritten.
