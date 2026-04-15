# Restructure Report

## Scope

Safe in-place refactor to 3 layers:
- `projects/`
- `system/`
- `workspace/`

## Folder Relocation

- `agents/` -> `system/agents/`
- `artifacts/` -> `system/artifacts/`
- `configs/` -> `system/configs/`
- `context/` -> `system/context/`
- `knowledge/` -> `system/knowledge/`
- `memory/` -> `system/memory/`
- `playbooks/` -> `system/playbooks/`
- `prompts/` -> `system/prompts/`
- `skills/` -> `system/skills/`
- `templates/` -> `system/templates/`
- `tools/` -> `system/tools/`
- `validators/` -> `system/validators/`
- `tests/` -> `system/tests/`
- `visuals/` -> `workspace/visuals/`
- `logs/` -> `workspace/logs/`

## Dashboard Relocation

- `projects/dashboard.md` -> `workspace/dashboard.md`
- `projects/dashboard.html` -> `workspace/dashboard.html`

## Major Path Updates

- Root `app.py` now loads modules from `system/tools/...`
- Config/artifact/template paths now use `system/...`
- Logging now writes to `workspace/logs/...`
- Dashboard generation now writes to `workspace/dashboard.*`

## Manual Checks Recommended

1. Run `python3 app.py --dashboard`
2. Run `python3 app.py --sync-context`
3. Run one project pipeline command and confirm output paths
4. Open `workspace/dashboard.md` and verify project links

