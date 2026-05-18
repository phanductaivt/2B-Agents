---
name: data-model-designer
description: Design entities, fields, ownership, relationships, and state for a runnable software slice. Use before BE implementation when persistence behavior matters.
---
# Data Model Designer

## Use When

- a feature needs stored records, state transitions, or seed data
- BE implementation would otherwise guess fields or ownership

## Output

A Markdown data model covering:
- entities
- important fields
- relationships
- ownership rules
- validation notes
- seed data needs

## Rules

- tie each entity to product or functional behavior
- avoid speculative fields
- make sensitive fields and audit needs explicit
