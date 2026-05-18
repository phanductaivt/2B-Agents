---
name: release-runbook-writer
description: Write local run instructions and release discussion notes for a generated runnable app. Use after verification results are available.
---
# Release Runbook Writer

## Use When

- the app needs clear run instructions
- QA and verification outputs need a release-facing summary

## Output

A Markdown runbook covering:
- prerequisites
- backend setup/run/test commands
- frontend setup/run/build commands
- database setup/reset command
- smoke verification steps
- known gaps and readiness status

## Rules

- prefer exact commands over prose
- do not hide failed verification
- keep deployment claims out of local runnable v1 unless explicitly proven
