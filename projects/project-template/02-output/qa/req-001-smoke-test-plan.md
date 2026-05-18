---
file_type: "Sample QA Artifact"
primary_agents: ["QA"]
supporting_agents: ["BE", "FE", "Release"]
supporting_agents: ["BE", "FE"]
activation_mode: "Reference Sample"
lifecycle_stage: "Project Sample Output"
purpose: "Show the QA-owned smoke test plan for the sample runnable ticket-change app."
---
# req-001 Smoke Test Plan

## Backend

```bash
cd "projects/project-template/02-output/app/backend"
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
pytest
uvicorn app.main:app --port 8000
```

## Frontend

```bash
cd "projects/project-template/02-output/app/frontend"
npm install
npm run build
npm run dev
```

## Manual Flow

1. Open the frontend dev URL.
2. Select ticket `TCK-1001`.
3. Choose `2026-06-07`.
4. Click `View fee`.
5. Confirm the fare difference, change fee, and total due.
6. Click `Confirm and pay`.
7. Confirm success message says the ticket changed and confirmation was sent.
