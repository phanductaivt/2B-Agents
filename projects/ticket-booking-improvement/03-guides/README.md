# Working Guide

## What This Project Is For

Improve booking change and refund experience.

## Daily Working Surface

1. Put files in `01-input/requirements/` (or `01-input/notes/meeting-notes/`).
2. Run pipeline from root:
   - `python3 app.py --project ticket-booking-improvement`
3. Open curated results:
   - `02-output/ba/`
   - `02-output/design/`
   - `02-output/fe/`

## When You Need Deep Debug/Trace

Open `_ops/`:
- `_ops/status.md`
- `_ops/generated/<requirement-name>/`
- `_ops/traceability/`
- `_ops/runtime/`

<!-- TODO: Add one screenshot-style example for first-time BA users. -->
