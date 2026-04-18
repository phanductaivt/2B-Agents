from __future__ import annotations

from pathlib import Path
from typing import Any


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8")


def line_value(lines: list[str], prefixes: list[str]) -> str:
    for line in lines:
        stripped = line.strip()
        for prefix in prefixes:
            if stripped.startswith(prefix):
                return stripped.split(":", 1)[1].strip()
    return ""


def collect_section(lines: list[str], header: str) -> list[str]:
    items: list[str] = []
    in_section = False
    for line in lines:
        stripped = line.strip()
        if stripped == header:
            in_section = True
            continue
        if in_section and stripped.startswith("## "):
            break
        if in_section and stripped.startswith("- "):
            items.append(stripped[2:].strip())
    return items


def parse_requirements_table(lines: list[str]) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    in_table = False
    for line in lines:
        if line.strip() == "| Requirement | Current Status | BA | UXUI | FE | Reviewer | Notes |":
            in_table = True
            continue
        if in_table and not line.strip().startswith("|"):
            break
        if in_table and line.strip().startswith("|"):
            cols = [col.strip() for col in line.strip("|").split("|")]
            if len(cols) < 7:
                continue
            if cols[0] in {"Requirement", "------------"}:
                continue
            rows.append(
                {
                    "requirement_name": cols[0],
                    "current_status": cols[1],
                    "ba": cols[2],
                    "uxui": cols[3],
                    "fe": cols[4],
                    "reviewer": cols[5],
                    "notes": cols[6],
                }
            )
    return rows


def parse_artifact_status_rows(status_text: str) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    in_table = False
    for raw_line in status_text.splitlines():
        line = raw_line.strip()
        if line == "| Artifact | Stage | Owner | Status | Approval State | Gate | Notes |":
            in_table = True
            continue
        if in_table and not line.startswith("|"):
            break
        if in_table and line.startswith("|"):
            cols = [col.strip() for col in line.strip("|").split("|")]
            if len(cols) < 7:
                continue
            if cols[0] in {"Artifact", "---------"}:
                continue
            rows.append(
                {
                    "artifact": cols[0],
                    "stage": cols[1],
                    "owner": cols[2],
                    "status": cols[3],
                    "approval_state": cols[4],
                    "gate": cols[5],
                    "notes": cols[6],
                }
            )
    return rows


def parse_gate_result_rows(gate_text: str) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    in_table = False
    for raw_line in gate_text.splitlines():
        line = raw_line.strip()
        if line == "| Artifact | Validation Result | Gate Result | Downstream Allowed | Reason |":
            in_table = True
            continue
        if in_table and not line.startswith("|"):
            break
        if in_table and line.startswith("|"):
            cols = [col.strip() for col in line.strip("|").split("|")]
            if len(cols) < 5:
                continue
            if cols[0] in {"Artifact", "---------"}:
                continue
            rows.append(
                {
                    "artifact": cols[0],
                    "validation_result": cols[1],
                    "gate_result": cols[2],
                    "downstream_allowed": cols[3],
                    "reason": cols[4],
                }
            )
    return rows


def gather_artifact_rows(project_dir: Path, paths_module: Any) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    generated = paths_module.generated_root(project_dir)
    if not generated.exists():
        return rows
    for req_dir in sorted(path for path in generated.iterdir() if path.is_dir()):
        for row in parse_artifact_status_rows(read_text(req_dir / "artifact-status.md")):
            row_with_req = dict(row)
            row_with_req["requirement_name"] = req_dir.name
            rows.append(row_with_req)
    return rows


def gather_gate_rows(project_dir: Path, paths_module: Any) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    generated = paths_module.generated_root(project_dir)
    if not generated.exists():
        return rows
    for req_dir in sorted(path for path in generated.iterdir() if path.is_dir()):
        for row in parse_gate_result_rows(read_text(req_dir / "gate-results.md")):
            row_with_req = dict(row)
            row_with_req["requirement_name"] = req_dir.name
            rows.append(row_with_req)
    return rows


def load_confirmation_items(project_dir: Path, paths_module: Any, yaml_module: Any) -> list[dict[str, Any]]:
    path = paths_module.pending_confirmations_yaml_path(project_dir)
    if yaml_module is None or not path.exists():
        return []
    raw = yaml_module.safe_load(path.read_text(encoding="utf-8")) or {}
    items = raw.get("items", []) if isinstance(raw, dict) else []
    return items if isinstance(items, list) else []


def confirmation_summary(items: list[dict[str, Any]]) -> dict[str, int]:
    pending = 0
    needs_more_info = 0
    resolved = 0
    for item in items:
        if not isinstance(item, dict):
            continue
        status = str(item.get("status", "pending")).strip().lower()
        if status == "pending":
            pending += 1
        elif status == "needs-more-info":
            needs_more_info += 1
        elif status in {"confirmed", "rejected", "resolved"}:
            resolved += 1
    return {
        "pending": pending,
        "needs_more_info": needs_more_info,
        "open": pending + needs_more_info,
        "resolved": resolved,
    }
