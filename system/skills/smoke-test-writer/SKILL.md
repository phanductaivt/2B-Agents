---
name: smoke-test-writer
description: Write minimal smoke checks for a local runnable app. Use when the app needs proof that backend, frontend, and core happy path can run.
---
# Smoke Test Writer

## Use When

- the generated app needs local runnable verification
- full automation is too heavy for the first slice

## Output

Smoke test instructions or scripts covering:
- backend health or root check
- representative API call
- frontend build or startup check
- one core user flow

## Rules

- keep smoke checks executable by a developer
- record exact commands
- separate smoke success from full QA readiness
