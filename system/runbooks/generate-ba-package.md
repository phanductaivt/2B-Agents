---
file_type: "Runbook"
primary_agents: ["BA"]
supporting_agents: ["PO"]
activation_mode: "Triggered By Workflow"
lifecycle_stage: "System Core"
purpose: "Generate the BA package from business input, project context, and the PO BRD."
reads: ["01-input/requirements/", "03-context/", "02-output/po/<req>-brd.md", "system/rules/", "system/guardrails/", "system/skills/", "system/templates/"]
produces: ["02-output/ba/<req>-clarification.md", "02-output/ba/<req>-process-bpmn.md", "02-output/ba/<req>-user-story.md", "02-output/ba/<req>-acceptance-criteria.md", "02-output/ba/<req>-frs.md", "02-output/ba/<req>-feature-list.md"]
---
# Generate BA Package

Use this runbook to generate the BA package for one requirement.

## Required Skills

- `requirement-clarifier`
- `ambiguity-checker-plus`
- `frs-drafter`
- `user-story-writer`
- `acceptance-criteria-writer`
- `bpmn-mermaid-writer`
- `feature-breakdown-writer`

## Optional Skills

- `process-analyzer`
  - use when the process flow has AS-IS / TO-BE complexity
- `scope-boundary-checker`
  - use when the slice still feels too broad
- `rule-coverage-checker`
  - use when business rules are critical or spread across multiple artifacts
- `exception-scenario-expander`
  - use when the happy path is clearer than the failure path

## Inputs

- `01-input/requirements/<req>.md`
- relevant files from `03-context/`
- upstream PO BRD in `02-output/po/`
- relevant rules, agents, skills, and templates

## Steps

1. Read in this order:
   - `01-input/requirements/<req>.md`
   - relevant files from `03-context/`
   - matching PO BRD in `02-output/po/`
   - BA agent guidance, execution rules, and templates
2. Invoke `requirement-clarifier` and run discovery first:
   - confirm the BRD intent, business objective, and first-slice scope
   - extract the requirement insight and current pain point
   - identify the primary actor or stakeholder
   - identify expected business value
   - identify hard business rules, policy constraints, and release boundaries
   - separate facts, assumptions, blocking questions, non-blocking questions, constraints, and out-of-scope items
3. Invoke `ambiguity-checker-plus` as a required quality pass before BPMN, story, acceptance criteria, FRS, or feature breakdown:
   - check actor, value, rule, scope, release, data, permission, dependency, and success ambiguity
   - classify each question as `blocking`, `non-blocking`, or `assumption-backed`
   - recommend whether the BA package should proceed, proceed with assumptions, or be blocked
4. Ask clarification only when a missing rule or conflict would materially change the final BA package.
5. Infer with best effort when:
   - wording is incomplete but the business intent is still clear
   - a success measure is missing but can be marked as missing without blocking analysis
   - secondary labels or wording details do not change scope or behavior
6. Write `<req>-clarification.md` before any other BA output with these required sections:
   - Insight & Pain Point
   - Known Facts
   - Assumptions
   - Blocking Questions
   - Non-Blocking Questions
   - Recommended Decision: `Proceed`, `Proceed with assumptions`, or `Blocked`
   - User Approval Status: `Pending User Approval`, `Approved - Proceed`, `Approved - Proceed with assumptions`, or `Blocked`
   - Downstream Readiness Notes
7. Stop after writing the clarification artifact when `User Approval Status` is `Pending User Approval` or `Blocked`; do not create BPMN, user story, acceptance criteria, FRS, feature list, or downstream outputs.
   - final response must name `02-output/ba/<req>-clarification.md` as the review file
   - final response must list the exact sections the user should read
   - final response must state the recommended decision, current approval status, and acceptable approval replies
8. If process complexity spans multiple actors, states, or before/after flow shifts:
   - invoke `process-analyzer`
9. If the slice still feels too broad or mixed:
   - invoke `scope-boundary-checker`
10. If the user explicitly approves downstream BA work, create or complete the BA outputs in this order directly in `02-output/ba/`:
   - `<req>-clarification.md`
   - `<req>-process-bpmn.md`
   - `<req>-user-story.md`
   - `<req>-acceptance-criteria.md`
   - `<req>-frs.md`
   - `<req>-feature-list.md`
11. Use this artifact intent while writing:
   - clarification = make insight, pain point, BRD gaps, facts, assumptions, blocking questions, non-blocking questions, and readiness decision visible
   - BPMN = invoke `bpmn-mermaid-writer` to show main path and important branches
   - user story = invoke `user-story-writer` to state the first-slice user need and value
   - acceptance criteria = invoke `acceptance-criteria-writer` to make the first slice testable
   - FRS = invoke `frs-drafter` to describe observable functional behavior for downstream teams
   - feature list = invoke `feature-breakdown-writer` to organize scope into non-overlapping release-ready slices
12. If business rules are critical across multiple artifacts:
   - invoke `rule-coverage-checker`
13. If failure, fallback, restriction, or negative-path behavior is still thin:
   - invoke `exception-scenario-expander`
14. Before finishing, self-check:
   - insight, pain point, actor, and expected value are visible in clarification
   - every clarification question is classified as blocking, non-blocking, or assumption-backed
   - `Recommended Decision` and `User Approval Status` are present and respected
   - downstream BA outputs are not created unless user approval is explicit
   - ambiguity is reduced visibly
   - PO BRD and FRS do not contradict each other
   - BPMN branches appear in FRS alternative flows when relevant
   - user story and acceptance criteria fit the same scope as the PO BRD and FRS
   - feature list does not drift or duplicate functional scope
   - unresolved gaps are visible instead of hidden
   - downstream UIUX and FE work will not need to guess core behavior
