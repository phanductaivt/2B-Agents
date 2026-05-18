---
file_type: "Sample Frontend Guide"
primary_agents: ["FE", "Release"]
supporting_agents: ["BE", "QA"]
activation_mode: "Reference Sample"
lifecycle_stage: "Project Sample Output"
purpose: "Show how the sample Vite React frontend can be run locally."
---
# Ticket Change Frontend

## Before You Start

Start the backend first:

```bash
cd ../backend
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

## Run The Frontend

Open a second terminal:

```bash
cd projects/project-template/02-output/app/frontend
npm install
npm run dev
```

Open:

```text
http://localhost:5173
```

Do not open `index.html` directly from the file browser. This app must be served by Vite so React and API calls work correctly.

## API Base URL

By default, the frontend calls:

```text
http://127.0.0.1:8000
```

To override it:

```bash
VITE_API_BASE=http://localhost:8000 npm run dev
```

## Build Check

```bash
npm run build
```
