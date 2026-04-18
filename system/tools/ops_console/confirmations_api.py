from __future__ import annotations

from pathlib import Path
import importlib.util
import sys
from typing import Any


def _load_module(module_name: str, file_path: Path):
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Could not load module: {file_path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


_MAPPER = _load_module(
    "state_mapper_for_ops_confirmations_api",
    Path(__file__).resolve().parent / "state_mapper.py",
)
_CONFIRMATION_MANAGER = _load_module(
    "confirmation_manager_for_ops_confirmations_api",
    Path(__file__).resolve().parents[1] / "review" / "confirmation_manager.py",
)


def _map_item(item: dict[str, Any], project_name: str) -> dict[str, Any]:
    return {
        "confirmation_id": item.get("id", ""),
        "project": item.get("project", project_name),
        "requirement": item.get("requirement", "-"),
        "artifact": item.get("artifact", "-"),
        "type": item.get("type", "-"),
        "title": item.get("title", ""),
        "description": item.get("description", ""),
        "status": item.get("status", "pending"),
        "owner": item.get("owner", "-"),
        "impact": item.get("impact", []),
        "blocked_reason": item.get("blocked_reason", ""),
        "suggested_action": item.get("suggested_action", ""),
        "recommendation_source": item.get("recommendation_source", "research-agent"),
        "recommendation_label": item.get("recommendation_label", "Research Recommendation"),
        "decision_authority": item.get("decision_authority", "human-required"),
        "data_state": item.get("data_state", "recommended"),
        "linked_files": item.get("linked_files", []),
        "decision": item.get("decision", ""),
        "decision_note": item.get("decision_note", ""),
        "confirmed_by": item.get("confirmed_by", ""),
        "confirmed_at": item.get("confirmed_at", ""),
        "final_decision_by": item.get("final_decision_by", ""),
        "propagation_targets": item.get("effective_rule_update_target", []),
    }


def get_confirmations(
    base_dir: Path,
    project_name: str,
    status_filter: str = "all",
    type_filter: str = "all",
    owner_filter: str = "all",
    search: str = "",
) -> dict[str, Any]:
    project_dir = _MAPPER.resolve_project_dir(base_dir, project_name)
    _CONFIRMATION_MANAGER.sync_confirmations_from_status(project_dir)
    all_items = _CONFIRMATION_MANAGER.project_items(
        project_dir,
        status_filter=status_filter,
        search=search,
    )
    items = list(all_items)
    if type_filter.strip().lower() != "all":
        wanted = type_filter.strip().lower()
        items = [item for item in items if str(item.get("type", "")).strip().lower() == wanted]
    if owner_filter.strip().lower() != "all":
        wanted = owner_filter.strip().lower()
        items = [item for item in items if str(item.get("owner", "")).strip().lower() == wanted]
    mapped = [_map_item(item, project_name) for item in items]
    type_options = sorted(
        {
            str(item.get("type", "")).strip()
            for item in all_items
            if str(item.get("type", "")).strip()
        }
    )
    owner_options = sorted(
        {
            str(item.get("owner", "")).strip()
            for item in all_items
            if str(item.get("owner", "")).strip()
        }
    )
    return {
        "project": project_name,
        "confirmations": mapped,
        "filters": {
            "type_options": type_options,
            "owner_options": owner_options,
        },
    }


def refresh_confirmations(base_dir: Path, project_name: str = "") -> dict[str, Any]:
    name = project_name.strip()
    if name:
        project_dir = _MAPPER.resolve_project_dir(base_dir, name)
        result = _CONFIRMATION_MANAGER.sync_confirmations_from_status(project_dir)
        return {"project": name, "result": result}

    refreshed = []
    for project_dir in _CONFIRMATION_MANAGER.list_projects(base_dir):
        result = _CONFIRMATION_MANAGER.sync_confirmations_from_status(project_dir)
        refreshed.append({"project": project_dir.name, **result})
    return {"refreshed": refreshed}


def _find_item(project_dir: Path, item_id: str) -> dict[str, Any]:
    for item in _CONFIRMATION_MANAGER.load_items(project_dir):
        if str(item.get("id", "")).strip() == item_id.strip():
            return item
    raise ValueError(f"Confirmation item not found: {item_id}")


def _action_status(action: str) -> str | None:
    value = action.strip().lower()
    if value == "confirm":
        return "confirmed"
    if value == "reject":
        return "rejected"
    if value == "needs_more_info":
        return "needs-more-info"
    if value == "mark_resolved":
        return "resolved"
    return None


def update_confirmation(base_dir: Path, payload: dict[str, Any]) -> dict[str, Any]:
    project_name = str(payload.get("project", "")).strip()
    item_id = str(payload.get("item_id", "")).strip()
    if not project_name:
        raise ValueError("Missing project.")
    if not item_id:
        raise ValueError("Missing item_id.")

    project_dir = _MAPPER.resolve_project_dir(base_dir, project_name)
    current = _find_item(project_dir, item_id)

    action = str(payload.get("action", "")).strip().lower()
    status = str(payload.get("status", "")).strip().lower()
    if not status:
        mapped = _action_status(action)
        status = mapped if mapped else str(current.get("status", "pending")).strip().lower()

    decision = str(payload.get("decision", "")).strip()
    decision_note = str(payload.get("decision_note", "")).strip()
    confirmed_by = str(payload.get("confirmed_by", "")).strip()
    confirmed_at = str(payload.get("confirmed_at", "")).strip()

    # Action-specific partial updates keep other fields stable.
    if action == "add_decision_note" and not decision_note:
        decision_note = str(current.get("decision_note", "")).strip()
    if action == "set_confirmed_by" and not confirmed_by:
        confirmed_by = str(current.get("confirmed_by", "")).strip()
    if action == "set_confirmed_at" and not confirmed_at:
        confirmed_at = str(current.get("confirmed_at", "")).strip()
    if action and action not in {
        "confirm",
        "reject",
        "needs_more_info",
        "mark_resolved",
        "add_decision_note",
        "set_confirmed_by",
        "set_confirmed_at",
        "save",
    }:
        raise ValueError(f"Unsupported confirmation action: {action}")

    updated = _CONFIRMATION_MANAGER.apply_decision(
        project_dir=project_dir,
        item_id=item_id,
        status=status or str(current.get("status", "pending")),
        decision=decision,
        decision_note=decision_note,
        confirmed_by=confirmed_by,
        confirmed_at=confirmed_at,
    )
    return {"updated": _map_item(updated, project_name)}


def get_confirmation_projects(base_dir: Path) -> dict[str, Any]:
    projects = []
    for project_dir in _CONFIRMATION_MANAGER.list_projects(base_dir):
        _CONFIRMATION_MANAGER.sync_confirmations_from_status(project_dir)
        projects.append(_CONFIRMATION_MANAGER.project_summary(project_dir))
    return {"projects": projects}
