# Projects

This folder stores real project work.

Each project should keep its own:
- inputs
- outputs
- knowledge
- project config
- project README
- status
- decision log
- task tracker
- change log
- dependency map

Tracking file purposes:
- `status.md`: main progress snapshot for the project and each requirement
- `decision-log.md`: key decisions with date, reason, and impact
- `task-tracker.md`: lightweight task board
- `change-log.md`: version history for generated requirement outputs
- `dependency-map.md`: project-level dependency links and downstream risk view

The dashboard:
- `projects/dashboard.md` summarizes all projects in one place
- it is generated from each project's `status.md`
 - `projects/dashboard.html` is a simple web view of the same data

Each project also includes:
- `project-flow.md` for a visual flow of inputs, agents, outputs, and status updates
This file is auto-generated after `python3 app.py` runs.

Each processed requirement also has:
- `outputs/generated/<requirement-name>/requirement-flow.md`
This file shows requirement-level traceability.

Traceability outputs:
- `outputs/generated/<requirement-name>/requirement-traceability-matrix.md`
- `outputs/generated/<requirement-name>/requirement-traceability-flow.md`
- `requirement-traceability-summary.md` in the project folder

Test case output:
- `outputs/generated/<requirement-name>/test-cases.md`
- `outputs/generated/<requirement-name>/version-info.md` for requirement-level versions
- `outputs/generated/<requirement-name>/artifact-status.md` for artifact-by-artifact status
- `outputs/generated/<requirement-name>/artifact-checklist.md` for practical completion checks
- `outputs/generated/<requirement-name>/gate-report.md` for gate and approval visibility
- `outputs/generated/<requirement-name>/risk-notes.md` for review-stage risk summary

Requirement ID system:
- `id-registry.yaml` keeps a simple mapping from input file to requirement ID
- all downstream IDs (BRD, FR, US, AC, FEAT, UI, RV, TC) are stored there too
ID format example: `REQ-001`, `BRD-001`, `FR-001`, `US-001`, `AC-001`, `FEAT-001`, `UI-001`, `RV-001`, `TC-001`

Version rules:
- First generation: `v1.0`
- Meaningful regeneration: `v1.1`, `v1.2`, ...
- Larger structural changes can move to a new major version such as `v2.0`

Auto context injection:
- The run pipeline auto-loads global context files from `context/`
- The run pipeline auto-loads project context files from `projects/<project-name>/knowledge/`
- You do not need to type manual context-loading prompts for normal runs

## Why This Matters

- each project stays separate in VS Code
- input and output are easier to control
- project knowledge stays close to the real work
- the reusable system stays clean

## Included Here

- `project-template/`
- `ticket-booking-improvement/`
- `loyalty-feature-expansion/`

## How To Create A New Project

1. Copy `project-template/`
2. Rename the copied folder
3. Update `project-config.yaml`
4. Update `status.md`, `decision-log.md`, and `task-tracker.md`
5. Update `README.md`
6. Add project knowledge files
7. Add your first input file in `projects/<project-name>/inputs/requirements/`

## Which Files To Fill First

Start with:
- `project-config.yaml`
- `status.md`
- `decision-log.md`
- `task-tracker.md`
- `knowledge/business-rules.md`
- `knowledge/glossary.md`
- `projects/<project-name>/inputs/requirements/req-001.md`

## How To Run One Project

Example:

```bash
python3 app.py --project ticket-booking-improvement
```

Controlled artifact mode example:

```bash
python3 app.py --project ticket-booking-improvement --requirement req-001.md --mode controlled
```

One stage example:

```bash
python3 app.py --project ticket-booking-improvement --requirement req-001.md --stage ba-core
```

One artifact example:

```bash
python3 app.py --project ticket-booking-improvement --requirement req-001.md --artifact frs
```

After running, `status.md` is updated with a row for each processed requirement.

To refresh the dashboard:

```bash
python3 app.py --dashboard
```

Open `projects/dashboard.md` in VS Code for editing.
Open `projects/dashboard.html` in a browser for a visual view.
Use the filter buttons or search box to narrow projects.

Visual system guides:
- [system-flow.md](/Users/macbookair/2B%20Agents/visuals/system-flow.md)
- [agent-flow.md](/Users/macbookair/2B%20Agents/visuals/agent-flow.md)
- [playbook-flow.md](/Users/macbookair/2B%20Agents/visuals/playbook-flow.md)

<!-- TODO: Add a short checklist for archiving completed projects later. -->
