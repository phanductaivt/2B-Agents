---
file_type: "System Guide"
primary_agents: ["PO", "BA", "Architect", "Data", "BE", "UIUX", "FE", "QA", "Release"]
supporting_agents: []
activation_mode: "Manual Navigation"
lifecycle_stage: "System Core"
purpose: "Explain the active system layer, naming conventions, and operating responsibilities."
---
# System

The active system layer is the AI operating layer.

Naming convention:
- runbooks, rules, and guardrails should use a clear `Action + Object` pattern where practical
- templates should use `Template - Object`
- checklists should use `Checklist - Object`

## Active Folders

- `rules/`
- `guardrails/`
- `runbooks/`
- `agents/`
- `agent-knowledge/`
- `skills/`
- `templates/`
- `artifacts/`

## How It Works

- `rules/` defines the operating rules AI should follow
- `guardrails/` defines execution contracts, clarification rules, and verification rules
- `runbooks/` provides reusable workflow prompts
- `agents/` defines role-based operating behavior
- `agents/define-agent-usage-matrix.md` provides one-table navigation for agent ownership and usage
- `agent-knowledge/` provides optional supporting knowledge by agent
- `skills/` provides focused capability instructions
- `templates/` provides reusable output structures grouped by document type:
  - `requirements/`
  - `data/`
  - `technical-design/`
  - `design/`
  - `quality/`
  - `checklists/`
- `artifacts/` defines the final artifact catalog in Markdown

For PO and BA work, the active operating model now assumes:
- PO creates the BRD first
- PO may research current market conditions when market-sensitive decisions matter
- PO classifies the work into business, stakeholder, solution, and transition requirements
- BA owns the analysis package after framing is clear
- Architect owns architecture, NFR, and security review before runnable implementation
- Data owns data model, state transition, SQLite schema planning, and metric tracking plans
- BE owns API and service design after BA functional behavior is clear
- QA owns test design, negative-path coverage, and release-readiness review after delivery artifacts are visible
- Release owns local runnable verification, run instructions, and runnable status evidence
- ambiguity reduction happens before downstream handoff
- downstream agents must wait for explicit user approval after the clarification gate
- scope boundaries and first-release slicing are explicit

Runnable delivery uses:
- `02-output/app/backend/` for FastAPI code
- `02-output/app/frontend/` for Vite React TypeScript code
- `02-output/qa/` for smoke test planning
- `02-output/release/` for actual runnable verification evidence

## Project Context Rule

Project-specific context does not live in `system/`.

It belongs in:
- `projects/<project>/03-context/`
