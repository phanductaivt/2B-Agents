---
name: nfr-reviewer
description: Review non-functional needs for a runnable feature slice. Use when performance, reliability, usability, observability, or maintainability could affect implementation or release readiness.
---
# NFR Reviewer

## Use When

- the slice is moving from specification into runnable implementation
- quality attributes may affect BE, FE, QA, or release decisions

## Output

A Markdown NFR review covering:
- performance expectations
- reliability and failure handling
- usability and accessibility concerns
- observability needs
- maintainability risks
- known gaps and assumptions

## Rules

- do not invent production SLOs without project context
- mark missing expectations clearly
- focus on what changes implementation, testing, or release readiness
