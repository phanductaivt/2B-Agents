---
file_type: "Change Request Guide"
primary_agents: ["PO", "BA", "Architect", "Data", "BE", "UIUX", "FE", "QA", "Release"]
supporting_agents: []
activation_mode: "Manual Navigation"
lifecycle_stage: "Project Change Control"
purpose: "Copy-ready cookbook for receiving, analyzing, approving, applying, verifying, merging, and rolling back change requests on an existing stable project."
---
# Project Change Request Guide

Use this guide when a project already has stable requirements, generated outputs, or runnable app code, and a customer asks for a change or customization.

Use `PROJECT_EXECUTION_GUIDE.md` for new project creation and first-time product-slice generation. Use this guide for post-baseline change control.

Core rules:
- Do not edit the original requirement or generated outputs directly when a new change request arrives.
- Do not regenerate artifacts before impact analysis and explicit approval.
- Do not apply an approved change request unless a baseline snapshot exists.
- Every changed artifact, code file, test, or verification note must trace back to a `CR ID`.
- Merge approved changes into the linked requirement only after apply and verification.

## Quick Start

### Prompt to copy

Replace project, requirement, and change details:

```text
Create a change request intake and run impact analysis only. Do not apply or regenerate anything yet.

Project:
- projects/<project-name>/

Linked requirement:
- 01-input/requirements/<requirement-file>.md

Change request ID:
- CR-001

Customer/requester:
- <name or team>

Requested change/customization:
<paste the requested change here>

Operating mode:
- Follow system/runbooks/handle-change-request.md
- Follow system/rules/
- Follow system/guardrails/
- Use system/agents/ as role definitions
- Use system/skills/ and system/templates/
- Read existing project context from 03-context/
- Read existing outputs from 02-output/

Tasks:
- Create 01-input/change-requests/cr-001.md.
- Create 02-output/change-analysis/cr-001-impact-analysis.md.
- Set CR Status to Pending Approval.
- Stop before baseline, apply, regenerate, merge, or rollback.

Final response:
- List files created or updated.
- Tell me the exact impact analysis path.
- State recommended decision and CR Status.
- Tell me the exact approval/rejection phrases I can reply with.
```

### Expected result

- `01-input/change-requests/cr-001.md` exists.
- `02-output/change-analysis/cr-001-impact-analysis.md` exists.
- No official requirement, output artifact, or app code has been changed yet.
- CR status is `Pending Approval`.

## Step 1: Create Change Request Intake

### What to do

Capture the customer request as its own source artifact.

### Prompt to copy

```text
Create a change request intake only. Do not analyze, apply, regenerate, or merge yet.

Project:
- projects/<project-name>/

Change request ID:
- CR-001

Linked requirement:
- 01-input/requirements/<requirement-file>.md

Requester:
- <requester>

Requested change:
<paste request>

Write:
- 01-input/change-requests/cr-001.md

Use:
- system/templates/change-control/template-change-request.md
```

### Expected result

The CR file records:
- CR ID
- linked requirement
- requester
- requested change
- business reason
- expected behavior
- current behavior affected
- priority
- status

## Step 2: Analyze Impact

### What to do

Before any regeneration, analyze how the CR affects the current project.

### Prompt to copy

```text
Run impact analysis for this change request only. Do not apply or regenerate anything.

Project:
- projects/<project-name>/

Change request:
- 01-input/change-requests/cr-001.md

Linked requirement:
- 01-input/requirements/<requirement-file>.md

Read:
- 03-context/
- 02-output/
- 02-output/app/

Write:
- 02-output/change-analysis/cr-001-impact-analysis.md

Use:
- system/runbooks/handle-change-request.md
- system/templates/change-control/template-impact-analysis.md

Stop with CR Status set to Pending Approval.
```

### Expected result

Impact analysis explains:
- whether the CR is in scope
- business rule impact
- requirement conflict or overlap
- affected artifacts
- affected app code or tests
- data/schema/state impact
- API/FE/BE impact
- QA/regression impact
- release or runnable verification impact
- recommended decision

## Step 3: Approve, Reject, Or Revise

### Approve

Use this only after reviewing the impact analysis:

```text
Approved CR-001 - Proceed.

Create the regeneration plan, rollback plan, and baseline snapshot before applying any changes.
```

### Reject

Use this when the CR should not be applied:

```text
Rejected CR-001.

Record the rejection reason:
- <reason>

Do not apply, regenerate, merge, or modify official requirement/output/app files.
Update the CR status and change log only.
```

### Revise

Use this when the CR needs more clarification:

```text
Revise CR-001 with these details, then rerun impact analysis only:
- <detail 1>
- <detail 2>

Do not apply or regenerate anything.
```

## Step 4: Create Regeneration And Rollback Plans

### What to do

After approval, list exactly which files will change and how to restore them if the CR is cancelled later.

### Prompt to copy

```text
CR-001 is approved. Create the regeneration and rollback plans only. Do not apply changes yet.

Project:
- projects/<project-name>/

Change request:
- 01-input/change-requests/cr-001.md

Impact analysis:
- 02-output/change-analysis/cr-001-impact-analysis.md

Write:
- 02-output/change-analysis/cr-001-regeneration-plan.md
- 02-output/change-analysis/cr-001-rollback-plan.md

Plans must list:
- files to update
- files to create
- files to remove if rolled back
- owning agent for each change
- verification commands or checks
- merge target in the linked requirement
```

### Expected result

The regeneration plan identifies only the impacted files. It should not default to full project regeneration.

## Step 5: Create Baseline Snapshot

### What to do

If not using Git, copy the current version of every file that the CR will update.

### Prompt to copy

```text
Create baseline snapshot for CR-001. Do not apply changes yet.

Project:
- projects/<project-name>/

Regeneration plan:
- 02-output/change-analysis/cr-001-regeneration-plan.md

Rollback plan:
- 02-output/change-analysis/cr-001-rollback-plan.md

Create:
- 05-baselines/before-cr-001/baseline-manifest.md
- 05-baselines/before-cr-001/files/

Snapshot only files listed as update targets in the regeneration plan.
Record files that will be created by CR-001 in the rollback plan.
```

### Expected result

Baseline manifest exists and maps original file paths to snapshot paths.

## Step 6: Apply Approved Change

### What to do

Apply only the files listed in the regeneration plan.

### Prompt to copy

```text
Apply approved CR-001 using the regeneration plan.

Project:
- projects/<project-name>/

Use:
- 01-input/change-requests/cr-001.md
- 02-output/change-analysis/cr-001-impact-analysis.md
- 02-output/change-analysis/cr-001-regeneration-plan.md
- 02-output/change-analysis/cr-001-rollback-plan.md
- 05-baselines/before-cr-001/baseline-manifest.md

Rules:
- Change only files listed in the regeneration plan unless a newly discovered blocker requires stopping.
- Keep filenames stable for existing artifacts.
- Add CR trace notes to updated artifacts where useful.
- Do not merge CR into the linked requirement until verification is complete.
```

### Expected result

Impacted outputs, app code, or tests are updated and traceable to `CR-001`.

## Step 7: Verify Change

### What to do

Run or document checks that prove the changed behavior is coherent.

### Prompt to copy

```text
Verify applied CR-001.

Project:
- projects/<project-name>/

Read:
- 02-output/change-analysis/cr-001-regeneration-plan.md
- 02-output/change-analysis/cr-001-rollback-plan.md
- changed artifacts and app files
- 02-output/qa/
- 02-output/release/

Write:
- 02-output/change-analysis/cr-001-verification.md

Run or document:
- artifact consistency checks
- backend tests if backend changed
- frontend build if frontend changed
- smoke checks if runnable behavior changed
- regression coverage for old and new behavior

Do not merge into the linked requirement unless verification is pass or explicitly accepted with known risks.
```

## Step 8: Merge Approved CR Into Requirement

### What to do

After successful verification, update the linked requirement so it represents the current approved truth.

### Prompt to copy

```text
Merge verified CR-001 into the linked requirement.

Project:
- projects/<project-name>/

Linked requirement:
- 01-input/requirements/<requirement-file>.md

Read:
- 01-input/change-requests/cr-001.md
- 02-output/change-analysis/cr-001-impact-analysis.md
- 02-output/change-analysis/cr-001-verification.md

Update:
- linked requirement with an Approved Change Requests section
- 01-input/change-requests/cr-001.md status to Merged
- 02-output/change-analysis/change-log.md

Do not remove the CR file. It remains audit trail.
```

### Expected requirement section

```md
## Approved Change Requests

### CR-001: <short title>
Status: Merged
Approved Date:
Merged Date:

Change Summary:
- ...

Affected Areas:
- BA
- Data
- BE
- FE
- QA

Source:
- 01-input/change-requests/cr-001.md
```

## Step 9: Roll Back Applied CR

### What to do

Use rollback only when the CR was applied and later cancelled or rejected.

### Prompt to copy

```text
Roll back applied CR-001 using the baseline snapshot. Do not guess rollback scope.

Project:
- projects/<project-name>/

Read:
- 05-baselines/before-cr-001/baseline-manifest.md
- 02-output/change-analysis/cr-001-rollback-plan.md

Tasks:
- Restore every snapshotted file to its original path.
- Remove CR-only files listed in the rollback plan, unless they are audit files.
- Keep the CR intake, impact analysis, rollback plan, and change log.
- Set CR Status to Rolled Back.
- Update 02-output/change-analysis/change-log.md.
- Write rollback evidence to 02-output/change-analysis/cr-001-verification.md or a rollback note.
```

### Expected result

The stable project returns to the pre-CR file state for all planned affected files.

## Folder Reference

```text
projects/<project>/
├── 01-input/
│   ├── requirements/
│   └── change-requests/
├── 02-output/
│   └── change-analysis/
├── 03-context/
└── 05-baselines/
```

## Status Reference

Use these CR statuses:

```text
Draft
Analyzed
Pending Approval
Rejected
Approved
Baseline Created
Applied
Verified
Merged
Rolled Back
```
