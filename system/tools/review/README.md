# Review Tools (Legacy Compatibility)

This folder contains local tools for confirmation and decision review.

Scope note:
- Confirmation storage/sync logic remains here (`confirmation_manager.py`).
- Write interaction is now owned by Operations Console (`system/tools/ops_console/`).
- `decision_server.py` is deprecated and now acts as a compatibility wrapper to ops_console.
- Confirmation model separates recommendation vs final truth:
  - `recommendation_label`: `Research Recommendation`
  - `data_state`: `recommended` or `confirmed-data`
  - `decision_authority`: `human-required`

## Files
- `confirmation_manager.py`: project-level confirmation source-of-truth manager (YAML + Markdown sync).
- `decision_server.py`: legacy compatibility wrapper (deprecated).

## Data Location (per project)
- `_ops/confirmations/pending-confirmations.yaml` (machine source of truth)
- `_ops/confirmations/pending-confirmations.md` (human-readable summary)
- `_ops/confirmations/decisions-log.md` (decision history)

## Run
```bash
python3 system/tools/review/decision_server.py
```

Then open (legacy port):
`http://127.0.0.1:8787`

Preferred path:
```bash
python3 app.py --ops-console
```

Note:
- `decision_server.py` should be treated as compatibility-only.
- It reuses `ops_console` backend/UI and should not be extended with separate behavior.
- Active confirmation and document workflows should be done in `ops_console`.
- Long-term primary interaction layer is `system/tools/ops_console/` + `workspace/ops-console/`.

<!-- TODO: Add a short troubleshooting section for port conflicts. -->
