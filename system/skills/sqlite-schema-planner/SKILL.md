---
name: sqlite-schema-planner
description: Convert a data model into a practical SQLite schema plan for a local runnable app. Use when v1 implementation stores data locally.
---
# SQLite Schema Planner

## Use When

- the project uses SQLite for local runnable delivery
- schema, seed data, and status transitions need to be clear before coding

## Output

A Markdown schema plan covering:
- tables
- columns
- primary keys and foreign keys
- important indexes
- seed data
- migration or reset notes

## Rules

- keep SQLite schema simple and inspectable
- prefer explicit status fields when workflows have state transitions
- document constraints that implementation tests should verify
