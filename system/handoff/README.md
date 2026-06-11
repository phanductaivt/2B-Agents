---
file_type: "Handoff Governance Index"
primary_agents: []
supporting_agents: ["PO", "BA", "Architect", "Data", "BE", "UIUX", "FE", "QA", "Release"]
activation_mode: "On Pause Or Executor Change"
lifecycle_stage: "System Core"
purpose: "Define repository-wide continuity between AI Executors, Agent phases, and work sessions."
---
# Repository Handoff

## Purpose

`system/handoff/` is the repository-wide continuity layer for paused work,
session changes, and AI Executor switching.

It preserves the current work state without treating the AI Executor as the
active Agent. The handoff points to source files and evidence; it does not
replace runbooks, Agent definitions, project outputs, or approval records.

## Canonical Files

- `latest-handoff.md`: current active task continuity record.
- `handoff-template.md`: required handoff structure.
- `update-handoff-runbook.md`: procedure for updating continuity state.
- `switch-ai-executor-runbook.md`: procedure for changing AI Executors safely.
- `system/executors/executor-contract.md`: required Executor behavior.
- `system/executors/executor-switching-policy.md`: switching policy.
- `system/workflows/workflow-lifecycle.md`: workflow transition and handoff
  requirements.

## Required Separation

Every handoff must identify these independently:

- Active Executor
- Active Agent
- Active Workflow
- Active Phase
- Active Runbook
- Active Project
- Active Task ID

The Active Executor is the AI system or client performing work. The Active
Agent is the instruction-defined role currently activated by the runbook.

When Filesystem/Workspace MCP is relevant, record its exact workspace scope,
approval requirements, denied actions, and unrelated dirty-work boundary under
Available MCP Tools and Permission Profile. Record local Git/GitHub usage
separately as non-MCP command/tool evidence when relevant.

## When To Update

Update `latest-handoff.md` when:

- incomplete work is paused
- the user may switch AI Executors
- Active Workflow, Active Phase, Active Runbook, Active Agent, Active Executor,
  or active project changes
- files were created or modified
- validation was performed or failed
- permissions, tools, MCP availability, risks, or uncertainty changed

## Handoff Reading Rule

The incoming Executor must:

1. Read `latest-handoff.md`.
2. Confirm the Active Task ID and project.
3. Verify its own capabilities and permissions.
4. Load only the active runbook and files referenced by the handoff.
5. Avoid bulk-reading the repository.
6. Preserve unrelated dirty work.
7. Stop when the handoff is stale, conflicting, or insufficient for safe work.

## Scope And Freshness

`latest-handoff.md` is authoritative only for the one task identified by its
Active Task ID. It must not be treated as a historical log or as authority for
another project.

Uncertainty: concurrent active tasks are not yet governed by task-specific
handoff files. Confirm the current task before replacing `latest-handoff.md`.

## Compatibility Note

The previous location `system/component-factory/handoff/` remains as a
compatibility pointer. Do not update handoff state there.
