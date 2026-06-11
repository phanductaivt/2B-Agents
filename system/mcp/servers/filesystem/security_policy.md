# Security Policy: Filesystem/Workspace MCP

## Risk And Mitigation

- Risk level: High because broad or write-enabled filesystem access can expose
  secrets, overwrite governance, delete files, or disturb unrelated work.
- Mitigation: Executor-bound availability, narrow configured root, exact path
  routing, secret/private-file denial, read-before-write, approval gates, and
  handoff evidence.

## Allowed By Default

- List and read exact task-relevant paths under the configured workspace root.
- Create files in exact approved project output/review paths.
- Review an exact user/task-scoped diff artifact or compare exact approved
  files.
- Report unrelated dirty files without touching them.

## Human Approval Required

- delete or move any file
- overwrite an existing source/input file
- write outside approved project paths
- expand the configured workspace root
- read a private or potentially secret-bearing file when the user has
  explicitly identified and approved it
- overwrite governance files outside a scoped governance task

## Prohibited By Default

- broad user-home or filesystem reads
- reading or exposing secrets, credentials, tokens, `.env`, private keys, or
  private files
- writing outside approved workspace/project paths
- deleting files without explicit approval
- touching unrelated dirty files
- overwriting governance files without a scoped governance task
- logging sensitive file content

## Required Executor Declaration

The active AI Executor must record Filesystem/Workspace MCP availability,
configured root, allowed read/write paths, denied paths/actions, and actual
verification evidence.

## Required Handoff Evidence

Record exact paths read or written, actual actions/results, permission profile,
approval state, unrelated dirty files preserved, risks, and next step.
