---
file_type: "Sample Release Artifact"
primary_agents: ["Release"]
supporting_agents: ["QA", "BE", "FE"]
activation_mode: "Reference Sample"
lifecycle_stage: "Project Sample Output"
purpose: "Show how runnable-system verification should be recorded."
---
# req-001 Runnable System Verification

## Scope

- project: `project-template`
- verification target: local FastAPI + SQLite backend and Vite React TypeScript frontend
- backend path: `02-output/app/backend/`
- frontend path: `02-output/app/frontend/`
- smoke plan: `02-output/qa/req-001-smoke-test-plan.md`

## Backend Verification

- setup command: `python3 -m venv .venv && .venv/bin/pip install -r requirements.txt`
- test command: `.venv/bin/pytest`
- start command: `.venv/bin/uvicorn app.main:app --reload --port 8000`
- health command: `curl -s http://127.0.0.1:8000/health`
- expected result: backend tests pass
- recorded result: `3 passed in 0.21s`
- health result: `{"status":"ok"}`

## Frontend Verification

- setup command: `npm install`
- build command: `npm run build`
- start command: `npm run dev`
- page command: `curl -s -I http://localhost:5173/`
- expected result: frontend builds successfully
- recorded result: Vite build completed successfully with 26 transformed modules
- page result: `HTTP/1.1 200 OK`
- note: `npm install` reports dev dependency vulnerabilities; this does not block local demo readiness, but should be resolved before production use

## Database Verification

- setup: backend startup creates and seeds SQLite database
- expected result: backend tests can quote and confirm seeded sample tickets
- recorded result: covered by passing backend pytest suite

## Smoke Verification

- steps: see `02-output/qa/req-001-smoke-test-plan.md`
- recorded result: browser localhost flow completed by user after backend and frontend were started

## Runnable Verdict

- verdict: local-runnable-demo-ready
- reason: backend API, backend tests, frontend build, frontend dev server, and browser localhost flow have all been verified for the sample
- not production-ready because: real authentication, ticket ownership checks, real payment processing, production persistence, and real confirmation delivery are not implemented
