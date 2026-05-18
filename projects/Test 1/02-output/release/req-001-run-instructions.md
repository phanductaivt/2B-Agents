---
file_type: "Release Artifact"
primary_agents: ["Release"]
supporting_agents: ["BE", "FE", "QA"]
activation_mode: "Generated Output"
lifecycle_stage: "Project Output"
purpose: "Local run instructions for req-001."
---
# req-001 Run Instructions

## Terminal 1 - Backend

```bash
cd "projects/Test 1/02-output/app/backend"
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
pytest
uvicorn app.main:app --reload --port 8000
```

Backend health:

```text
http://127.0.0.1:8000/health
```

## Terminal 2 - Frontend

```bash
cd "projects/Test 1/02-output/app/frontend"
npm install
npm run build
npm run dev
```

Frontend URL:

```text
http://localhost:5173
```

## Database

SQLite database is created and seeded automatically by the backend.
