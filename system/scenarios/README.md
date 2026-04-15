# Scenario Engine (Level 2)

This folder stores reusable scenario defaults used by the runner.

## Why this exists

- Keep scenario logic out of `app.py`
- Make new projects configuration-driven
- Let BA/PO users add scenario behavior by editing YAML, not Python

## Files

- `scenario-catalog.yaml`: maps scenario keys and domain aliases to scenario files
- `generic.yaml`: fallback scenario
- `ticketing.yaml`: booking/ticket change scenario defaults
- `loyalty.yaml`: loyalty/points scenario defaults
- `order-status.yaml`: order tracking scenario defaults

## Resolution order

1. If `project-config.yaml` has `scenario`, use it.
2. Else map `domain` using `scenario-catalog.yaml`.
3. Else fallback to `generic`.

## Notes

- Scenario files provide defaults, not rigid templates.
- Input text and project knowledge can still override/extend these defaults.
- Keep YAML practical and beginner-friendly.

<!-- TODO: Add short example for creating a custom scenario file. -->
