---
file_type: "Backend Guide"
primary_agents: ["BE", "Release"]
supporting_agents: ["QA"]
activation_mode: "Generated Output"
lifecycle_stage: "Project Output"
purpose: "Run and test the inventory backend."
---
# Inventory Backend

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

SQLite database is created and seeded automatically.
