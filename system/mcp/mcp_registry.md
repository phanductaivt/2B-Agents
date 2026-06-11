# MCP Registry

This registry is the source of truth for MCP servers and bridge integrations
allowed in the Agent Workspace.

| MCP name | Category | Status | Usage | Allowed Agents | Risk Level | Recommended Pattern | Notes |
|---|---|---|---|---|---|---|---|
| Filesystem/Workspace MCP | Local Resource | Approved | Scoped local workspace file read/write for exact task/project paths. | Active Agent only when its runbook explicitly requires the MCP; otherwise governance/setup tasks with Active Agent `None` | High | Verify current-Executor availability; declare `WORKSPACE_ROOT`; read exact paths; write only approved project paths. | Secret/private files, unrelated dirty files, delete, out-of-scope writes, and unscoped governance overwrites are denied by default. |
| Google Drive MCP / Google Drive Bridge | Cloud Workspace | Restricted / Prefer Local Bridge | Read configured Drive input folder, export Docs/Sheets, sync normalized files to local project inputs, create review packages, optionally sync reviewed output back. | Ingestion/Router first; PO, BA, Product, UX, QA, Release through routed local files; FE/Architect only when docs are needed | High | Local Google Drive Bridge -> Normalize -> Agent Workspace -> Review -> Optional Write-back | Must use `GOOGLE_DRIVE_INPUT_FOLDER_ID`, `GOOGLE_DRIVE_OUTPUT_FOLDER_ID`, and `GOOGLE_DRIVE_REVIEW_FOLDER_ID`. No full Drive crawling. |
| Playwright MCP | Browser Automation | Approved | Browser automation, local/dev UI smoke tests, screenshots, console inspection, accessibility-oriented checks. | UX, FE, QA, Release | Medium | Use on local/dev URLs or explicitly approved safe URLs. | Production-impacting flows require approval. |

Git MCP is de-scoped. Local Git CLI, IDE Git features, and GitHub remote usage
remain outside the MCP registry.

## Status Meanings

- `Approved`: may be used under the policy and server-specific contract.
- `Restricted`: may be used only within the listed boundaries.
- `Restricted / Prefer Local Bridge`: cloud system should be mediated through a
  local bridge or desktop sync before remote MCP is considered.
- `Pending`: not usable until setup and validation evidence exists.
- `Deferred`: intentionally paused.
- `Blocked`: must not be used.

## Agent Scope

Workspace agents include PO, BA, Product, UX/UI, Architect, Data, BE, FE,
QA/Test, and Release agents. A server profile may narrow this list.

## Availability Rule

Registry status defines governance eligibility, not current-session
availability. Every AI Executor must verify MCP availability and record its
allowed scope and permission profile before use.
