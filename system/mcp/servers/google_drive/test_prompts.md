# Test Prompts: Google Drive MCP / Bridge

## Test Connection

You are testing Google Drive Bridge connectivity.

Steps:
1. Run `gdrive.health_check` in dry-run mode.
2. Confirm required environment variables are present without printing values.
3. Confirm OAuth status without printing tokens.
4. Confirm input, output, and review folders are reachable.

Output:
- Status:
- Missing variables:
- Folder checks:
- Errors:

## Test List File

Search only inside `GOOGLE_DRIVE_INPUT_FOLDER_ID` for up to 10 files. Return
file ID, name, MIME type, and modified time. Do not read file content.

## Test Read Metadata

For a user-provided file ID, call `gdrive.get_file_metadata`. Confirm the file
belongs to an allowed folder. Stop if the parent folder is outside scope.

## Test Export Google Docs

Export one user-approved Google Doc from the input folder to Markdown in
`PROJECT_INPUT_DIR` using dry-run first. Then run the real export only after the
dry-run plan is accepted.

## Test Export Google Sheets

Export one user-approved Google Sheet from the input folder to CSV or JSON in
`PROJECT_INPUT_DIR` using dry-run first. Report sheet/tab names and row count
only when available.

## Test Sync Local

Run `gdrive.sync_folder_to_project` in dry-run mode for the configured input
folder. Report the planned manifest and local destination paths.

## Test Write Output

Write a small Markdown output to the local project review folder with
`gdrive.write_markdown_output` in dry-run mode. Do not sync to Google Drive.

## Test Permission Boundary

Try to read metadata for a file ID known to be outside the configured folders.
Expected result: blocked, denied, or stopped due to scope validation.

## Test Fail Case

Call `gdrive.export_google_doc` with an invalid file ID. Report the exact
non-sensitive error and confirm no local output was created.

## Test Final Health Check

Run:
1. `gdrive.health_check`
2. Folder-scoped search.
3. Metadata read for one allowed file.
4. Dry-run export.
5. Dry-run review package creation.

Final output:
- Health status: `Healthy | Degraded | Unavailable | Blocked`
- Evidence:
- Blockers:
- Next action:
