---
file_type: "Runbook"
primary_agents: ["Architect"]
supporting_agents: ["PO", "BA", "BE", "FE", "QA"]
activation_mode: "Triggered By Workflow"
lifecycle_stage: "System Core"
purpose: "Generate architecture, NFR, and security outputs for a runnable feature slice."
reads: ["02-output/po/", "02-output/ba/", "03-context/", "system/rules/", "system/guardrails/", "system/skills/", "system/templates/"]
produces: ["02-output/architecture/<req>-architecture-note.md", "02-output/architecture/<req>-nfr-review.md", "02-output/architecture/<req>-security-review.md"]
---
# Generate Architecture

Use this runbook after PO BRD and BA package are ready.

## Required Skills

- `architecture-designer`
- `nfr-reviewer`
- `security-reviewer`

## Steps

1. Read PO BRD, BA FRS, acceptance criteria, and feature list.
2. Invoke `architecture-designer` and define the local runnable architecture.
3. Invoke `nfr-reviewer` and record quality attributes that affect implementation or testing.
4. Invoke `security-reviewer` when authorization, ownership, payment, privacy, or sensitive data matters.
5. Write outputs to `02-output/architecture/`.
6. Stop for clarification when an architecture, NFR, or security gap would materially change implementation.

## Validation

- architecture matches the same slice as BRD and FRS
- runtime stack is explicit
- security and NFR gaps are visible
- BE, FE, Data, QA, and Release can consume the outputs without guessing core constraints
