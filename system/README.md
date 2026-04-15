# System Layer

This folder contains shared, reusable engine components for all projects.

## Structure

- `system/agents/`
- `system/artifacts/`
- `system/configs/`
- `system/context/`
- `system/knowledge/`
- `system/memory/`
- `system/playbooks/`
- `system/prompts/`
- `system/scenarios/`
- `system/skills/`
- `system/templates/`
- `system/tools/`
- `system/validators/`
- `system/tests/`

## Purpose

Use `system/` for components reused across many projects:
- orchestration logic
- governance rules
- context pack
- templates and validators
- shared knowledge

Project data should not be stored here.
Project-specific work remains in `projects/<project-name>/`.
