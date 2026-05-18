---
file_type: "Runbook"
primary_agents: ["PO"]
supporting_agents: ["BA"]
activation_mode: "Triggered By Workflow"
lifecycle_stage: "System Core"
purpose: "Generate a PO-owned BRD from business input and project context."
reads: ["01-input/requirements/", "03-context/", "system/rules/", "system/guardrails/", "system/skills/", "system/templates/"]
produces: ["02-output/po/<req>-brd.md"]
---
# Generate BRD

Use this runbook to create a PO-owned BRD for one requirement or one small initiative.

## Required Skills

- `brd-drafter`
- `baccm-product-framer`
- `requirement-classifier`
- `requirement-clarifier`
  - required when the raw requirement does not clearly state insight, pain point, actor, and expected value

## Optional Skills

- `market-research-synthesizer`
  - use when current market conditions or competitor patterns could change product direction
- `prioritization-helper`
  - use when scope pressure or sequencing tradeoffs matter

## Inputs

- `01-input/requirements/<req>.md`
- relevant files from `03-context/`
- relevant rules, agents, skills, and templates

## Steps

1. Read the requirement and project context first.
2. Determine whether current market conditions or competitor patterns materially affect product direction.
3. If market-sensitive decisions matter and the repository does not already contain enough current market information:
   - invoke `market-research-synthesizer`
   - research current market conditions
   - separate verified observations from inference and recommendation
4. If the raw requirement does not clearly state the product insight, current pain point, actor, expected value, or critical business rules:
   - invoke `requirement-clarifier`
   - identify supplemental clarification questions before drafting the BRD
   - classify each question as `blocking`, `non-blocking`, or `assumption-backed`
5. Invoke `baccm-product-framer` to frame the change using BACCM:
   - Change
   - Need
   - Solution
   - Stakeholder
   - Value
   - Context
6. Invoke `requirement-classifier` to classify the requirement statements into:
   - business requirements
   - stakeholder requirements
   - solution requirements
   - transition requirements
7. Invoke `brd-drafter` and define:
   - insight and current pain point
   - why now or business need
   - business objective
   - first-slice scope and out-of-scope boundaries
   - success measures
   - what must be clarified before delivery
   - priority or tradeoff notes
   - assumptions, non-blocking questions, and open questions
   - recommended decision, while leaving user approval status pending for downstream execution
8. If scope pressure or sequencing tradeoffs matter:
   - invoke `prioritization-helper`
9. Ask clarification only when a missing answer would materially change:
   - the product problem framing
   - the first-slice scope
   - the success direction
   - the requirement classification
10. Write the BRD directly to `02-output/po/`:
   - `<req>-brd.md`
   - or `<initiative>-brd.md` when the work is not requirement-scoped
11. Before finishing, verify:
   - the insight and pain point are visible
   - the problem is specific
   - the actor or stakeholder is visible
   - the business objective is measurable or explicitly marked as still missing
   - BACCM framing is visible
   - requirement classification is complete and understandable
   - in-scope and out-of-scope boundaries are clear
   - success measures are not vague
   - blocking questions, non-blocking questions, assumptions, recommended decision, and user approval status are separated
   - priority or tradeoff notes are visible when they matter
12. Hand the BRD to BA as upstream framing input for clarification, BPMN, story, acceptance criteria, FRS, and feature breakdown.
