# ID System

## ID Formats
- `REQ-001`
- `BRD-001`
- `FR-001`
- `US-001`
- `AC-001`
- `FEAT-001`
- `UI-001`
- `RV-001`
- `TC-001`

## Storage
- Per project: `_ops/runtime/id-registry.yaml`
- Requirement file header: `# Requirement ID: REQ-001`

## Propagation
- REQ ID assigned to input.
- BRD/FR/US/AC/FEAT/UI/RV IDs derived and written to outputs.
- TC IDs allocated uniquely per project.

## Rules
- IDs are unique within a project.
- Use zero-padded numbers.
- Reuse existing IDs if already registered.
