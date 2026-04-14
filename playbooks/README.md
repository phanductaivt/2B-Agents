# Playbooks

Playbooks are end-to-end operational guides.

## What A Playbook Includes

- step order
- decision logic
- rules
- validation points
- output rules

## Playbook vs Prompt

- A prompt explains how one task should be performed.
- A playbook explains how one type of request should be handled from start to finish.
- A project stores the real files, config, and knowledge that the playbook works on.

Current active model:
- BA Agent handles analysis and feature structuring
- UXUI Agent handles wireframe output
- FE Agent handles HTML output
- Reviewer Agent checks the final consistency

## Playbook vs Project

- Playbook = reusable process
- Project = reusable container of real work items

Example:
- `product-development` is one reusable playbook
- `projects/ticket-booking-improvement/` is one real project that can use that playbook

Every playbook now works with:
- the selected project's input files
- the selected project's `project-config.yaml`
- the selected project's knowledge files
- the selected project's output folder
- the selected project's tracking files (status, decisions, tasks)

Execution styles:
- full run: generate the whole package in one pass
- controlled run: generate one artifact at a time with dependency gates

Artifact definitions:
- see `artifacts/artifact-catalog.yaml`

## Current Playbooks

- `requirement-intake/`
- `prd-generation/`
- `backlog-refinement/`
- `product-development/`

<!-- TODO: Add a future playbook for meeting note analysis. -->
