---
file_type: "Rule"
primary_agents: ["PO", "BA", "Architect", "Data", "BE", "UIUX", "FE", "QA", "Release"]
supporting_agents: []
activation_mode: "Always-On Shared"
lifecycle_stage: "System Core"
purpose: "Define the overall system flow from business input to final output."
---
# Define System Overview

## Current Repository Model

The repository is a pure AI Operating Repository.

Primary flow:
- business input lives in `projects/<project>/01-input/`
- project context lives in `projects/<project>/03-context/`
- Codex uses `system/rules/`, `system/guardrails/`, `system/runbooks/`, `system/agents/`, `system/agent-knowledge/`, `system/skills/`, and `system/templates/`
- final artifacts live directly in `projects/<project>/02-output/`
- runnable code lives in `projects/<project>/02-output/app/`
- smoke test planning lives in `projects/<project>/02-output/qa/`

## Main Artifact Flow

- requirement + project context -> PO BRD
- PO BRD + project context -> BA package
- PO BRD + BA package -> architecture package
- PO BRD + BA + architecture -> data package
- PO BRD + BA + architecture + data -> BE package and FastAPI backend
- BA package -> wireframe
- BA package + wireframe + BE package -> FE UI and Vite React frontend
- PO BRD + BA + backend + design + FE outputs -> QA package
- all outputs + app + tests -> release package and runnable-system verification

## Delivery Collaboration

- BE and FE should stay aligned on request, response, validation, and error behavior
- FE should not guess backend contract behavior from the FRS alone when a BE package exists
- BE should not invent business scope beyond the BRD and BA package
- Architect and Data should reduce implementation guessing before BE and FE generate code
- QA should review the same slice end-to-end and make quality risks visible before the team treats the slice as ready
- Release should not call a system runnable without command evidence

## BA And PO Quality Expectation

The PO BRD is considered good only when:
- the problem, business objective, scope boundaries, and success measures are visible
- BACCM framing is visible
- requirement classification is visible
- assumptions and open questions are separated
- tradeoffs are explicit when they affect the first slice

The BA package is considered good only when:
- ambiguity is reduced visibly
- assumptions and open questions are explicit
- scope boundaries and first release slice are visible
- rules, exception behavior, and dependencies are covered enough for downstream handoff
