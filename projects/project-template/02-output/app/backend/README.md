---
file_type: "Sample Backend Guide"
primary_agents: ["BE", "Release"]
supporting_agents: ["QA"]
activation_mode: "Reference Sample"
lifecycle_stage: "Project Sample Output"
purpose: "Show how the sample FastAPI backend can be run and tested."
---
# Ticket Change Backend

## Setup

```bash
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
```

## Run

```bash
uvicorn app.main:app --reload --port 8000
```

## Test

```bash
pytest
```

The SQLite database is seeded automatically on first request.
