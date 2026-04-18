from __future__ import annotations

from datetime import datetime
from pathlib import Path
import importlib.util
import sys
from typing import Any

try:
    import yaml
except ImportError:
    yaml = None


def _load_module(module_name: str, file_path: Path):
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Could not load module: {file_path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


_PATHS = _load_module(
    "project_paths_for_ops_console_state_mapper",
    Path(__file__).resolve().parents[1] / "project" / "project_paths.py",
)
_STALENESS = _load_module(
    "staleness_engine_for_ops_state_mapper",
    Path(__file__).resolve().parent / "staleness_engine.py",
)
_SEMANTICS = _load_module(
    "semantic_mapper_for_ops_state_mapper",
    Path(__file__).resolve().parents[1] / "project" / "semantic_mapper.py",
)
_SUMMARY = _load_module(
    "summary_reader_for_ops_state_mapper",
    Path(__file__).resolve().parents[1] / "project" / "summary_reader.py",
)


def _read_text(path: Path) -> str:
    return _SUMMARY.read_text(path)


def _read_yaml(path: Path) -> dict[str, Any]:
    if yaml is None or not path.exists():
        return {}
    raw = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    return raw if isinstance(raw, dict) else {}


def _is_within(base: Path, target: Path) -> bool:
    try:
        target.resolve().relative_to(base.resolve())
        return True
    except ValueError:
        return False


def _line_value(lines: list[str], prefixes: list[str]) -> str:
    return _SUMMARY.line_value(lines, prefixes)


def _collect_blockers(lines: list[str]) -> list[str]:
    items = _SUMMARY.collect_section(lines, "## Current Blockers")
    return [value for value in items if value.lower() not in {"blocker 1", "blocker 2", "no blockers listed"}]


def _parse_requirements(lines: list[str]) -> list[dict[str, str]]:
    return _SUMMARY.parse_requirements_table(lines)


def _gather_artifact_rows(project_dir: Path) -> list[dict[str, str]]:
    return _SUMMARY.gather_artifact_rows(project_dir, _PATHS)


def _gather_gate_rows(project_dir: Path) -> list[dict[str, str]]:
    return _SUMMARY.gather_gate_rows(project_dir, _PATHS)


def discover_projects(base_dir: Path) -> list[Path]:
    projects_dir = base_dir / "projects"
    results: list[Path] = []
    for entry in sorted(projects_dir.iterdir()):
        if not entry.is_dir():
            continue
        if entry.name.startswith(".") or entry.name == "project-template":
            continue
        if (entry / "project-config.yaml").exists():
            results.append(entry)
    return results


def project_summary_model(project_dir: Path) -> dict[str, Any]:
    status_lines = _read_text(_PATHS.status_path(project_dir)).splitlines()
    requirements = _parse_requirements(status_lines)
    blockers = _collect_blockers(status_lines)
    phase = _line_value(status_lines, ["- Project Phase:", "- Current Stage:"]) or "Draft"
    owner = _line_value(status_lines, ["- Project Owner:", "- Owner:"]) or "BA Team"
    last_update = _line_value(status_lines, ["- Last Updated:"]) or "-"
    project_status, readiness = _SEMANTICS.project_status_and_readiness(
        requirement_statuses=[item["current_status"] for item in requirements],
        blockers=blockers,
        project_phase=phase,
    )
    staleness = _STALENESS.summary_counts(project_dir)

    return {
        "project_name": _line_value(status_lines, ["- Project Name:"]) or project_dir.name,
        "project_phase": phase,
        "project_owner": owner,
        "project_status": project_status,
        "project_readiness": readiness,
        "last_update": last_update,
        "stale_items_count": staleness.get("stale_items_count", 0),
        "needs_rerun_items_count": staleness.get("needs_rerun_items_count", 0),
    }


def execution_snapshot_model(project_dir: Path) -> dict[str, Any]:
    artifact_rows = _gather_artifact_rows(project_dir)
    gate_rows = _gather_gate_rows(project_dir)
    status_lines = _read_text(_PATHS.status_path(project_dir)).splitlines()
    blockers = _collect_blockers(status_lines)
    confirmation_items = confirmation_models(project_dir)
    confirmation_blockers = _SEMANTICS.parse_confirmation_blockers(confirmation_items)
    return _SEMANTICS.execution_snapshot(
        artifact_rows=artifact_rows,
        gate_rows=gate_rows,
        project_blockers=blockers,
        confirmation_blockers=confirmation_blockers,
    )


def requirement_processing_models(project_dir: Path) -> list[dict[str, Any]]:
    status_lines = _read_text(_PATHS.status_path(project_dir)).splitlines()
    req_rows = _parse_requirements(status_lines)
    project_status = project_summary_model(project_dir).get("project_status", "Active")
    state = _read_yaml(_PATHS.processing_state_path(project_dir))
    state_requirements = state.get("requirements", {}) if isinstance(state, dict) else {}
    if not isinstance(state_requirements, dict):
        state_requirements = {}
    rows = _SEMANTICS.requirement_processing_rows(
        requirement_rows=req_rows,
        processing_state_requirements=state_requirements,
        project_status=str(project_status),
    )
    return [
        {
            "requirement_name": row["requirement_name"],
            "processing_status": row["processing_status"],
            "display_status": row["display_status"],
            "input_change_state": row["input_change_state"],
            "last_processed_at": row["last_processed_at"],
            "rerun_needed": row["rerun_needed"],
        }
        for row in rows
    ]


def confirmation_models(project_dir: Path) -> list[dict[str, Any]]:
    items = _SUMMARY.load_confirmation_items(project_dir, _PATHS, yaml)
    results: list[dict[str, Any]] = []
    for item in items:
        if not isinstance(item, dict):
            continue
        results.append(
            {
                "confirmation_id": item.get("id", ""),
                "project": item.get("project", project_dir.name),
                "requirement": item.get("requirement", "-"),
                "artifact": item.get("artifact", "-"),
                "type": item.get("type", "-"),
                "title": item.get("title", ""),
                "description": item.get("description", ""),
                "status": item.get("status", "pending"),
                "owner": item.get("owner", "-"),
                "impact": item.get("impact", []),
                "decision": item.get("decision", ""),
                "decision_note": item.get("decision_note", ""),
                "confirmed_by": item.get("confirmed_by", ""),
                "confirmed_at": item.get("confirmed_at", ""),
                "propagation_targets": item.get("effective_rule_update_target", []),
            }
        )
    return sorted(results, key=lambda item: str(item.get("confirmation_id", "")))


def task_models(project_dir: Path) -> list[dict[str, Any]]:
    project_summary = project_summary_model(project_dir)
    artifact_rows = _gather_artifact_rows(project_dir)
    confirmations = confirmation_models(project_dir)
    blocker_lookup = {str(item.get("description", "")).strip(): str(item.get("confirmation_id", "")) for item in confirmations}
    results: list[dict[str, Any]] = []
    for row in artifact_rows:
        status_value = str(row.get("status", "Not Started"))
        priority = "Medium"
        if status_value in {"Blocked", "Rework Needed"}:
            priority = "High"
        elif status_value == "In Review":
            priority = "Medium"
        else:
            priority = "Low"
        note = str(row.get("notes", "")).strip()
        linked_blocker_id = blocker_lookup.get(note, "")
        results.append(
            {
                "task_id": f"TSK-{project_dir.name}-{row.get('requirement_name', '-')}-{row.get('artifact', '-')}",
                "project": project_dir.name,
                "requirement": row.get("requirement_name", "-"),
                "stage": row.get("stage", "-"),
                "artifact": row.get("artifact", "-"),
                "title": f"{row.get('artifact', '-')} execution",
                "agent_owner": _SEMANTICS.normalize_execution_owner(str(row.get("owner", ""))),
                "human_owner": project_summary.get("project_owner", "BA Team"),
                "status": status_value,
                "priority": priority,
                "next_action": note or "Review artifact status and proceed based on gate result.",
                "linked_blocker_id": linked_blocker_id,
                "updated_at": project_summary.get("last_update", "-"),
            }
        )
    return results


def _file_doc_type(path: Path) -> str:
    name = path.name.lower()
    if name.endswith(".html"):
        return "html"
    if "frs" in name:
        return "frs"
    if "brd" in name:
        return "brd"
    if "user-story" in name:
        return "user-story"
    if "acceptance-criteria" in name:
        return "acceptance-criteria"
    if "feature-list" in name:
        return "feature-list"
    if "traceability" in name:
        return "traceability"
    if "review" in name:
        return "review"
    return "markdown"


def document_state_models(project_dir: Path) -> list[dict[str, Any]]:
    docs: list[dict[str, Any]] = []
    candidates = [
        _PATHS.status_path(project_dir),
        _PATHS.decision_log_path(project_dir),
        _PATHS.task_tracker_path(project_dir),
        _PATHS.change_log_path(project_dir),
        _PATHS.dependency_map_path(project_dir),
        _PATHS.project_flow_path(project_dir),
        _PATHS.traceability_summary_path(project_dir),
        _PATHS.pending_confirmations_yaml_path(project_dir),
        _PATHS.pending_confirmations_markdown_path(project_dir),
        _PATHS.confirmations_decisions_log_path(project_dir),
    ]

    generated = _PATHS.generated_root(project_dir)
    if generated.exists():
        for req_dir in sorted(path for path in generated.iterdir() if path.is_dir()):
            for file_path in sorted(req_dir.iterdir()):
                if file_path.is_file() and file_path.suffix.lower() in {".md", ".html", ".yaml", ".yml"}:
                    candidates.append(file_path)

    seen: set[str] = set()
    for path in candidates:
        if not path.exists():
            continue
        relative = str(path.relative_to(project_dir))
        if relative in seen:
            continue
        seen.add(relative)
        stat = path.stat()
        docs.append(
            {
                "file_path": relative,
                "doc_type": _file_doc_type(path),
                "editable": False,
                "last_modified": datetime.fromtimestamp(stat.st_mtime).strftime("%Y-%m-%d %H:%M:%S"),
                "manual_override": False,
                "stale_state": "fresh",
                "rerun_recommendation": "none",
            }
        )
    return docs


def doc_preview_metadata(project_dir: Path, relative_path: str) -> dict[str, Any]:
    cleaned = relative_path.strip().lstrip("/")
    if cleaned.startswith(".."):
        raise ValueError("Invalid relative path.")
    target = (project_dir / cleaned).resolve()
    if not _is_within(project_dir, target):
        raise ValueError("Invalid relative path.")
    if not target.exists() or not target.is_file():
        raise ValueError("Document not found.")
    allowed_suffix = {".md", ".html", ".yaml", ".yml", ".txt"}
    if target.suffix.lower() not in allowed_suffix:
        raise ValueError("Unsupported file type.")
    text = _read_text(target)
    first_lines = "\n".join(text.splitlines()[:8])
    return {
        "file_path": cleaned,
        "doc_type": _file_doc_type(target),
        "size_bytes": target.stat().st_size,
        "line_count": len(text.splitlines()),
        "preview": first_lines,
    }


def resolve_project_dir(base_dir: Path, project_name: str) -> Path:
    target = (base_dir / "projects" / project_name).resolve()
    projects_root = (base_dir / "projects").resolve()
    if not _is_within(projects_root, target):
        raise ValueError("Invalid project name.")
    if not target.exists() or not target.is_dir() or not (target / "project-config.yaml").exists():
        raise ValueError(f"Unknown project: {project_name}")
    return target


def project_bundle(project_dir: Path) -> dict[str, Any]:
    summary = project_summary_model(project_dir)
    execution = execution_snapshot_model(project_dir)
    requirements = requirement_processing_models(project_dir)
    tasks = task_models(project_dir)
    confirmations = confirmation_models(project_dir)
    docs = document_state_models(project_dir)
    return {
        "project_summary": summary,
        "execution_snapshot": execution,
        "requirements": requirements,
        "tasks": tasks,
        "confirmations": confirmations,
        "documents": docs,
    }


def projects_bundle(base_dir: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for project_dir in discover_projects(base_dir):
        bundle = project_bundle(project_dir)
        rows.append(
            {
                "project_name": project_dir.name,
                "project_summary": bundle["project_summary"],
                "execution_snapshot": bundle["execution_snapshot"],
                "requirement_count": len(bundle["requirements"]),
                "pending_confirmations": sum(
                    1
                    for item in bundle["confirmations"]
                    if str(item.get("status", "")).strip().lower() == "pending"
                ),
            }
        )
    return rows


def overview_metrics(base_dir: Path) -> dict[str, Any]:
    projects = projects_bundle(base_dir)
    total = len(projects)
    blocked = sum(
        1
        for item in projects
        if str(item.get("project_summary", {}).get("project_status", "")).lower() == "blocked"
    )
    done = sum(
        1
        for item in projects
        if str(item.get("project_summary", {}).get("project_status", "")).lower() == "done"
    )
    active = max(total - blocked - done, 0)
    return {
        "total_projects": total,
        "active_projects": active,
        "blocked_projects": blocked,
        "done_projects": done,
        "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }
