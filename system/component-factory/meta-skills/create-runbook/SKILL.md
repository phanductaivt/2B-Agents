---
name: create-runbook
description: Use when a new runtime Runbook is needed for a repeatable operating workflow and no existing runbook can be safely extended; do not use for ad hoc one-off execution notes.
---
# Create Runbook

## Purpose

Create a new runtime runbook through Component Factory.

## Steps

1. Check `system/runbooks/` for an existing workflow that already fits.
2. Read factory rules for scope, naming, dependency, and update control.
3. Use `runbooks/create-runbook-runbook.md`.
4. Use `templates/runbook-template.md`.
5. Produce `artifacts/component-creation-report.md`.

## Prohibited Actions

- do not create a runbook that should really be a rule or skill
- do not create a runbook without clear purpose, steps, validation, and expected output
