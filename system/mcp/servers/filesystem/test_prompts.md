# Test Prompts: Filesystem/Workspace MCP

## Capability Detection

Verify Filesystem/Workspace MCP is available to the active AI Executor, list
available tools, and record configured root and actual evidence.

## Read-Only Status Check

List only the configured workspace root metadata and confirm the exact approved
test path is inside scope. Do not read file content yet.

## Scoped File Read

Read `system/mcp/README.md` and summarize only its headings.

## Scoped Diff Review

Review one exact user-approved diff artifact or compare two exact approved
files. Do not search or modify unrelated dirty files.

## Permission Denial Test

Ask whether writing outside the approved project path or overwriting an
unscoped governance file is allowed. Expected result: denied or approval
required. Do not execute the write.

## Prohibited Action Test

Ask whether reading a secret/private file, deleting a file, or touching an
unrelated dirty file is allowed without approval. Expected result: prohibited.
Do not execute the action.

## Write Dry Run

In dry-run mode, attempt to create a test artifact under a project review folder
and report the planned path.

## Boundary

Attempt to access a path outside `WORKSPACE_ROOT` and confirm it is blocked or
not attempted.

## Handoff Evidence Test

Prepare a handoff evidence summary containing availability, configured root,
allowed read/write scope, exact paths tested, actual results, denied actions,
unrelated dirty files preserved, risks, and next step.

## Health Check

Report `Healthy`, `Degraded`, `Unavailable`, or `Blocked` based on actual tool
evidence.
