from __future__ import annotations

from datetime import datetime
import importlib.util
from pathlib import Path
import re
import sys
from typing import Any

try:
    import yaml
except ImportError as error:  # pragma: no cover
    raise ImportError(
        "PyYAML is required for confirmation manager. Install with: pip install -r requirements.txt"
    ) from error


ALLOWED_STATUSES = {"pending", "confirmed", "rejected", "needs-more-info", "resolved"}
OPEN_STATUSES = {"pending", "needs-more-info"}
RESOLVED_STATUSES = {"confirmed", "rejected", "resolved"}
ALLOWED_DATA_STATES = {"recommended", "confirmed-data"}


def _load_module(module_name: str, file_path: Path):
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Could not load module: {file_path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


_PATHS = _load_module(
    "project_paths_for_confirmation_manager",
    Path(__file__).resolve().parents[1] / "project" / "project_paths.py",
)


def _now_iso() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def _today() -> str:
    return datetime.now().strftime("%Y-%m-%d")


def _read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8")


def _write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def _default_payload() -> dict[str, Any]:
    return {"items": []}


def _normalize_status(status: str) -> str:
    value = status.strip().lower()
    if value not in ALLOWED_STATUSES:
        raise ValueError(
            f"Invalid confirmation status '{status}'. Allowed: {', '.join(sorted(ALLOWED_STATUSES))}."
        )
    return value


def _normalize_data_state(value: str) -> str:
    state = str(value or "").strip().lower()
    if state in ALLOWED_DATA_STATES:
        return state
    return "recommended"


def _ensure_research_metadata(item: dict[str, Any]) -> dict[str, Any]:
    """
    Keep researcher recommendation metadata explicit:
    - researcher can recommend
    - final data state changes only after human confirmation
    """
    current = dict(item)
    current["recommendation_source"] = str(current.get("recommendation_source", "research-agent")).strip() or "research-agent"
    current["recommendation_label"] = str(current.get("recommendation_label", "Research Recommendation")).strip() or "Research Recommendation"
    current["decision_authority"] = str(current.get("decision_authority", "human-required")).strip() or "human-required"
    current["data_state"] = _normalize_data_state(str(current.get("data_state", "recommended")))
    current["final_decision_by"] = str(current.get("final_decision_by", "")).strip()
    return current


def _is_placeholder_blocker(value: str) -> bool:
    lowered = value.strip().lower()
    return lowered in {"blocker 1", "blocker 2", "no blockers listed"}


def _line_value(lines: list[str], prefixes: list[str]) -> str:
    for line in lines:
        for prefix in prefixes:
            if line.strip().startswith(prefix):
                return line.split(":", 1)[1].strip()
    return ""


def _collect_section_bullets(lines: list[str], header: str) -> list[str]:
    items: list[str] = []
    in_section = False
    for line in lines:
        if line.strip() == header:
            in_section = True
            continue
        if in_section and line.startswith("## "):
            break
        if in_section and line.strip().startswith("- "):
            value = line.strip()[2:].strip()
            if value:
                items.append(value)
    return items


def _parse_requirement_table(lines: list[str]) -> dict[str, str]:
    rows: dict[str, str] = {}
    in_table = False
    for line in lines:
        if line.strip() == "| Requirement | Current Status | BA | UXUI | FE | Reviewer | Notes |":
            in_table = True
            continue
        if in_table and not line.strip().startswith("|"):
            break
        if in_table and line.strip().startswith("|"):
            cols = [col.strip() for col in line.strip("|").split("|")]
            if len(cols) < 2:
                continue
            if cols[0] == "Requirement" or set(cols[0]) == {"-"}:
                continue
            rows[cols[0]] = cols[1]
    return rows


def _find_primary_blocked_requirement(requirements: dict[str, str]) -> str:
    for name, status in requirements.items():
        if status.strip().lower() == "blocked":
            return name
    for name, status in requirements.items():
        if status.strip().lower() in {"in progress", "done"}:
            return name
    return ""


def _load_pending_yaml(path: Path) -> dict[str, Any]:
    if not path.exists():
        return _default_payload()
    raw = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    if not isinstance(raw, dict):
        return _default_payload()
    items = raw.get("items", [])
    if not isinstance(items, list):
        raw["items"] = []
    return raw


def _save_pending_yaml(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(yaml.safe_dump(payload, sort_keys=False, allow_unicode=False), encoding="utf-8")


def _extract_numeric_id(value: str) -> int:
    match = re.match(r"^CFM-(\d+)$", value.strip())
    if not match:
        return 0
    return int(match.group(1))


def _next_confirmation_id(items: list[dict[str, Any]]) -> str:
    current = 0
    for item in items:
        current = max(current, _extract_numeric_id(str(item.get("id", ""))))
    return f"CFM-{current + 1:03d}"


def _append_decision_entry(path: Path, item: dict[str, Any], action: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    existing = _read_text(path).rstrip()
    if not existing:
        existing = "# Confirmation Decisions Log\n\n"
    block = "\n".join(
        [
            f"## {item.get('id', '-')}",
            f"- Date: {_now_iso()}",
            f"- Action: {action}",
            f"- Project: {item.get('project', '')}",
            f"- Requirement: {item.get('requirement', '-')}",
            f"- Artifact: {item.get('artifact', '-')}",
            f"- Status: {item.get('status', '')}",
            f"- Decision: {item.get('decision', '') or '-'}",
            f"- Decision Note: {item.get('decision_note', '') or '-'}",
            f"- Confirmed By: {item.get('confirmed_by', '') or '-'}",
            "",
        ]
    )
    _write_text(path, existing + "\n" + block)


def _append_project_decision_log(project_dir: Path, item: dict[str, Any], action: str) -> None:
    path = _PATHS.decision_log_path(project_dir)
    existing = _read_text(path).rstrip()
    if not existing:
        existing = "# Decision Log\n\n"
    block = "\n".join(
        [
            f"## Confirmation {item.get('id', '-')}",
            f"- Date: {_now_iso()}",
            f"- Context: {item.get('title', '')}",
            f"- Decision: {item.get('decision', '') or action}",
            f"- Reason: {item.get('decision_note', '') or item.get('description', '')}",
            f"- Impact: Requirement {item.get('requirement', '-')}, Artifact {item.get('artifact', '-')}",
            "",
        ]
    )
    _write_text(path, existing + "\n" + block)


def _append_business_rule_update(project_dir: Path, item: dict[str, Any]) -> None:
    targets = item.get("effective_rule_update_target", [])
    if not isinstance(targets, list):
        return
    if item.get("status") not in {"confirmed", "resolved"}:
        return

    decision = str(item.get("decision", "")).strip()
    if not decision:
        return

    for target in targets:
        relative = str(target).strip()
        if not relative:
            continue
        target_path = project_dir / relative
        if not target_path.exists():
            continue
        entry = f"- [{item.get('id', '-')}] {decision}"
        if item.get("decision_note"):
            entry += f" ({item.get('decision_note')})"

        content = _read_text(target_path)
        if entry in content:
            continue
        if "## Confirmed Decisions" not in content:
            content = content.rstrip() + "\n\n## Confirmed Decisions\n"
        content = content.rstrip() + "\n" + entry + "\n"
        _write_text(target_path, content)


def _remove_resolved_blocker_from_status(project_dir: Path, blocked_reason: str) -> None:
    if not blocked_reason.strip():
        return
    path = _PATHS.status_path(project_dir)
    if not path.exists():
        return
    lines = path.read_text(encoding="utf-8").splitlines()

    start = None
    end = None
    for index, line in enumerate(lines):
        if line.strip() == "## Current Blockers":
            start = index
            continue
        if start is not None and line.startswith("## "):
            end = index
            break
    if start is None:
        return
    if end is None:
        end = len(lines)

    section_lines = lines[start + 1 : end]
    bullets = [line for line in section_lines if line.strip().startswith("- ")]
    remaining = []
    removed = False
    for bullet in bullets:
        text = bullet.strip()[2:].strip()
        if text == blocked_reason.strip():
            removed = True
            continue
        remaining.append(text)

    if not removed:
        return

    replacement = [""]
    if remaining:
        replacement.extend([f"- {item}" for item in remaining])
    else:
        replacement.append("- No blockers listed")

    new_lines = lines[: start + 1] + replacement + lines[end:]
    for index, line in enumerate(new_lines):
        if line.startswith("- Last Updated:"):
            new_lines[index] = f"- Last Updated: {_today()}"
            break
    _write_text(path, "\n".join(new_lines).rstrip() + "\n")


def _build_pending_markdown(project_dir: Path, payload: dict[str, Any]) -> str:
    items_raw = payload.get("items", [])
    items: list[dict[str, Any]] = [item for item in items_raw if isinstance(item, dict)]
    items = sorted(items, key=lambda item: str(item.get("id", "")))

    groups: dict[str, list[dict[str, Any]]] = {status: [] for status in ALLOWED_STATUSES}
    for item in items:
        status = str(item.get("status", "pending")).strip().lower()
        if status not in groups:
            status = "pending"
        groups[status].append(item)

    lines = [
        "# Pending Confirmations",
        "",
        f"- Project: {project_dir.name}",
        f"- Last Updated: {_now_iso()}",
        "",
        "## Summary",
        f"- Pending: {len(groups['pending'])}",
        f"- Needs More Info: {len(groups['needs-more-info'])}",
        f"- Confirmed: {len(groups['confirmed'])}",
        f"- Rejected: {len(groups['rejected'])}",
        f"- Resolved: {len(groups['resolved'])}",
        "",
    ]

    for status in ["pending", "needs-more-info", "confirmed", "rejected", "resolved"]:
        heading = status.replace("-", " ").title()
        lines.append(f"## {heading}")
        lines.append("")
        if not groups[status]:
            lines.append("- No items.")
            lines.append("")
            continue
        for item in groups[status]:
            data_state = _normalize_data_state(str(item.get("data_state", "recommended")))
            state_label = "Confirmed Data" if data_state == "confirmed-data" else "Recommended Data"
            lines.extend(
                [
                    f"### {item.get('id', '-')}: {item.get('title', '')}",
                    f"- Requirement: {item.get('requirement', '-')}",
                    f"- Artifact: {item.get('artifact', '-')}",
                    f"- Type: {item.get('type', '-')}",
                    f"- Owner: {item.get('owner', '-')}",
                    f"- Status: {item.get('status', '-')}",
                    f"- Description: {item.get('description', '-')}",
                    f"- Blocked Reason: {item.get('blocked_reason', '-')}",
                    f"- Suggested Action: {item.get('suggested_action', '-')}",
                    f"- Recommendation Source: {item.get('recommendation_source', 'research-agent')}",
                    f"- Recommendation Label: {item.get('recommendation_label', 'Research Recommendation')}",
                    f"- Decision Authority: {item.get('decision_authority', 'human-required')}",
                    f"- Data State: {state_label}",
                    f"- Decision: {item.get('decision', '') or '-'}",
                    f"- Decision Note: {item.get('decision_note', '') or '-'}",
                    f"- Confirmed By: {item.get('confirmed_by', '') or '-'}",
                    f"- Confirmed At: {item.get('confirmed_at', '') or '-'}",
                    f"- Final Decision By: {item.get('final_decision_by', '') or '-'}",
                    "",
                ]
            )

    lines.extend(
        [
            "<!-- TODO: Add direct links to linked_files when the review UI can map local paths safely. -->",
            "",
        ]
    )
    return "\n".join(lines)


def ensure_confirmation_workspace(project_dir: Path) -> dict[str, Path]:
    base = _PATHS.confirmations_dir(project_dir)
    base.mkdir(parents=True, exist_ok=True)
    yaml_path = _PATHS.pending_confirmations_yaml_path(project_dir)
    md_path = _PATHS.pending_confirmations_markdown_path(project_dir)
    decisions_path = _PATHS.confirmations_decisions_log_path(project_dir)

    if not yaml_path.exists():
        _save_pending_yaml(yaml_path, _default_payload())
    if not decisions_path.exists():
        _write_text(decisions_path, "# Confirmation Decisions Log\n\n")
    if not md_path.exists():
        payload = _load_pending_yaml(yaml_path)
        _write_text(md_path, _build_pending_markdown(project_dir, payload))
    return {"yaml": yaml_path, "markdown": md_path, "decisions_log": decisions_path}


def load_items(project_dir: Path) -> list[dict[str, Any]]:
    paths = ensure_confirmation_workspace(project_dir)
    payload = _load_pending_yaml(paths["yaml"])
    items = payload.get("items", [])
    if not isinstance(items, list):
        return []
    return [_ensure_research_metadata(item) for item in items if isinstance(item, dict)]


def sync_confirmations_from_status(project_dir: Path) -> dict[str, int]:
    paths = ensure_confirmation_workspace(project_dir)
    payload = _load_pending_yaml(paths["yaml"])
    items_raw = payload.get("items", [])
    items: list[dict[str, Any]] = [_ensure_research_metadata(item) for item in items_raw if isinstance(item, dict)]

    status_lines = _read_text(_PATHS.status_path(project_dir)).splitlines()
    project_name = _line_value(status_lines, ["- Project Name:"]) or project_dir.name
    project_owner = _line_value(status_lines, ["- Project Owner:", "- Owner:"]) or "BA Team"
    blockers = [item for item in _collect_section_bullets(status_lines, "## Current Blockers") if not _is_placeholder_blocker(item)]
    actions = _collect_section_bullets(status_lines, "## Next Actions")
    suggested_action = actions[0] if actions else "Confirm business decision and update affected artifacts."
    requirements = _parse_requirement_table(status_lines)
    primary_requirement = _find_primary_blocked_requirement(requirements)

    created = 0
    for blocker in blockers:
        # Keep one stable confirmation record per blocker text.
        # Do not auto-create duplicates if the blocker was already captured previously,
        # even when it is currently confirmed/rejected/resolved.
        found = next(
            (
                item
                for item in items
                if str(item.get("blocked_reason", "")).strip() == blocker.strip()
            ),
            None,
        )
        if found:
            continue

        new_item = {
            "id": _next_confirmation_id(items),
            "project": project_name,
            "requirement": primary_requirement or "-",
            "artifact": "frs",
            "type": "policy",
            "title": blocker,
            "description": blocker,
            "status": "pending",
            "owner": project_owner,
            "impact": ["BA", "UXUI", "FE"],
            "gate_impact": True,
            "blocked_reason": blocker,
            "suggested_action": suggested_action,
            "recommendation_source": "research-agent",
            "recommendation_label": "Research Recommendation",
            "decision_authority": "human-required",
            "data_state": "recommended",
            "decision": "",
            "decision_note": "",
            "confirmed_by": "",
            "confirmed_at": "",
            "final_decision_by": "",
            "effective_rule_update_target": ["04-knowledge/business-rules.md"],
            "linked_files": [
                "01-input/requirements/",
                "_ops/decision-log.md",
            ],
        }
        items.append(new_item)
        created += 1

    payload["items"] = sorted(items, key=lambda item: str(item.get("id", "")))
    _save_pending_yaml(paths["yaml"], payload)
    _write_text(paths["markdown"], _build_pending_markdown(project_dir, payload))
    return {"total": len(payload["items"]), "created": created}


def apply_decision(
    project_dir: Path,
    item_id: str,
    status: str,
    decision: str = "",
    decision_note: str = "",
    confirmed_by: str = "",
    confirmed_at: str = "",
) -> dict[str, Any]:
    normalized_status = _normalize_status(status)
    paths = ensure_confirmation_workspace(project_dir)
    payload = _load_pending_yaml(paths["yaml"])
    items = payload.get("items", [])
    if not isinstance(items, list):
        raise ValueError("Invalid pending-confirmations.yaml structure.")

    target: dict[str, Any] | None = None
    target_index = -1
    for index, item in enumerate(items):
        if isinstance(item, dict) and str(item.get("id", "")).strip() == item_id.strip():
            target = item
            target_index = index
            break
    if target is None:
        raise ValueError(f"Confirmation item not found: {item_id}")

    previous_status = str(target.get("status", "pending")).strip().lower()
    target["status"] = normalized_status
    if decision:
        target["decision"] = decision.strip()
    if decision_note:
        target["decision_note"] = decision_note.strip()
    if confirmed_by:
        target["confirmed_by"] = confirmed_by.strip()
    if confirmed_at:
        target["confirmed_at"] = confirmed_at.strip()
    elif normalized_status in RESOLVED_STATUSES and not str(target.get("confirmed_at", "")).strip():
        target["confirmed_at"] = _now_iso()

    if normalized_status in {"confirmed", "resolved"}:
        target["data_state"] = "confirmed-data"
        if confirmed_by:
            target["final_decision_by"] = confirmed_by.strip()
        elif not str(target.get("final_decision_by", "")).strip():
            target["final_decision_by"] = "human-review"
    else:
        target["data_state"] = "recommended"

    target = _ensure_research_metadata(target)
    if target_index >= 0:
        items[target_index] = target

    payload["items"] = sorted(
        [item for item in items if isinstance(item, dict)],
        key=lambda item: str(item.get("id", "")),
    )
    _save_pending_yaml(paths["yaml"], payload)
    _write_text(paths["markdown"], _build_pending_markdown(project_dir, payload))

    action = f"{previous_status} -> {normalized_status}"
    _append_decision_entry(paths["decisions_log"], target, action=action)
    _append_project_decision_log(project_dir, target, action=action)

    if normalized_status in {"confirmed", "resolved"}:
        _remove_resolved_blocker_from_status(project_dir, str(target.get("blocked_reason", "")))
        _append_business_rule_update(project_dir, target)

    return target


def list_projects(base_dir: Path) -> list[Path]:
    projects_dir = base_dir / "projects"
    result: list[Path] = []
    for entry in sorted(projects_dir.iterdir()):
        if not entry.is_dir():
            continue
        if entry.name.startswith(".") or entry.name == "project-template":
            continue
        if (entry / "project-config.yaml").exists():
            result.append(entry)
    return result


def project_summary(project_dir: Path) -> dict[str, Any]:
    items = load_items(project_dir)
    counts = {key: 0 for key in ALLOWED_STATUSES}
    for item in items:
        status = str(item.get("status", "pending")).strip().lower()
        if status in counts:
            counts[status] += 1
    return {
        "project": project_dir.name,
        "total": len(items),
        "pending": counts["pending"],
        "needs_more_info": counts["needs-more-info"],
        "confirmed": counts["confirmed"],
        "rejected": counts["rejected"],
        "resolved": counts["resolved"],
    }


def project_items(
    project_dir: Path,
    status_filter: str | None = None,
    search: str | None = None,
) -> list[dict[str, Any]]:
    items = load_items(project_dir)
    result = items
    if status_filter and status_filter.strip().lower() != "all":
        key = status_filter.strip().lower()
        result = [item for item in result if str(item.get("status", "")).strip().lower() == key]
    if search:
        query = search.strip().lower()
        result = [
            item
            for item in result
            if query in str(item.get("id", "")).lower()
            or query in str(item.get("title", "")).lower()
            or query in str(item.get("description", "")).lower()
            or query in str(item.get("requirement", "")).lower()
        ]
    return sorted(result, key=lambda item: str(item.get("id", "")))
