---
file_type: "Sample Release Artifact"
primary_agents: ["Release"]
supporting_agents: ["BE", "FE", "QA"]
activation_mode: "Reference Sample"
lifecycle_stage: "Project Sample Output"
purpose: "Show local run instructions for the runnable ticket-change sample."
---
# req-001 Run Instructions

## Scope

- project: `project-template`
- runnable app path: `projects/project-template/02-output/app/`
- backend URL: `http://127.0.0.1:8000`
- frontend URL: `http://localhost:5173`
- health check: `http://127.0.0.1:8000/health`

## Terminal 1 - Backend

```bash
cd "projects/project-template/02-output/app/backend"
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
pytest
uvicorn app.main:app --reload --port 8000
```

Expected backend startup:

```text
Uvicorn running on http://127.0.0.1:8000
```

## Terminal 2 - Frontend

```bash
cd "projects/project-template/02-output/app/frontend"
npm install
npm run build
npm run dev
```

Expected frontend startup:

```text
Local: http://localhost:5173/
```

## Database

- SQLite database is created and seeded automatically by the backend.
- Local database file is generated under backend app code at runtime.
- Delete the generated SQLite file only when you intentionally want a fresh local seed.

## Browser Smoke Flow

1. Open `http://localhost:5173/`.
2. Select ticket `TCK-1001`.
3. Choose a new date before departure, for example `2026-06-07`.
4. Click `View fee`.
5. Confirm fare difference, change fee, total due, and payment-required state are visible.
6. Click `Confirm and pay`.
7. Verify success message confirms the ticket changed and confirmation was sent.

## Troubleshooting

- If the page does not load, confirm `npm run dev` is still running and open `http://localhost:5173/`, not the local `index.html` file.
- If tickets do not load, confirm backend is running and open `http://127.0.0.1:8000/health`.
- If the browser reports CORS or API errors, restart both backend and frontend after dependency installation.
- If port `8000` or `5173` is busy, stop the old process or update the frontend API base before rerunning.
