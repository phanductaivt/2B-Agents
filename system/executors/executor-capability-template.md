---
file_type: "Executor Capability Template"
primary_agents: []
supporting_agents: ["PO", "BA", "Architect", "Data", "BE", "UIUX", "FE", "QA", "Release"]
activation_mode: "On-Demand Reference"
lifecycle_stage: "System Core"
purpose: "Provide a standard capability and permission declaration for an AI Executor."
---
# AI Executor Capability Profile

## Executor Identity

- Executor name/client:
- Model or runtime, if known:
- Session/date:
- Capability profile status: `Verified | Partially Verified | Declared Only`

## Active Assignment

- Active task ID:
- Active project:
- Active workflow:
- Active runbook:
- Active Agent:

## Repository Capabilities

| Capability | Status | Scope / Evidence |
| --- | --- | --- |
| Read files | `Available | Unavailable | Unknown` | |
| Create files | `Available | Unavailable | Unknown` | |
| Modify files | `Available | Unavailable | Unknown` | |
| Delete or move files | `Approved | Restricted | Unavailable | Unknown` | |
| Execute local commands | `Available | Unavailable | Unknown` | |
| Access network | `Available | Restricted | Unavailable | Unknown` | |
| Use browser automation | `Available | Restricted | Unavailable | Unknown` | |

## Available MCP Tools

| MCP / Tool | Availability | Allowed Scope | Verification Evidence |
| --- | --- | --- | --- |
| Google Drive MCP / Bridge | `Available | Unavailable | Unknown` | | |
| Playwright MCP | `Available | Unavailable | Unknown` | | |
| Filesystem/Workspace MCP | `Available | Unavailable | Unknown` | Configured root; allowed read/write paths; denied secret/private paths | |
| Other | | | |

## Permission Profile

- Read scope:
- Write scope:
- Approval-required actions:
- Restricted or denied actions:
- Secret-handling constraints:
- Local Git/GitHub constraints and unrelated dirty-work boundary, when used
  outside MCP:
- Filesystem/Workspace allowed paths and delete/overwrite restrictions:

## Executor Limitations

- Context or file-access limitations:
- Tool limitations:
- Command/runtime limitations:
- Output-format limitations:
- Other limitations:

## Uncertainty

- Unverified capability:
- Impact if required:
- Safe next action:
