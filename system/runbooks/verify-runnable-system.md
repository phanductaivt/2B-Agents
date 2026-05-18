---
file_type: "Runbook"
primary_agents: ["Release"]
supporting_agents: ["QA", "BE", "FE"]
activation_mode: "Triggered By Workflow"
lifecycle_stage: "System Core"
purpose: "Verify whether a generated project can be called locally runnable."
reads: ["02-output/app/backend/", "02-output/app/frontend/", "02-output/qa/", "02-output/release/"]
produces: ["02-output/release/<req>-runnable-system-verification.md"]
---
# Verify Runnable System

Use this runbook after integration instructions are ready.

## Required Skills

- `runnable-system-verifier`

## Steps

1. Read run instructions and project README.
2. Run or document the backend install, setup, and test commands.
3. Start the backend or document why it cannot be started.
4. Verify backend health with a concrete URL or command.
5. Run or document the frontend install and build commands.
6. Start the frontend or document why it cannot be started.
7. Verify the frontend page responds with a concrete URL or command.
8. Run or document the database setup/reset command.
9. Run or document smoke verification steps.
10. Invoke `runnable-system-verifier` and write verification results to `02-output/release/`.

## Runnable Claim Rule

Do not call a project runnable unless the verification output records:
- backend start or test command
- frontend start or build command
- database setup command
- at least one smoke or test command
- actual command results or explicit reason a command could not be run
- a clear local-runnable vs production-ready distinction

## Recovery

If verification fails, record the exact command, error output, suspected owner, and next action. Route backend/API/database failures to BE or Data, frontend build/API-consumption failures to FE, unclear expected behavior to PO or BA, and release documentation gaps to Release.
