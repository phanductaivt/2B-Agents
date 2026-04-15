# Ticket Booking Improvement

## Project Purpose

This project focuses on improving the ticket change and refund support experience.

## Start Here

- `03-guides/README.md`

## Current Scope

The first scope is a clearer self-service booking change flow for web users.

## Where Inputs Are Stored

- `projects/ticket-booking-improvement/01-input/requirements/`
- `projects/ticket-booking-improvement/01-input/notes/meeting-notes/`
- `projects/ticket-booking-improvement/01-input/assets/raw/`

## Where Main Outputs Are Stored

- `projects/ticket-booking-improvement/02-output/ba/`
- `projects/ticket-booking-improvement/02-output/design/`
- `projects/ticket-booking-improvement/02-output/fe/`

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

What they do:
- `_ops/status.md` shows overall progress and requirement status.
- `_ops/decision-log.md` records key decisions and their impact.
- `_ops/task-tracker.md` keeps a simple task board.
- `_ops/change-log.md` tracks version updates for generated requirement outputs.
- `_ops/dependency-map.md` shows prerequisite links (REQ -> FR -> FEAT) and downstream risks.

Version file per requirement output:
- `_ops/generated/<requirement-name>/version-info.md`

## How To Run This Project

```bash
python3 app.py --project ticket-booking-improvement --input req-001.md
```
