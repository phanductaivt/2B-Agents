---
name: architecture-designer
description: Create a concise architecture note for a local runnable software slice. Use when PO and BA outputs are ready and BE/FE/Data need a stable technical shape. Do not use for detailed implementation code.
---
# Architecture Designer

## Use When

- the feature needs a runnable system shape before BE and FE implementation
- agent outputs need a shared view of modules, boundaries, data flow, and integration points

## Inputs

- PO BRD
- BA FRS, acceptance criteria, feature list
- project context
- existing BE, FE, QA outputs when available

## Output

A Markdown architecture note covering:
- feature scope
- runtime stack
- module boundaries
- data flow
- API and UI touchpoints
- risks and constraints
- implementation implications

## Rules

- default to FastAPI + SQLite + Vite React for v1 runnable projects
- keep architecture proportional to the slice
- separate confirmed constraints from recommendations
- flag security, data, and NFR concerns instead of burying them
