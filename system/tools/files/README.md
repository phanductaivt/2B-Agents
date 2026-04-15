# File Tools

This folder contains simple local-first utilities for reading project input files and writing project output files.

## Files

- `reader.py`: reads file content from `projects/<project-name>/01-input/`
- `writer.py`: creates output folders and writes Markdown or HTML files into `projects/<project-name>/_ops/generated/`

## Why This Matters

These utilities keep the system easy to run locally in VS Code without external systems.

Simple rule:
- choose one project
- read from `01-input`
- write internal generated files to `_ops/generated`
- let app-level curation copy main files to `02-output`

<!-- TODO: Add a small helper for listing available input files. -->
