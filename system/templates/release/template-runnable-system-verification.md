---
file_type: "Template"
primary_agents: ["Release"]
supporting_agents: ["QA", "BE", "FE"]
activation_mode: "On-Demand Reference"
lifecycle_stage: "System Core"
purpose: "Provide the standard structure for recording runnable-system verification."
---
# Template - Runnable System Verification

## 1. Scope

- Project:
- Requirement:
- Verification date:
- Verifier:
- Verification target:
- Environment:
- Runnable status: Runnable / Partially Runnable / Not Runnable / Blocked / Not Verified

## 2. Evidence Rules

- Do not mark the system `Runnable` unless required backend, frontend, database, and smoke checks have actual command evidence.
- Every pass/fail claim must link to a command log row or detailed command block.
- If a command was not run, mark it `Not Run`, `Blocked`, or `Not Verified`; do not infer success from existing code or runbooks.
- Keep failed commands visible. Do not remove or rewrite failed output to make the report cleaner.
- Distinguish local runnable status from release readiness.

## 3. Required Command Log

| ID | Area | Working Directory | Command | Expected Result | Actual Result | Exit Code | Status | Timestamp | Notes |
|---|---|---|---|---|---|---:|---|---|---|
| CMD-001 | Backend install |  |  |  |  |  | Not Run |  |  |
| CMD-002 | Backend test |  |  |  |  |  | Not Run |  |  |
| CMD-003 | Backend start |  |  |  |  |  | Not Run |  |  |
| CMD-004 | Backend health/API check |  |  |  |  |  | Not Run |  |  |
| CMD-005 | Frontend install |  |  |  |  |  | Not Run |  |  |
| CMD-006 | Frontend build |  |  |  |  |  | Not Run |  |  |
| CMD-007 | Frontend start/preview |  |  |  |  |  | Not Run |  |  |
| CMD-008 | Frontend page check |  |  |  |  |  | Not Run |  |  |
| CMD-009 | Database setup/reset |  |  |  |  |  | Not Run |  |  |
| CMD-010 | Smoke flow |  |  |  |  |  | Not Run |  |  |

Status values:

- Pass
- Fail
- Blocked
- Not Run
- Skipped

## 4. Detailed Command Evidence

Use one block per executed, failed, blocked, skipped, or not-run command when the table row needs more context.

````md
### CMD-001: [Area] - [Purpose]

- Working directory:
- Command:
- Timestamp:
- Environment:
- Expected result:
- Actual result:
- Exit code:
- Status: Pass / Fail / Blocked / Not Run / Skipped

#### Relevant Output

```text
[paste relevant output]
```

#### Interpretation

#### Follow-up
````

## 5. Backend Verification

- install command:
- test command:
- start command:
- health command:
- test result:
- health result:
- linked command evidence:
- backend runnable status:

## 6. Frontend Verification

- install command:
- build command:
- start command:
- page command:
- build result:
- page result:
- dependency/security note:
- linked command evidence:
- frontend runnable status:

## 7. Database Verification

- setup/reset command:
- result:
- linked command evidence:
- database runnable status:

## 8. Smoke Verification

- command or steps:
- result:
- linked command evidence:
- smoke status:

## 9. Failure / Blocker Log

| ID | Type | Severity | Command/Check | Actual Result | Impact | Owner | Required Fix |
|---|---|---|---|---|---|---|---|

## 10. Known Gaps

- gap:

## 11. Runnable Verdict

- verdict:
- reason:
- evidence used:
- commands not run:
- blockers:
- local runnable limitations:
- not production-ready because:

## 12. Release Readiness Separation

- Release readiness status: Ready / Ready with caution / Not ready / Blocked / Not assessed
- Release readiness reason:
- QA evidence used:
- security/privacy/NFR evidence used:
- release blockers:
- approval/sign-off status:

## 13. Failure Routing

- backend/API/database failures:
- frontend build/API-consumption failures:
- unclear product behavior:
- verification rerun condition:
