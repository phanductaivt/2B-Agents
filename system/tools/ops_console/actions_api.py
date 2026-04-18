from __future__ import annotations

from pathlib import Path
import importlib.util
import subprocess
import sys
from typing import Any
from datetime import datetime


def _load_module(module_name: str, file_path: Path):
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Could not load module: {file_path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


_MAPPER = _load_module(
    "state_mapper_for_ops_actions_api",
    Path(__file__).resolve().parent / "state_mapper.py",
)
_STALENESS = _load_module(
    "staleness_engine_for_ops_actions_api",
    Path(__file__).resolve().parent / "staleness_engine.py",
)
_ARTIFACT_RUNNER = _load_module(
    "artifact_runner_for_ops_actions_api",
    Path(__file__).resolve().parents[1] / "project" / "artifact_runner.py",
)
_PATHS = _load_module(
    "project_paths_for_ops_actions_api",
    Path(__file__).resolve().parents[1] / "project" / "project_paths.py",
)
_SEMANTICS = _load_module(
    "semantic_mapper_for_ops_actions_api",
    Path(__file__).resolve().parents[1] / "project" / "semantic_mapper.py",
)

_CATALOG_PATH = Path(__file__).resolve().parents[2] / "artifacts" / "artifact-catalog.yaml"
_ALLOWED_ACTIONS = {"rerun_project", "rerun_requirement", "rerun_from_stage"}
_TIMEOUT_SECONDS = 1800


def _requirement_name(value: str) -> str:
    text = str(value or "").strip()
    if not text:
        return ""
    if text.endswith(".md"):
        text = text[:-3]
    return text


def _collect_stale_documents(project_dir: Path) -> list[dict[str, Any]]:
    state = _STALENESS.load_state(project_dir)
    documents = state.get("documents", {})
    if not isinstance(documents, dict):
        return []
    rows: list[dict[str, Any]] = []
    for relative, entry in documents.items():
        if not isinstance(entry, dict):
            continue
        stale_state = _SEMANTICS.normalize_stale_state(str(entry.get("stale_state", "fresh")))
        if stale_state not in {"stale", "needs-rerun", "manual-override"}:
            continue
        rows.append(
            {
                "file_path": str(relative),
                "stale_state": stale_state,
                "rerun_recommendation": str(entry.get("rerun_recommendation", "none")),
                "impacted_requirements": list(entry.get("impacted_requirements", [])),
                "impacted_artifacts": list(entry.get("impacted_artifacts", [])),
                "impacted_stages": list(entry.get("impacted_stages", [])),
                "reason": list(entry.get("reason", [])),
                "last_edit_at": str(entry.get("last_edit_at", "")),
            }
        )
    return rows


def _editable_paths_for_staleness(project_dir: Path) -> list[Path]:
    paths: list[Path] = []
    for root in (_PATHS.requirements_dir(project_dir), _PATHS.notes_dir(project_dir)):
        if root.exists():
            for path in sorted(root.rglob("*")):
                if path.is_file() and path.suffix.lower() in {".md", ".txt"}:
                    paths.append(path)
    for relative in [
        _PATHS.knowledge_dir(project_dir) / "business-rules.md",
        _PATHS.knowledge_dir(project_dir) / "notes.md",
        _PATHS.decision_log_path(project_dir),
    ]:
        if relative.exists() and relative.is_file():
            paths.append(relative)
    confirmations_dir = _PATHS.confirmations_dir(project_dir)
    if confirmations_dir.exists():
        for path in sorted(confirmations_dir.glob("*.md")):
            if path.is_file():
                paths.append(path)
    return paths


def _parse_timestamp(value: str) -> datetime | None:
    text = str(value or "").strip()
    if not text:
        return None
    for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%d"):
        try:
            return datetime.strptime(text, fmt)
        except ValueError:
            continue
    return None


def _staleness_needs_refresh(project_dir: Path) -> bool:
    state_path = _PATHS.ops_console_staleness_path(project_dir)
    if not state_path.exists():
        return True
    state = _STALENESS.load_state(project_dir)
    updated_at = _parse_timestamp(str(state.get("updated_at", "")))
    if updated_at is None:
        return True
    for path in _editable_paths_for_staleness(project_dir):
        try:
            modified = datetime.fromtimestamp(path.stat().st_mtime)
        except OSError:
            continue
        if modified > updated_at:
            return True
    return False


def _refresh_staleness_snapshot(project_dir: Path) -> str:
    state = _STALENESS.load_state(project_dir)
    docs = state.get("documents", {})
    if not isinstance(docs, dict):
        docs = {}
        state["documents"] = docs

    tracked_relatives: set[str] = set(str(key) for key in docs.keys())
    for path in _editable_paths_for_staleness(project_dir):
        try:
            relative = str(path.relative_to(project_dir)).replace("\\", "/")
        except ValueError:
            continue
        tracked_relatives.add(relative)

    for relative in sorted(tracked_relatives):
        _STALENESS.evaluate_document(project_dir, state, relative)
    _STALENESS.save_state(project_dir, state)
    return "Stale-state snapshot refreshed from editable upstream documents."


def _stale_rows_with_freshness_guard(project_dir: Path) -> tuple[list[dict[str, Any]], list[str]]:
    guard_notes: list[str] = []
    if _staleness_needs_refresh(project_dir):
        guard_notes.append(_refresh_staleness_snapshot(project_dir))
    rows = _collect_stale_documents(project_dir)
    return rows, guard_notes


def _stage_options() -> list[str]:
    catalog = _ARTIFACT_RUNNER.load_artifact_catalog(_CATALOG_PATH)
    seen: set[str] = set()
    stages: list[str] = []
    for item in catalog:
        stage = str(item.get("stage", "")).strip()
        if stage and stage not in seen:
            seen.add(stage)
            stages.append(stage)
    return stages


def _requirement_options(project_dir: Path) -> list[str]:
    options: list[str] = []
    req_dir = _PATHS.requirements_dir(project_dir)
    if not req_dir.exists():
        return options
    for path in sorted(req_dir.iterdir()):
        if path.is_file() and path.suffix.lower() in {".md", ".txt"}:
            options.append(path.stem)
    return options


def _rerun_eligibility(
    *,
    project_dir: Path,
    action: str,
    requirement: str,
    stage: str,
) -> tuple[bool, str]:
    if action not in _ALLOWED_ACTIONS:
        return (False, f"Unsupported action: {action}")

    stale_rows, guard_notes = _stale_rows_with_freshness_guard(project_dir)
    if not stale_rows:
        refresh_note = f" ({guard_notes[0]})" if guard_notes else ""
        return (
            False,
            "No stale or needs-rerun documents found after freshness check. "
            "Rerun is blocked to keep execution conservative."
            + refresh_note,
        )

    requirement_names = set(_requirement_options(project_dir))
    if action == "rerun_requirement":
        if not requirement:
            return (False, "Requirement is required for rerun_requirement.")
        if requirement not in requirement_names:
            return (False, f"Unknown requirement: {requirement}")
        impacted = any(
            requirement.lower() in [str(name).lower() for name in row.get("impacted_requirements", [])]
            or str(row.get("file_path", "")).endswith(f"/{requirement}.md")
            for row in stale_rows
        )
        if not impacted:
            return (
                False,
                f"Requirement {requirement} is not in current stale impact scope after freshness check.",
            )
        return (True, ("Eligible." + (f" {guard_notes[0]}" if guard_notes else "")))

    if action == "rerun_from_stage":
        if not stage:
            return (False, "Stage is required for rerun_from_stage.")
        if stage not in _stage_options():
            return (False, f"Unknown stage: {stage}")
        if requirement:
            if requirement not in requirement_names:
                return (False, f"Unknown requirement: {requirement}")
            impacted = any(
                requirement.lower() in [str(name).lower() for name in row.get("impacted_requirements", [])]
                and stage in [str(name) for name in row.get("impacted_stages", [])]
                for row in stale_rows
            )
            if not impacted:
                return (
                    False,
                    f"Stage {stage} is not recommended for requirement {requirement} "
                    "after freshness check.",
                )
        else:
            impacted = any(stage in [str(name) for name in row.get("impacted_stages", [])] for row in stale_rows)
            if not impacted:
                return (
                    False,
                    f"Stage {stage} is not currently recommended after freshness check.",
                )
        return (True, ("Eligible." + (f" {guard_notes[0]}" if guard_notes else "")))

    # rerun_project
    return (True, ("Eligible." + (f" {guard_notes[0]}" if guard_notes else "")))


def _rerun_command(base_dir: Path, action: str, project: str, requirement: str, stage: str) -> list[str]:
    app_path = base_dir / "app.py"
    command: list[str] = [sys.executable, str(app_path), "--project", project, "--force"]
    if action == "rerun_requirement":
        command.extend(["--requirement", f"{requirement}.md"])
    elif action == "rerun_from_stage":
        command.extend(["--mode", "controlled", "--stage", stage])
        if requirement:
            command.extend(["--requirement", f"{requirement}.md"])
    return command


def _refresh_staleness_after_rerun(project_dir: Path) -> None:
    state = _STALENESS.load_state(project_dir)
    docs = state.get("documents", {})
    if not isinstance(docs, dict):
        return
    for relative in list(docs.keys()):
        _STALENESS.evaluate_document(project_dir, state, str(relative))
    _STALENESS.save_state(project_dir, state)


def get_actions_capabilities(base_dir: Path, project_name: str = "") -> dict[str, Any]:
    capabilities: list[dict[str, Any]] = [
        {
            "name": "confirmation_update",
            "enabled": True,
            "entrypoint": "/api/confirmations/update",
            "note": "Confirmation write actions are enabled.",
        },
        {
            "name": "docs_edit",
            "enabled": True,
            "entrypoint": "/api/doc-save",
            "note": "Only allowlisted docs are editable.",
        },
        {
            "name": "staleness_analysis",
            "enabled": True,
            "entrypoint": "/api/docs + /api/doc-preview",
            "note": "Computes stale state and rerun recommendations.",
        },
        {
            "name": "rerun_project",
            "enabled": True,
            "entrypoint": "/api/actions/execute",
            "note": "Controlled rerun for one project.",
        },
        {
            "name": "rerun_requirement",
            "enabled": True,
            "entrypoint": "/api/actions/execute",
            "note": "Controlled rerun for one requirement.",
        },
        {
            "name": "rerun_from_stage",
            "enabled": True,
            "entrypoint": "/api/actions/execute",
            "note": "Controlled rerun from one stage.",
        },
        {
            "name": "artifact_level_rerun",
            "enabled": False,
            "reason": "Not enabled in Phase 3B.",
        },
        {
            "name": "gate_override",
            "enabled": False,
            "reason": "Not exposed in Phase 3B UI.",
        },
    ]
    payload = {
        "mode": "phase-3b",
        "actions_enabled": True,
        "capabilities": capabilities,
    }
    if project_name.strip():
        payload["context"] = get_rerun_context(base_dir, project_name.strip())
    return payload


def get_rerun_context(base_dir: Path, project_name: str) -> dict[str, Any]:
    project_dir = _MAPPER.resolve_project_dir(base_dir, project_name)
    stale_rows, guard_notes = _stale_rows_with_freshness_guard(project_dir)
    requirements = _requirement_options(project_dir)
    stages = _stage_options()
    counts = _STALENESS.summary_counts(project_dir)
    recommended_requirements = sorted(
        {
            str(req).lower()
            for row in stale_rows
            for req in row.get("impacted_requirements", [])
            if str(req).strip()
        }
    )
    recommended_stages = sorted(
        {
            str(stage)
            for row in stale_rows
            for stage in row.get("impacted_stages", [])
            if str(stage).strip()
        }
    )
    return {
        "project": project_name,
        "stale_items_count": counts.get("stale_items_count", 0),
        "needs_rerun_items_count": counts.get("needs_rerun_items_count", 0),
        "stale_documents": stale_rows,
        "requirement_options": requirements,
        "stage_options": stages,
        "recommended_requirements": recommended_requirements,
        "recommended_stages": recommended_stages,
        "freshness_notes": guard_notes,
    }


def check_rerun_eligibility(base_dir: Path, payload: dict[str, Any]) -> dict[str, Any]:
    action = str(payload.get("action", "")).strip().lower()
    project = str(payload.get("project", "")).strip()
    requirement = _requirement_name(str(payload.get("requirement", "")))
    stage = str(payload.get("stage", "")).strip()

    if not project:
        raise ValueError("Missing project.")
    project_dir = _MAPPER.resolve_project_dir(base_dir, project)
    eligible, reason = _rerun_eligibility(
        project_dir=project_dir,
        action=action,
        requirement=requirement,
        stage=stage,
    )
    return {
        "project": project,
        "action": action,
        "requirement": requirement,
        "stage": stage,
        "eligible": eligible,
        "reason": reason,
    }


def execute_rerun_action(base_dir: Path, payload: dict[str, Any]) -> dict[str, Any]:
    eligibility = check_rerun_eligibility(base_dir, payload)
    if not eligibility.get("eligible", False):
        return {
            "executed": False,
            "eligible": False,
            "blocked_reason": eligibility.get("reason", "Action is blocked."),
            "eligibility": eligibility,
        }

    action = str(eligibility.get("action", ""))
    project = str(eligibility.get("project", ""))
    requirement = str(eligibility.get("requirement", ""))
    stage = str(eligibility.get("stage", ""))
    project_dir = _MAPPER.resolve_project_dir(base_dir, project)
    command = _rerun_command(base_dir, action, project, requirement, stage)

    try:
        completed = subprocess.run(
            command,
            cwd=base_dir,
            capture_output=True,
            text=True,
            timeout=_TIMEOUT_SECONDS,
            check=False,
        )
    except subprocess.TimeoutExpired as error:
        return {
            "executed": False,
            "eligible": True,
            "action": action,
            "project": project,
            "requirement": requirement,
            "stage": stage,
            "command": " ".join(command),
            "message": f"Rerun timed out after {_TIMEOUT_SECONDS} seconds.",
            "stdout_tail": (error.stdout or "").splitlines()[-20:],
            "stderr_tail": (error.stderr or "").splitlines()[-20:],
        }
    stdout_lines = [line for line in completed.stdout.splitlines() if line.strip()]
    stderr_lines = [line for line in completed.stderr.splitlines() if line.strip()]

    if completed.returncode == 0:
        _refresh_staleness_after_rerun(project_dir)
        context = get_rerun_context(base_dir, project)
        return {
            "executed": True,
            "eligible": True,
            "action": action,
            "project": project,
            "requirement": requirement,
            "stage": stage,
            "command": " ".join(command),
            "exit_code": completed.returncode,
            "message": "Rerun completed successfully.",
            "stdout_tail": stdout_lines[-20:],
            "stderr_tail": stderr_lines[-20:],
            "context": context,
        }

    return {
        "executed": False,
        "eligible": True,
        "action": action,
        "project": project,
        "requirement": requirement,
        "stage": stage,
        "command": " ".join(command),
        "exit_code": completed.returncode,
        "message": "Rerun failed. Review stderr/stdout output.",
        "stdout_tail": stdout_lines[-20:],
        "stderr_tail": stderr_lines[-20:],
    }
