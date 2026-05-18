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

## 2. Backend Verification

- install command:
- test command:
- start command:
- health command:
- test result:
- health result:

## 3. Frontend Verification

- install command:
- build command:
- start command:
- page command:
- build result:
- page result:
- dependency/security note:

## 4. Database Verification

- setup/reset command:
- result:

## 5. Smoke Verification

- command or steps:
- result:

## 6. Known Gaps

- gap:

## 7. Runnable Verdict

- verdict:
- reason:
- not production-ready because:

## 8. Failure Routing

- backend/API/database failures:
- frontend build/API-consumption failures:
- unclear product behavior:
- verification rerun condition:
