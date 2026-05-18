---
file_type: "Guardrail"
primary_agents: ["PO", "BA", "Architect", "Data", "BE", "UIUX", "FE", "QA", "Release"]
supporting_agents: []
activation_mode: "Always-On Shared"
lifecycle_stage: "System Core"
purpose: "Define the overall execution protocol for using project input, context, runbooks, agents, skills, and templates."
---
# Define Execution Protocol

## Primary Mode

Codex/AI is the only execution engine.

Execution happens directly in the repository by reading project inputs and writing final Markdown/HTML outputs.
For runnable delivery, execution may also create project application code under `02-output/app/`, backend tests under `02-output/app/backend/tests/`, QA smoke planning under `02-output/qa/`, and verification evidence under `02-output/release/`.

## Standard Flow

1. Read business input from `01-input/`
2. Read project context from `03-context/`
3. Read the relevant runbook in `system/runbooks/`
4. Generate final outputs in `02-output/`
5. When runnable software is requested, generate app code in `02-output/app/`, backend tests beside backend code, QA smoke planning in `02-output/qa/`, and verification output in `02-output/release/`

## Skill Binding Rule

- when a runbook declares `Required Skills`, those skills are part of the execution contract, not optional flavor
- when a runbook declares `Optional Skills`, invoke them when the stated condition is true
- do not replace a required skill with general freeform writing if the repository already provides that skill
- if a skill is not enough to resolve a gap safely, use `resolve-clarification.md` instead of guessing

## Runnable Claim Rule

- do not call a project runnable until `verify-runnable-system.md` records command results
- a reviewable prototype is not the same as a runnable system
- local runnable does not imply deploy ready
