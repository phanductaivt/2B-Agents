---
name: runnable-system-verifier
description: Verify whether a generated project can be called runnable. Use after app code and tests exist.
---
# Runnable System Verifier

## Use When

- backend, frontend, and tests have been generated
- the Release agent needs actual command results before declaring runnable status

## Output

A verification report covering:
- backend install/start/test command results
- frontend install/build command results
- database setup result
- smoke test result
- known gaps

## Rules

- do not call a project runnable without command evidence
- include failures plainly
- distinguish local runnable from deploy ready
