---
file_type: "Baseline Snapshot Area"
primary_agents: ["Release", "QA"]
supporting_agents: ["PO", "BA", "Architect", "Data", "BE", "UIUX", "FE"]
activation_mode: "Manual Navigation"
lifecycle_stage: "Project Change Control"
purpose: "Store pre-change snapshots for rollback when Git is not used as the rollback layer."
---
# Baselines

Use this folder only when applying an approved change request without Git rollback.

Expected structure:

```text
before-cr-001/
├── baseline-manifest.md
└── files/
```

Snapshot only files listed as update targets in the CR regeneration plan.

Do not apply an approved CR without either:
- a Git baseline or branch, or
- a snapshot under this folder.
