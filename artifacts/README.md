# Artifact Model

This folder defines how requirement processing is split into small, controllable artifacts.

## Why This Exists
- We can run one artifact at a time.
- We can check quality before downstream work.
- We can avoid cascading issues from weak upstream outputs.

## Main File
- `artifact-catalog.yaml`: source of truth for artifact definitions.

Each artifact definition includes:
- `name`
- `stage`
- `owner`
- `dependencies`
- `outputs`
- `validators`
- `gate_required`

## Typical Stages
- `clarification`
- `ba-core`
- `design`
- `fe-prototype`
- `review`

<!-- TODO: Add optional project-specific artifact override support when teams need custom flow. -->

