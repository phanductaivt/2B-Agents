# Loyalty Feature Expansion

## Project Purpose

This project focuses on improving the loyalty dashboard experience for members.

## Start Here

- `03-guides/README.md`

## Current Scope

The first scope is a clearer web view for points, tier progress, and recent loyalty activity.

## Where Inputs Are Stored

- `projects/loyalty-feature-expansion/01-input/requirements/`
- `projects/loyalty-feature-expansion/01-input/notes/meeting-notes/`
- `projects/loyalty-feature-expansion/01-input/assets/raw/`

## Where Main Outputs Are Stored

- `projects/loyalty-feature-expansion/02-output/ba/`
- `projects/loyalty-feature-expansion/02-output/design/`
- `projects/loyalty-feature-expansion/02-output/fe/`

## Knowledge Files

- `04-knowledge/glossary.md`
- `04-knowledge/business-rules.md`
- `04-knowledge/notes.md`

## Deep Ops Files

- `_ops/status.md`
- `_ops/decision-log.md`
- `_ops/task-tracker.md`
- `_ops/change-log.md`
- `_ops/dependency-map.md`
- `_ops/project-flow.md`
- `_ops/traceability/requirement-traceability-summary.md`
- `_ops/runtime/id-registry.yaml`
- `_ops/runtime/processing-state.yaml`
- `_ops/confirmations/pending-confirmations.yaml`
- `_ops/confirmations/pending-confirmations.md`
- `_ops/confirmations/decisions-log.md`

What they do:
- `_ops/status.md` shows overall progress and requirement status.
- `_ops/decision-log.md` records key decisions and their impact.
- `_ops/task-tracker.md` keeps a simple task board.
- `_ops/change-log.md` tracks version updates for generated requirement outputs.
- `_ops/dependency-map.md` shows prerequisite links (REQ -> FR -> FEAT) and downstream risks.
- `_ops/confirmations/` tracks pending business confirmations and saved decisions.

Version file per requirement output:
- `_ops/generated/<requirement-name>/version-info.md`

## How To Run This Project

```bash
python3 app.py --project loyalty-feature-expansion --input req-001.md
```
