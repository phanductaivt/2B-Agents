# Architecture

This framework now uses a project-based BA-led product development flow.

The separate PO Agent was removed because the BA Agent now owns both:
- business analysis
- product structuring and feature decomposition

## Core Flow

`projects/<project-name>/inputs -> BA agent -> UXUI agent -> FE agent -> validators -> projects/<project-name>/outputs/generated`

## Two Simple Layers

### 1. System Layer

The system layer stores reusable parts:
- agents
- skills
- playbooks
- validators
- prompts
- templates
- tools
- shared knowledge

These do not belong to one project only.

### 2. Project Layer

The project layer stores real work:
- project inputs
- project outputs
- project knowledge
- project config
- project README

This makes each project easier to manage inside VS Code.

## Step-by-Step Explanation

### 1. Project

Each project lives inside:

`projects/<project-name>/`

Each project has:
- `project-config.yaml`
- `projects/<project-name>/inputs/`
- `projects/<project-name>/outputs/`
- `knowledge/`
- `README.md`
- `status.md`
- `decision-log.md`
- `task-tracker.md`
- `change-log.md`
- `dependency-map.md`

Root-level input/output folders are removed.
Only project folders under `projects/<project-name>/` are valid working paths.

The tracking files are simple:
- `status.md` shows overall progress and requirement status
- `decision-log.md` keeps key decisions and their impact
- `task-tracker.md` is a lightweight task board
- `change-log.md` keeps a simple version history for generated requirement packages
- `dependency-map.md` shows requirement/FR/feature prerequisites and dependency risks

The dashboard (`projects/dashboard.md`) summarizes all projects by reading each project's `status.md`.

Each project also has a `project-flow.md` file that visualizes its own input-to-output flow.
Each requirement also has a `requirement-flow.md` file inside its output folder.
Requirement traceability files are generated per requirement and summarized at the project level.
Each requirement can also have artifact-level governance files:
- `artifact-status.md`
- `artifact-checklist.md`
- `gate-report.md`
Each project maintains a simple `id-registry.yaml` that maps input files to IDs for REQ, BRD, FR, US, AC, FEAT, UI, RV, and TC.
ID format example: REQ-001, BRD-001, FR-001, US-001, AC-001, FEAT-001, UI-001, RV-001, TC-001.

Test cases (`test-cases.md`) are generated per requirement from the BA package (FRS, user story, acceptance criteria) and linked using these IDs.
Each requirement output folder also contains `version-info.md` so the team can track version, change summary, and affected IDs over time.

Visual references:
- [system-flow.md](/Users/macbookair/2B%20Agents/visuals/system-flow.md)
- [agent-flow.md](/Users/macbookair/2B%20Agents/visuals/agent-flow.md)
- [playbook-flow.md](/Users/macbookair/2B%20Agents/visuals/playbook-flow.md)

### 2. Inputs

Inputs now belong to the selected project.

Examples:
- `projects/<project-name>/inputs/requirements/`
- `projects/<project-name>/inputs/meeting-notes/`
- `projects/<project-name>/inputs/raw/`

This keeps project files separate from each other.

### 3. Project Config

Each project has its own `project-config.yaml`.

It explains:
- project name
- description
- owner
- default playbook
- domain
- active agents
- project notes

This helps the system know what kind of work it is running.

### 4. Project Knowledge

Each project may also have its own knowledge files:
- `glossary.md`
- `business-rules.md`
- `notes.md`

Knowledge priority is simple:
1. project knowledge
2. shared system knowledge
3. generic fallback in code

This means the system uses the selected project's context first whenever possible.

### 5. BA Agent

The BA Agent is now the main analysis and product-structuring agent.

Typical outputs:
- clarification
- BPMN-style Mermaid process
- user story
- acceptance criteria
- BRD
- FRS
- feature list

### 6. UXUI Agent

The UXUI Agent turns the BA FRS into a simple wireframe.

Typical outputs:
- wireframe markdown
- layout notes
- screen sections

### 7. FE Agent

The FE Agent turns the agreed BA and UXUI flow into a simple HTML page.

Typical outputs:
- HTML demo page

### 8. Validators

Validators act as quality gates.

They check things like:
- ambiguity
- completeness
- consistency
- template fit

The goal is to catch weak output before it is shared with a team.

### 9. Outputs

The output layer writes Markdown files that business users can read and edit directly, plus a simple HTML file from the FE Agent.

Outputs now belong to the selected project:

`projects/<project-name>/outputs/generated/<input-name>/`

Examples:
- `clarification.md`
- `process-bpmn.md`
- `user-story.md`
- `acceptance-criteria.md`
- `brd.md`
- `frs.md`
- `feature-list.md`
- `wireframe.md`
- `review-notes.md`
- `ui.html`

## Playbook vs Project

- Playbook: reusable end-to-end process
- Project: reusable container of real work items

Example:
- the `product-development` playbook can be reused in many different projects
- each project still keeps its own inputs, knowledge, and outputs

## Execution Modes

1. Full mode
- Generates the whole package in one run for each requirement.

2. Controlled mode
- Generates one artifact at a time.
- Checks dependency gates before downstream artifacts.
- Supports manual approval states for each artifact.

## Why This Design Helps BA/PO Work

- each project stays separate and easier to review
- outputs are easier to find because they stay inside the project
- project knowledge stays close to the project itself
- playbooks stay reusable across many projects
- the BA package remains the main source of truth for UXUI and FE

## Why PO Agent Was Removed

- one BA-led package is easier to review than a split analysis and product-structuring package
- feature decomposition now stays closer to BRD and FRS
- UXUI and FE teams now receive one cleaner source of truth from the BA Agent

## Simple Example

1. A BA opens `projects/ticket-booking-improvement/`.
2. The BA updates `status.md`, `decision-log.md`, and `task-tracker.md` as needed.
3. The BA adds or updates an input file in `projects/<project-name>/inputs/requirements/`.
4. `app.py` loads that project's config and project knowledge.
5. The BA Agent creates clarification, BPMN Mermaid, BRD, FRS, story, acceptance criteria, and feature list.
6. The UXUI Agent creates a Markdown wireframe from the BA FRS.
7. The FE Agent creates a simple HTML page from the BA FRS and wireframe.
8. Validators review the package.
9. Final Markdown and HTML files are written to `projects/<project-name>/outputs/generated/<input-name>/`.
10. Version tracking is updated (`version-info.md` in output folder + project `change-log.md`).
11. `status.md` is updated so the requirement row shows BA, UXUI, FE, and Reviewer progress.
12. `dependency-map.md` is regenerated to show prerequisite links and downstream risk.

<!-- TODO: Add a simple Mermaid diagram for the full project-based flow. -->
