---
file_type: "Change Request Rollback Plan Template"
primary_agents: ["Release", "QA", "BA"]
supporting_agents: ["PO", "Architect", "Data", "BE", "UIUX", "FE"]
activation_mode: "Template"
lifecycle_stage: "Project Change Control"
purpose: "Define how to restore a project if an applied change request is cancelled or rejected."
---
# Rollback Plan: <CR-ID>

Linked Requirement: `<requirement-file>`
Baseline: `05-baselines/before-<cr-id>/`

## Restore From Baseline

| Original Path | Baseline Snapshot Path | Reason |
| --- | --- | --- |
|  |  |  |

## Remove CR-Only Files

| File | Reason |
| --- | --- |
|  |  |

## Keep Audit Files

- `01-input/change-requests/<cr-id>.md`
- `02-output/change-analysis/<cr-id>-impact-analysis.md`
- `02-output/change-analysis/<cr-id>-regeneration-plan.md`
- `02-output/change-analysis/<cr-id>-rollback-plan.md`
- `02-output/change-analysis/change-log.md`

## Rollback Verification

- 

## Rollback Stop Conditions

- 
