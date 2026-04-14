from __future__ import annotations

from datetime import date
from pathlib import Path
import re


def _today() -> str:
    return date.today().isoformat()


def _read_if_exists(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8")


def _extract_id_number(value: str) -> int:
    match = re.search(r"-(\d+)$", value.strip())
    if not match:
        return 0
    return int(match.group(1))


def _sorted_ids(values: list[str], prefix: str) -> list[str]:
    filtered = [value.strip() for value in values if value.strip().startswith(prefix + "-")]
    return sorted(filtered, key=_extract_id_number)


def _parse_registry(project_dir: Path) -> dict[str, object]:
    path = project_dir / "id-registry.yaml"
    if not path.exists():
        return {}
    data: dict[str, object] = {}
    current_key: str | None = None

    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.split("#", 1)[0].rstrip()
        stripped = line.strip()
        if not stripped:
            continue

        if stripped.endswith(":") and not stripped.startswith("-"):
            current_key = stripped[:-1]
            if current_key == "requirements":
                data[current_key] = {}
            else:
                data.setdefault(current_key, [])
            continue

        if current_key == "requirements" and ":" in stripped:
            key, value = stripped.split(":", 1)
            requirements = data.get("requirements", {})
            if isinstance(requirements, dict):
                requirements[key.strip()] = value.strip()
                data["requirements"] = requirements
            continue

        if stripped.startswith("-") and current_key:
            values = data.get(current_key, [])
            if isinstance(values, list):
                values.append(stripped.lstrip("-").strip())
                data[current_key] = values

    return data


def _parse_status_table(project_dir: Path) -> dict[str, dict[str, str]]:
    status_text = _read_if_exists(project_dir / "status.md")
    rows: dict[str, dict[str, str]] = {}
    in_table = False

    for line in status_text.splitlines():
        if line.strip() == "| Requirement | Current Status | BA | UXUI | FE | Reviewer | Notes |":
            in_table = True
            continue

        if in_table and not line.strip().startswith("|"):
            break

        if in_table and line.strip().startswith("|"):
            columns = [part.strip() for part in line.strip().strip("|").split("|")]
            if len(columns) < 7:
                continue
            requirement_name = columns[0]
            if requirement_name.lower() == "requirement":
                continue
            rows[requirement_name] = {
                "current_status": columns[1],
                "ba": columns[2],
                "uxui": columns[3],
                "fe": columns[4],
                "reviewer": columns[5],
                "notes": columns[6],
            }

    return rows


def _requirement_output_flags(project_dir: Path, requirement_name: str) -> dict[str, bool]:
    output_dir = project_dir / "outputs" / "generated" / requirement_name
    return {
        "frs": (output_dir / "frs.md").exists(),
        "wireframe": (output_dir / "wireframe.md").exists(),
        "ui": (output_dir / "ui.html").exists(),
        "review": (output_dir / "review-notes.md").exists(),
    }


def _build_dependency_rows(project_dir: Path) -> list[dict[str, str]]:
    registry = _parse_registry(project_dir)
    rows: list[dict[str, str]] = []

    requirements_map = registry.get("requirements", {})
    requirement_ids: list[str] = []
    if isinstance(requirements_map, dict):
        requirement_ids = _sorted_ids(list(requirements_map.values()), "REQ")

    fr_ids = _sorted_ids(
        registry.get("fr", []) if isinstance(registry.get("fr", []), list) else [], "FR"
    )
    feat_ids = _sorted_ids(
        registry.get("feature", []) if isinstance(registry.get("feature", []), list) else [], "FEAT"
    )

    # Requirement-to-requirement dependency chain
    for index in range(1, len(requirement_ids)):
        current_req = requirement_ids[index]
        previous_req = requirement_ids[index - 1]
        rows.append(
            {
                "item_id": current_req,
                "depends_on": previous_req,
                "type": "Requirement",
                "reason": f"{current_req} builds on the base scope from {previous_req}",
                "impact": "High",
                "notes": "Downstream requirement may pause if upstream scope changes.",
            }
        )

    # FR depends on parent REQ with the same suffix
    for fr_id in fr_ids:
        suffix = fr_id.split("-", 1)[1] if "-" in fr_id else ""
        parent_req = f"REQ-{suffix}" if suffix else ""
        if parent_req and parent_req in requirement_ids:
            rows.append(
                {
                    "item_id": fr_id,
                    "depends_on": parent_req,
                    "type": "Functional Requirement",
                    "reason": f"{fr_id} is derived from {parent_req}",
                    "impact": "High",
                    "notes": "If the parent requirement changes, this FR must be reviewed.",
                }
            )

    # Functional requirement chain
    for index in range(1, len(fr_ids)):
        current_fr = fr_ids[index]
        previous_fr = fr_ids[index - 1]
        rows.append(
            {
                "item_id": current_fr,
                "depends_on": previous_fr,
                "type": "Functional Requirement",
                "reason": f"{current_fr} needs the flow foundation from {previous_fr}",
                "impact": "Medium",
                "notes": "UI flow can be blocked if prerequisite FR is unstable.",
            }
        )

    # Feature dependency on FR with the same numeric suffix
    for feat_id in feat_ids:
        suffix = feat_id.split("-", 1)[1] if "-" in feat_id else ""
        parent_fr = f"FR-{suffix}" if suffix else ""
        if parent_fr and parent_fr in fr_ids:
            rows.append(
                {
                    "item_id": feat_id,
                    "depends_on": parent_fr,
                    "type": "Feature",
                    "reason": f"{feat_id} is derived from {parent_fr}",
                    "impact": "Medium",
                    "notes": "Feature details should follow the parent FR structure.",
                }
            )

    # Fallback for small projects with only one requirement
    if not rows and requirement_ids and fr_ids:
        rows.append(
            {
                "item_id": fr_ids[0],
                "depends_on": requirement_ids[0],
                "type": "Functional Requirement",
                "reason": "Functional scope must come from the approved requirement.",
                "impact": "High",
                "notes": "If requirement changes, FR should be reviewed.",
            }
        )

    return rows


def _build_dependency_risks(project_dir: Path) -> list[str]:
    risks: list[str] = []
    status_rows = _parse_status_table(project_dir)

    requirements_dir = project_dir / "inputs" / "requirements"
    requirement_files = []
    if requirements_dir.exists():
        requirement_files = sorted(path for path in requirements_dir.iterdir() if path.is_file())

    for file_path in requirement_files:
        req_name = file_path.stem
        status = status_rows.get(req_name, {})
        current_status = status.get("current_status", "Not Started")
        flags = _requirement_output_flags(project_dir, req_name)

        if current_status == "Blocked":
            risks.append(
                f"{req_name} is blocked in status.md. Dependent UXUI/FE work should pause until BA gaps are resolved."
            )

        if not flags["frs"]:
            risks.append(
                f"{req_name} is missing `frs.md`. This is a High dependency risk because UXUI and FE depend on FRS."
            )
        elif not flags["wireframe"]:
            risks.append(
                f"{req_name} is missing `wireframe.md`. FE implementation quality may drop without UX guidance."
            )
        elif not flags["ui"]:
            risks.append(f"{req_name} is missing `ui.html`. FE delivery is not complete yet.")

        if flags["ui"] and not flags["review"]:
            risks.append(
                f"{req_name} has UI output but no `review-notes.md`. Review dependency is incomplete before handover."
            )

    if not risks:
        risks.append("No high dependency risk detected from current project files.")

    return risks


def _to_node_id(value: str) -> str:
    return re.sub(r"[^A-Za-z0-9]", "", value)


def _build_mermaid(rows: list[dict[str, str]]) -> str:
    if not rows:
        return "\n".join(
            [
                "```mermaid",
                "graph LR",
                "    A[No dependency items yet]",
                "```",
            ]
        )

    declared_nodes: dict[str, str] = {}
    edges: list[str] = []

    for row in rows:
        item = row["item_id"]
        dependency = row["depends_on"]
        item_node = _to_node_id(item)
        dep_node = _to_node_id(dependency)
        declared_nodes[item_node] = item
        declared_nodes[dep_node] = dependency
        edges.append(f"    {dep_node}[{dependency}] --> {item_node}[{item}]")

    lines = ["```mermaid", "graph LR"]
    lines.extend(edges)
    lines.append("```")
    return "\n".join(lines)


def build_dependency_map(project_dir: Path) -> str:
    rows = _build_dependency_rows(project_dir)
    risks = _build_dependency_risks(project_dir)
    project_name = project_dir.name

    lines: list[str] = [
        "# Dependency Map",
        "",
        "## Overview",
        f"- Project Name: {project_name}",
        f"- Last Updated: {_today()}",
        "",
        "## Dependency Table",
        "",
        "| Item ID | Depends On | Type | Reason | Impact if Missing | Notes |",
        "|--------|------------|------|--------|-------------------|------|",
    ]

    if rows:
        for row in rows:
            lines.append(
                "| "
                + " | ".join(
                    [
                        row["item_id"],
                        row["depends_on"],
                        row["type"],
                        row["reason"],
                        row["impact"],
                        row["notes"],
                    ]
                )
                + " |"
            )
    else:
        lines.append("| - | - | - | No dependency has been identified yet. | - | Add more requirements to map dependencies. |")

    lines.extend(
        [
            "",
            "## Visual Dependency Graph",
            "",
            _build_mermaid(rows),
            "",
            "## Dependency Risks for Downstream Work",
        ]
    )

    for risk in risks:
        lines.append(f"- {risk}")

    lines.extend(
        [
            "",
            "<!-- TODO: Add optional manual dependency tags in requirement files for more precise mapping. -->",
            "",
        ]
    )

    return "\n".join(lines)


def write_dependency_map(project_dir: Path) -> Path:
    path = project_dir / "dependency-map.md"
    path.write_text(build_dependency_map(project_dir), encoding="utf-8")
    return path
