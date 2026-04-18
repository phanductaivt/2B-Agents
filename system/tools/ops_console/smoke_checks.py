from __future__ import annotations

from pathlib import Path
import importlib.util
import sys


def _load_module(module_name: str, file_path: Path):
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Could not load module: {file_path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


BASE_DIR = Path(__file__).resolve().parents[3]
PROJECTS_DIR = BASE_DIR / "projects"

_DASHBOARD = _load_module(
    "dashboard_manager_for_ops_smoke_checks",
    BASE_DIR / "system" / "tools" / "project" / "dashboard_manager.py",
)
_MAPPER = _load_module(
    "state_mapper_for_ops_smoke_checks",
    BASE_DIR / "system" / "tools" / "ops_console" / "state_mapper.py",
)
_DOCS_API = _load_module(
    "docs_api_for_ops_smoke_checks",
    BASE_DIR / "system" / "tools" / "ops_console" / "docs_api.py",
)
_ACTIONS_API = _load_module(
    "actions_api_for_ops_smoke_checks",
    BASE_DIR / "system" / "tools" / "ops_console" / "actions_api.py",
)
_SEMANTICS = _load_module(
    "semantic_mapper_for_ops_smoke_checks",
    BASE_DIR / "system" / "tools" / "project" / "semantic_mapper.py",
)


def _assert(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def _check_summary_consistency() -> None:
    for project_dir in _DASHBOARD.discover_projects(PROJECTS_DIR):
        lines = _DASHBOARD._read_text(_DASHBOARD._PATHS.status_path(project_dir)).splitlines()
        requirements = _DASHBOARD._parse_requirements(lines)
        blockers = _DASHBOARD._collect_section(lines, "## Current Blockers")
        execution_dash = _DASHBOARD._build_execution_model(project_dir, blockers)
        summary_dash = _DASHBOARD._build_project_summary_model(
            project_dir=project_dir,
            status_lines=lines,
            requirements=requirements,
            blockers=blockers,
            execution=execution_dash,
        )

        summary_ops = _MAPPER.project_summary_model(project_dir)
        execution_ops = _MAPPER.execution_snapshot_model(project_dir)

        _assert(
            str(summary_dash.get("project_status")) == str(summary_ops.get("project_status")),
            f"{project_dir.name}: project_status mismatch between dashboard and ops mapper.",
        )
        _assert(
            int(summary_dash.get("project_progress", -1)) == int(summary_ops.get("project_readiness", -2)),
            f"{project_dir.name}: project readiness/progress mismatch.",
        )
        _assert(
            str(execution_dash.get("current_execution_owner")) == str(execution_ops.get("current_execution_owner")),
            f"{project_dir.name}: execution owner mismatch.",
        )
        _assert(
            str(execution_dash.get("blocked_reason")) == str(execution_ops.get("blocked_reason")),
            f"{project_dir.name}: blocked reason mismatch.",
        )


def _check_protected_boundaries() -> None:
    _assert(_DOCS_API._is_editable("01-input/requirements/req-001.md"), "requirements should be editable.")
    _assert(_DOCS_API._is_editable("04-knowledge/notes.md"), "knowledge notes should be editable.")
    _assert(not _DOCS_API._is_editable("_ops/runtime/processing-state.yaml"), "runtime state must stay protected.")
    _assert(not _DOCS_API._is_editable("_ops/generated/req-001/frs.md"), "generated runtime outputs must stay protected.")
    _assert(not _DOCS_API._is_editable("02-output/ba/frs.md"), "curated outputs must remain view-only.")


def _check_rerun_allow_deny() -> None:
    projects = _MAPPER.discover_projects(BASE_DIR)
    _assert(bool(projects), "No valid projects found for rerun checks.")
    project_name = projects[0].name

    denied = _ACTIONS_API.check_rerun_eligibility(
        BASE_DIR,
        {"action": "rerun_requirement", "project": project_name, "requirement": "req-does-not-exist"},
    )
    _assert(denied.get("eligible") is False, "Unknown requirement must be denied.")

    project_level = _ACTIONS_API.check_rerun_eligibility(
        BASE_DIR,
        {"action": "rerun_project", "project": project_name},
    )
    _assert("eligible" in project_level and "reason" in project_level, "Project rerun eligibility should return reasoned result.")


def _check_stale_vocabulary() -> None:
    allowed = {"fresh", "stale", "needs-rerun", "manual-override"}
    samples = ["fresh", "stale", "needs_rerun", "manual-override", "bad-value"]
    for raw in samples:
        normalized = _SEMANTICS.normalize_stale_state(raw)
        _assert(normalized in allowed, f"Invalid stale state normalization result: {normalized}")


def main() -> None:
    _check_summary_consistency()
    _check_protected_boundaries()
    _check_rerun_allow_deny()
    _check_stale_vocabulary()
    print("OK: ops_console smoke checks passed.")


if __name__ == "__main__":
    main()
