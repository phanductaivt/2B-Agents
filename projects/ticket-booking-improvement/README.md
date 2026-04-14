# Ticket Booking Improvement

## Project Purpose

This project focuses on improving the ticket change and refund support experience.

## Current Scope

The first scope is a clearer self-service booking change flow for web users.

## Where Inputs Are Stored

- `projects/ticket-booking-improvement/inputs/requirements/`
- `projects/ticket-booking-improvement/inputs/meeting-notes/`
- `projects/ticket-booking-improvement/inputs/raw/`

## Where Outputs Are Stored

- `projects/ticket-booking-improvement/outputs/generated/`

## Knowledge Files

- `knowledge/glossary.md`
- `knowledge/business-rules.md`
- `knowledge/notes.md`

## Project Management Files

- `status.md`
- `decision-log.md`
- `task-tracker.md`
- `change-log.md`
- `dependency-map.md`

What they do:
- `status.md` shows overall progress and requirement status.
- `decision-log.md` records key decisions and their impact.
- `task-tracker.md` keeps a simple task board.
- `change-log.md` tracks version updates for generated requirement outputs.
- `dependency-map.md` shows prerequisite links (REQ -> FR -> FEAT) and downstream risks.

Version file per requirement output:
- `outputs/generated/<requirement-name>/version-info.md`

## How To Run This Project

```bash
python3 app.py --project ticket-booking-improvement --input req-001.md
```
