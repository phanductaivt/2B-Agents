---
file_type: "Runbook"
primary_agents: ["PO", "BA", "Architect", "Data", "BE", "UIUX", "FE", "QA", "Release"]
supporting_agents: []
activation_mode: "Triggered By Workflow"
lifecycle_stage: "System Core"
purpose: "Control change requests for an existing stable project from intake through impact analysis, approval, baseline, apply, verification, merge, or rollback."
reads: ["01-input/requirements/", "01-input/change-requests/", "03-context/", "02-output/", "02-output/app/", "05-baselines/", "system/rules/", "system/guardrails/", "system/templates/change-control/"]
produces: ["01-input/change-requests/<cr>.md", "02-output/change-analysis/", "05-baselines/before-<cr>/", "updated approved artifacts or app files"]
---
# Handle Change Request

Use this runbook when a stable project receives a customer change request or customization request.

Do not use this runbook for first-time project generation. Use `generate-product-slice.md` and `projects/PROJECT_EXECUTION_GUIDE.md` for new project flow.

## Required Control Rules

- Every change request must have a stable `CR ID`.
- A CR intake file must exist before impact analysis.
- Impact analysis must happen before approval.
- No output artifact, app code, or linked requirement may be changed while CR status is `Draft`, `Analyzed`, `Pending Approval`, or `Rejected`.
- Approval must be explicit before regeneration or implementation.
- If Git is not the rollback layer, a baseline snapshot must exist before applying an approved CR.
- Apply only files listed in the regeneration plan.
- Merge into the linked requirement only after verification.
- Rollback must restore only files listed in the baseline manifest and rollback plan.

## Status Model

Allowed statuses:
- `Draft`
- `Analyzed`
- `Pending Approval`
- `Rejected`
- `Approved`
- `Baseline Created`
- `Applied`
- `Verified`
- `Merged`
- `Rolled Back`

## Phase 1: Intake

Create or update:
- `01-input/change-requests/<cr-id>.md`

Use:
- `system/templates/change-control/template-change-request.md`

Record:
- CR ID
- linked requirement
- requester
- requested change
- business reason
- current behavior affected
- expected behavior
- priority
- known constraints
- status

## Phase 2: Impact Analysis

Read:
- linked requirement in `01-input/requirements/`
- CR intake in `01-input/change-requests/`
- reusable context in `03-context/`
- current generated artifacts in `02-output/`
- current runnable app files in `02-output/app/` when implementation exists

Create:
- `02-output/change-analysis/<cr-id>-impact-analysis.md`

Use:
- `system/templates/change-control/template-impact-analysis.md`

Analyze:
- scope fit
- business value and urgency
- rule conflict or overlap
- affected user flows
- affected artifacts by owner
- data, state, schema, API, UI, backend, frontend, QA, metric, and release impact
- migration or compatibility concerns
- regression risk
- recommended decision

Stop after impact analysis unless the user explicitly approves.

## Phase 3: Approval Decision

If rejected before apply:
- update CR status to `Rejected`
- record reason in the CR file
- update `02-output/change-analysis/change-log.md`
- do not modify linked requirement, generated outputs, or app code

If revised:
- update CR intake
- rerun impact analysis only
- return to `Pending Approval`

If approved:
- update CR status to `Approved`
- create regeneration and rollback plans

## Phase 4: Regeneration And Rollback Plans

Create:
- `02-output/change-analysis/<cr-id>-regeneration-plan.md`
- `02-output/change-analysis/<cr-id>-rollback-plan.md`

Use:
- `system/templates/change-control/template-regeneration-plan.md`
- `system/templates/change-control/template-rollback-plan.md`

The regeneration plan must list:
- existing files to update
- new files to create
- owning agent
- reason each file is affected
- required skill/runbook route
- verification required

The rollback plan must list:
- files to restore from baseline
- CR-only files to remove
- audit files to keep
- verification after rollback

## Phase 5: Baseline Snapshot

If not using Git, create:
- `05-baselines/before-<cr-id>/baseline-manifest.md`
- `05-baselines/before-<cr-id>/files/`

Snapshot only existing files listed as update targets in the regeneration plan.

The baseline manifest must map:
- original path
- snapshot path
- reason for snapshot
- checksum or timestamp when available

Set CR status to `Baseline Created` before applying changes.

## Phase 6: Apply Approved Change

Apply the approved CR by following the regeneration plan.

Use the relevant artifact runbook and skill bindings:
- PO/BA: `generate-brd.md`, `generate-ba-package.md`, or targeted BA skills
- Architect: `generate-architecture.md`
- Data: `generate-data-design.md`
- BE: `generate-be-package.md`, `implement-be.md`
- UIUX/FE: `generate-wireframe.md`, `generate-fe-ui.md`, `implement-fe.md`
- QA: `generate-qa-review.md`
- Release: `integrate-runnable-app.md`, `verify-runnable-system.md`

Rules:
- keep existing filenames stable unless the plan explicitly creates a new file
- add CR trace notes where helpful
- stop if a newly discovered impact is outside the approved plan

Set CR status to `Applied`.

## Phase 7: Verification

Create:
- `02-output/change-analysis/<cr-id>-verification.md`

Use:
- `system/templates/change-control/template-change-verification.md`

Verify:
- changed artifacts remain consistent
- tests or smoke checks cover old and new behavior
- backend tests run or failure is documented
- frontend build runs or failure is documented
- release/run instructions remain accurate when runnable behavior changed

Set CR status to `Verified` only when evidence is recorded.

## Phase 8: Merge Into Linked Requirement

After verification, merge the approved CR summary into the linked requirement under:

```md
## Approved Change Requests
```

Keep the CR file as audit trail.

Update:
- linked requirement
- CR status to `Merged`
- `02-output/change-analysis/change-log.md`

## Phase 9: Rollback

Use rollback only after an applied CR is cancelled, rejected, or found unsafe.

Read:
- `05-baselines/before-<cr-id>/baseline-manifest.md`
- `02-output/change-analysis/<cr-id>-rollback-plan.md`

Rollback rules:
- restore only files listed in the baseline manifest
- remove only CR-created files listed in the rollback plan
- keep CR intake, impact analysis, rollback plan, and change log
- do not guess rollback scope

Set CR status to `Rolled Back` and record rollback evidence.
