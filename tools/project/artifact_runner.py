from __future__ import annotations

from datetime import date
from pathlib import Path
import re


def _today() -> str:
    return date.today().isoformat()


def _strip_comment(line: str) -> str:
    if "#" not in line:
        return line.rstrip()
    head, _tail = line.split("#", 1)
    return head.rstrip()


def _parse_inline_list(value: str) -> list[str]:
    raw = value.strip()
    if raw == "[]":
        return []
    if not (raw.startswith("[") and raw.endswith("]")):
        return []
    inside = raw[1:-1].strip()
    if not inside:
        return []
    return [item.strip().strip("'\"") for item in inside.split(",") if item.strip()]


def load_artifact_catalog(catalog_path: Path) -> list[dict[str, object]]:
    """
    Parse artifacts/artifact-catalog.yaml with a lightweight custom parser.
    """
    if not catalog_path.exists():
        raise FileNotFoundError(f"Missing artifact catalog: {catalog_path}")

    artifacts: list[dict[str, object]] = []
    current: dict[str, object] | None = None
    current_list_key: str | None = None

    for raw in catalog_path.read_text(encoding="utf-8").splitlines():
        line = _strip_comment(raw)
        stripped = line.strip()
        if not stripped or stripped == "artifacts:":
            continue

        if stripped.startswith("- name:"):
            if current:
                artifacts.append(current)
            current = {
                "name": stripped.split(":", 1)[1].strip(),
                "stage": "",
                "owner": "",
                "dependencies": [],
                "outputs": [],
                "validators": [],
                "gate_required": True,
            }
            current_list_key = None
            continue

        if current is None:
            continue

        if stripped.startswith("- ") and current_list_key:
            value = stripped[2:].strip()
            values = current.get(current_list_key, [])
            if isinstance(values, list):
                values.append(value)
                current[current_list_key] = values
            continue

        if ":" not in stripped:
            continue

        key, value = stripped.split(":", 1)
        key = key.strip()
        value = value.strip()

        if key in {"dependencies", "outputs", "validators"}:
            if value:
                current[key] = _parse_inline_list(value)
                current_list_key = None
            else:
                current[key] = []
                current_list_key = key
            continue

        if key == "gate_required":
            current[key] = value.lower() == "true"
            current_list_key = None
            continue

        current[key] = value
        current_list_key = None

    if current:
        artifacts.append(current)

    return artifacts


def catalog_by_name(catalog: list[dict[str, object]]) -> dict[str, dict[str, object]]:
    result: dict[str, dict[str, object]] = {}
    for item in catalog:
        name = str(item.get("name", "")).strip()
        if not name:
            continue
        result[name] = item
    return result


def list_stages(catalog: list[dict[str, object]]) -> list[str]:
    stages = []
    seen: set[str] = set()
    for item in catalog:
        stage = str(item.get("stage", "")).strip()
        if stage and stage not in seen:
            seen.add(stage)
            stages.append(stage)
    return stages


def _resolve_dependencies(
    artifact_name: str,
    indexed: dict[str, dict[str, object]],
    visited: set[str],
    stack: set[str],
    ordered: list[str],
) -> None:
    if artifact_name in visited:
        return
    if artifact_name in stack:
        raise ValueError(f"Circular artifact dependency detected at '{artifact_name}'.")
    if artifact_name not in indexed:
        raise ValueError(f"Artifact '{artifact_name}' is not defined in artifact catalog.")

    stack.add(artifact_name)
    artifact = indexed[artifact_name]
    dependencies = artifact.get("dependencies", [])
    if isinstance(dependencies, list):
        for dep in dependencies:
            dep_name = str(dep).strip()
            if dep_name:
                _resolve_dependencies(dep_name, indexed, visited, stack, ordered)

    stack.remove(artifact_name)
    visited.add(artifact_name)
    ordered.append(artifact_name)


def build_execution_plan(
    catalog: list[dict[str, object]],
    target_artifact: str | None = None,
    target_stage: str | None = None,
) -> list[str]:
    indexed = catalog_by_name(catalog)
    selected: list[str]

    if target_artifact:
        artifact_key = target_artifact.strip()
        if artifact_key not in indexed:
            raise ValueError(f"Unknown artifact '{target_artifact}'.")
        selected = [artifact_key]
    elif target_stage:
        selected = [
            str(item.get("name", "")).strip()
            for item in catalog
            if str(item.get("stage", "")).strip() == target_stage
        ]
        if not selected:
            raise ValueError(f"Unknown stage '{target_stage}'.")
    else:
        selected = [str(item.get("name", "")).strip() for item in catalog if str(item.get("name", "")).strip()]

    visited: set[str] = set()
    ordered: list[str] = []
    for name in selected:
        _resolve_dependencies(name, indexed, visited, set(), ordered)
    return ordered


def _status_path(project_dir: Path, requirement_name: str) -> Path:
    return project_dir / "outputs" / "generated" / requirement_name / "artifact-status.md"


def _default_state(catalog: list[dict[str, object]]) -> dict[str, dict[str, str]]:
    state: dict[str, dict[str, str]] = {}
    for item in catalog:
        name = str(item.get("name", "")).strip()
        if not name:
            continue
        dependencies = item.get("dependencies", [])
        dep_text = ", ".join([str(dep).strip() for dep in dependencies if str(dep).strip()]) if isinstance(dependencies, list) else "-"
        state[name] = {
            "status": "Not Started",
            "gate": "N/A",
            "notes": "-",
            "dependencies": dep_text if dep_text else "None",
        }
    return state


def parse_artifact_status(project_dir: Path, requirement_name: str, catalog: list[dict[str, object]]) -> dict[str, dict[str, str]]:
    path = _status_path(project_dir, requirement_name)
    state = _default_state(catalog)
    if not path.exists():
        return state

    in_table = False
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if line == "| Artifact | Stage | Owner | Status | Dependencies | Gate | Notes |":
            in_table = True
            continue
        if in_table and not line.startswith("|"):
            break
        if in_table and line.startswith("|"):
            cols = [col.strip() for col in line.strip("|").split("|")]
            if len(cols) < 7:
                continue
            artifact = cols[0]
            if artifact not in state:
                continue
            state[artifact]["status"] = cols[3]
            state[artifact]["dependencies"] = cols[4] or "None"
            state[artifact]["gate"] = cols[5]
            state[artifact]["notes"] = cols[6] or "-"
    return state


def write_artifact_status(
    project_dir: Path,
    requirement_name: str,
    requirement_id: str,
    catalog: list[dict[str, object]],
    state: dict[str, dict[str, str]],
) -> Path:
    output_dir = project_dir / "outputs" / "generated" / requirement_name
    output_dir.mkdir(parents=True, exist_ok=True)
    path = _status_path(project_dir, requirement_name)
    lines = [
        "# Artifact Status",
        "",
        "## Overview",
        f"- Project Name: {project_dir.name}",
        f"- Requirement Name: {requirement_name}",
        f"- Requirement ID: {requirement_id}",
        f"- Last Updated: {_today()}",
        "",
        "## Artifact Table",
        "",
        "| Artifact | Stage | Owner | Status | Dependencies | Gate | Notes |",
        "|---------|------|------|--------|-------------|------|------|",
    ]

    for item in catalog:
        name = str(item.get("name", "")).strip()
        if not name:
            continue
        row = state.get(name, {})
        stage = str(item.get("stage", "")).strip()
        owner = str(item.get("owner", "")).strip().replace("-agent", "").upper()
        lines.append(
            "| "
            + " | ".join(
                [
                    name,
                    stage,
                    owner or "-",
                    row.get("status", "Not Started"),
                    row.get("dependencies", "None"),
                    row.get("gate", "N/A"),
                    row.get("notes", "-"),
                ]
            )
            + " |"
        )

    lines.extend(
        [
            "",
            "Suggested status values:",
            "- Not Started",
            "- In Progress",
            "- Done",
            "- In Review",
            "- Blocked",
            "- Rework Needed",
            "",
            "Suggested gate values:",
            "- Pass",
            "- Warning",
            "- Fail",
            "- Not Allowed",
            "- N/A",
            "",
            "<!-- TODO: Add optional approval column when the governance model requires explicit sign-off. -->",
            "",
        ]
    )
    path.write_text("\n".join(lines), encoding="utf-8")
    return path


def ensure_artifact_status(
    project_dir: Path,
    requirement_name: str,
    requirement_id: str,
    catalog: list[dict[str, object]],
) -> Path:
    state = parse_artifact_status(project_dir, requirement_name, catalog)
    return write_artifact_status(project_dir, requirement_name, requirement_id, catalog, state)


def ensure_artifact_checklist(
    project_dir: Path,
    requirement_name: str,
    requirement_id: str,
    catalog: list[dict[str, object]],
) -> Path:
    output_dir = project_dir / "outputs" / "generated" / requirement_name
    output_dir.mkdir(parents=True, exist_ok=True)
    path = output_dir / "artifact-checklist.md"
    if path.exists():
        return path

    lines = [
        "# Artifact Checklist",
        "",
        f"- Project Name: {project_dir.name}",
        f"- Requirement Name: {requirement_name}",
        f"- Requirement ID: {requirement_id}",
        "",
    ]
    for item in catalog:
        name = str(item.get("name", "")).strip()
        stage = str(item.get("stage", "")).strip()
        dependencies = item.get("dependencies", [])
        dep_text = ", ".join([str(dep).strip() for dep in dependencies if str(dep).strip()]) if isinstance(dependencies, list) else "None"
        if not dep_text:
            dep_text = "None"
        if not name:
            continue
        lines.extend(
            [
                f"## {name}",
                f"- [ ] Stage confirmed: {stage}",
                f"- [ ] Dependencies confirmed: {dep_text}",
                "- [ ] Content quality reviewed",
                "- [ ] Gate status reviewed in artifact-status.md",
                "",
            ]
        )

    lines.append("<!-- TODO: Add optional owner sign-off checkbox if the team wants explicit approvals. -->")
    lines.append("")
    path.write_text("\n".join(lines), encoding="utf-8")
    return path


def _is_done_and_pass(row: dict[str, str]) -> bool:
    return row.get("status") == "Done" and row.get("gate") == "Pass"


def check_dependencies(
    artifact_name: str,
    catalog_index: dict[str, dict[str, object]],
    state: dict[str, dict[str, str]],
) -> tuple[bool, list[str]]:
    item = catalog_index.get(artifact_name, {})
    deps = item.get("dependencies", [])
    issues: list[str] = []
    if isinstance(deps, list):
        for dep in deps:
            dep_name = str(dep).strip()
            dep_state = state.get(dep_name, {})
            if not _is_done_and_pass(dep_state):
                issues.append(f"{dep_name} is not Done/Pass")
    return (len(issues) == 0, issues)


def detect_gate(artifact_name: str, content: str) -> tuple[str, str]:
    text = content.strip()
    if not text:
        return ("Fail", "Generated content is empty.")

    rules: dict[str, list[str]] = {
        "clarification": ["## Summary", "## Known Facts", "## Open Questions"],
        "brd": ["## Business Goals", "## Business Rules"],
        "process-bpmn": ["```mermaid"],
        "frs": ["## Main Flow", "## Alternative Flows", "## Edge Cases"],
        "user-story": ["## Story", "## INVEST Check"],
        "acceptance-criteria": ["## Criteria"],
        "feature-list": ["## "],
        "wireframe": ["## Main Sections", "## Wireframe Sketch"],
        "ui": ["<html", "</html>"],
        "review": ["Validation Status", "## Ambiguity Checker"],
        "test-cases": ["| TC ID |", "## Test Case Matrix"],
        "requirement-traceability-matrix": ["| Requirement ID |", "## Traceability Matrix"],
        "requirement-traceability-flow": ["```mermaid"],
        "risk-notes": ["## Key Risks"],
        "dependency-map": ["## Dependency Table", "```mermaid"],
    }
    required = rules.get(artifact_name, [])
    missing = [token for token in required if token.lower() not in text.lower()]
    if missing:
        return ("Warning", "Missing expected tokens: " + ", ".join(missing))
    return ("Pass", "Artifact quality check passed.")


def set_in_progress(state: dict[str, dict[str, str]], artifact_name: str) -> None:
    row = state.get(artifact_name, {})
    row["status"] = "In Progress"
    row["gate"] = "N/A"
    row["notes"] = "Running artifact generation."
    state[artifact_name] = row


def set_blocked(state: dict[str, dict[str, str]], artifact_name: str, reasons: list[str]) -> None:
    row = state.get(artifact_name, {})
    row["status"] = "Blocked"
    row["gate"] = "Not Allowed"
    row["notes"] = "; ".join(reasons) if reasons else "Dependency gate is not satisfied."
    state[artifact_name] = row


def set_result(state: dict[str, dict[str, str]], artifact_name: str, gate: str, note: str) -> None:
    row = state.get(artifact_name, {})
    if gate == "Pass":
        row["status"] = "Done"
    elif gate == "Warning":
        row["status"] = "In Review"
    else:
        row["status"] = "Rework Needed"
    row["gate"] = gate
    row["notes"] = note
    state[artifact_name] = row


def artifact_from_output_file(catalog: list[dict[str, object]], output_file: str) -> str | None:
    file_name = output_file.strip()
    for item in catalog:
        name = str(item.get("name", "")).strip()
        outputs = item.get("outputs", [])
        if not name or not isinstance(outputs, list):
            continue
        if file_name in [str(value).strip() for value in outputs]:
            return name
    return None


def write_gate_report(
    project_dir: Path,
    requirement_name: str,
    requirement_id: str,
    catalog: list[dict[str, object]],
    state: dict[str, dict[str, str]],
) -> Path:
    output_dir = project_dir / "outputs" / "generated" / requirement_name
    output_dir.mkdir(parents=True, exist_ok=True)
    path = output_dir / "gate-report.md"

    lines = [
        "# Gate Report",
        "",
        f"- Project Name: {project_dir.name}",
        f"- Requirement Name: {requirement_name}",
        f"- Requirement ID: {requirement_id}",
        f"- Last Updated: {_today()}",
        "",
        "| Artifact | Stage | Status | Gate | Notes |",
        "|---------|------|--------|------|------|",
    ]

    blocked: list[str] = []
    for item in catalog:
        name = str(item.get("name", "")).strip()
        if not name:
            continue
        stage = str(item.get("stage", "")).strip()
        row = state.get(name, {})
        status = row.get("status", "Not Started")
        gate = row.get("gate", "N/A")
        notes = row.get("notes", "-")
        lines.append(f"| {name} | {stage} | {status} | {gate} | {notes} |")
        if status in {"Blocked", "Rework Needed"} or gate in {"Fail", "Not Allowed"}:
            blocked.append(name)

    lines.append("")
    lines.append("## Current Gate State")
    if blocked:
        for name in blocked:
            lines.append(f"- Blocked artifact: {name}")
    else:
        lines.append("- No blocked artifact.")
    lines.append("")
    path.write_text("\n".join(lines), encoding="utf-8")
    return path
