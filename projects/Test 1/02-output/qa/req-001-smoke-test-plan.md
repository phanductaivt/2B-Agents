---
file_type: "QA Artifact"
primary_agents: ["QA"]
supporting_agents: ["BE", "FE", "Release"]
activation_mode: "Generated Output"
lifecycle_stage: "Project Output"
purpose: "Smoke test plan for the local runnable inventory app."
---
# req-001 Smoke Test Plan

## Backend Smoke

```bash
cd "projects/Test 1/02-output/app/backend"
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
pytest
uvicorn app.main:app --reload --port 8000
```

## Frontend Smoke

```bash
cd "projects/Test 1/02-output/app/frontend"
npm install
npm run build
npm run dev
```

## Browser Flow

1. Open `http://localhost:5173`.
2. Confirm seeded products display with ACTIVE, LOW_STOCK, and OUT_OF_STOCK badges.
3. Search `keychron`.
4. Create a product with a new product code.
5. Edit the product name or minimum stock.
6. Update quantity to 0 and verify OUT_OF_STOCK.
7. Delete product and confirm it no longer appears.
