# File Tools

This folder contains simple local-first utilities for reading project input files and writing project output files.

## Files

- `reader.py`: reads file content from `projects/<project-name>/inputs/`
- `writer.py`: creates output folders and writes Markdown or HTML files into `projects/<project-name>/outputs/generated/`

## Why This Matters

These utilities keep the system easy to run locally in VS Code without external systems.

Simple rule:
- choose one project
- read from that project's inputs
- write to that project's outputs

<!-- TODO: Add a small helper for listing available input files. -->
