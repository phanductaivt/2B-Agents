from __future__ import annotations

from datetime import date
from pathlib import Path
import re


def _today() -> str:
    return date.today().isoformat()


def _read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8")


def _line_value(lines: list[str], prefix: str) -> str:
    for line in lines:
        if line.strip().startswith(prefix):
            return line.split(":", 1)[1].strip()
    return ""


def _status_from_files(exists: list[bool]) -> str:
    if all(exists):
        return "Complete"
    if any(exists):
        return "Partial"
    return "Missing"


def _notes_from_files(labels: list[str], exists: list[bool]) -> str:
    missing = [label for label, ok in zip(labels, exists) if not ok]
    if not missing:
        return "Fully traced"
    return "Missing: " + ", ".join(missing)


def _extract_tc_ids_from_test_cases(output_dir: Path) -> list[str]:
    path = output_dir / "test-cases.md"
    if not path.exists():
        return []
    found = re.findall(r"\bTC-\d{3}\b", path.read_text(encoding="utf-8"))
    seen: set[str] = set()
    result: list[str] = []
    for item in found:
        if item in seen:
            continue
        seen.add(item)
        result.append(item)
    return result


def _requirement_status(status_lines: list[str], requirement_name: str) -> str:
    in_table = False
    for line in status_lines:
        if line.strip() == "| Requirement | Current Status | BA | UXUI | FE | Reviewer | Notes |":
            in_table = True
            continue
        if in_table and not line.strip().startswith("|"):
            break
        if in_table and line.strip().startswith("|"):
            columns = [col.strip() for col in line.strip("|").split("|")]
            if columns and columns[0] == requirement_name and len(columns) >= 2:
                return columns[1]
    return "Not Started"


def _list_requirements(project_dir: Path) -> list[Path]:
    requirements_dir = project_dir / "inputs" / "requirements"
    if not requirements_dir.exists():
        return []
    return sorted(path for path in requirements_dir.iterdir() if path.is_file())


def _load_registry(project_dir: Path) -> dict[str, object]:
    registry_path = project_dir / "id-registry.yaml"
    if not registry_path.exists():
        return {}
    registry: dict[str, object] = {}
    current_key: str | None = None
    for raw_line in registry_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.split("#", 1)[0].rstrip()
        if not line.strip():
            continue
        if line.endswith(":") and not line.startswith("-"):
            current_key = line.replace(":", "").strip()
            if current_key == "requirements":
                registry.setdefault(current_key, {})
            else:
                registry.setdefault(current_key, [])
            continue
        if current_key == "requirements" and ":" in line:
            key, value = line.split(":", 1)
            if isinstance(registry.get("requirements"), dict):
                registry["requirements"][key.strip()] = value.strip()
            continue
        if line.strip().startswith("-") and current_key:
            value = line.strip().lstrip("-").strip()
            if isinstance(registry.get(current_key), list):
                registry[current_key].append(value)
    return registry


def _requirement_id(project_dir: Path, requirement_name: str) -> str:
    registry = _load_registry(project_dir)
    filename = f"{requirement_name}.md"
    requirements = registry.get("requirements", {})
    if isinstance(requirements, dict) and filename in requirements:
        return requirements[filename]
    return requirement_name.upper()


def _id_map(requirement_id: str, registry: dict[str, object]) -> dict[str, str]:
    suffix = requirement_id.split("-", 1)[1] if "-" in requirement_id else "001"
    return {
        "req": requirement_id,
        "brd": f"BRD-{suffix}",
        "fr": f"FR-{suffix}",
        "us": f"US-{suffix}",
        "ac": f"AC-{suffix}",
        "feat": f"FEAT-{suffix}",
        "ui": f"UI-{suffix}",
        "rv": f"RV-{suffix}",
        "tc": f"TC-{suffix}",
    }


def _output_dir(project_dir: Path, requirement_name: str) -> Path:
    return project_dir / "outputs" / "generated" / requirement_name


def _output_files(output_dir: Path) -> dict[str, bool]:
    return {
        "brd.md": (output_dir / "brd.md").exists(),
        "frs.md": (output_dir / "frs.md").exists(),
        "user-story.md": (output_dir / "user-story.md").exists(),
        "acceptance-criteria.md": (output_dir / "acceptance-criteria.md").exists(),
        "feature-list.md": (output_dir / "feature-list.md").exists(),
        "process-bpmn.md": (output_dir / "process-bpmn.md").exists(),
        "wireframe.md": (output_dir / "wireframe.md").exists(),
        "ui.html": (output_dir / "ui.html").exists(),
        "review-notes.md": (output_dir / "review-notes.md").exists(),
        "test-cases.md": (output_dir / "test-cases.md").exists(),
    }


def build_requirement_traceability_matrix(
    project_dir: Path,
    requirement_name: str,
    input_file: Path,
    requirement_id: str | None = None,
    tc_ids: list[str] | None = None,
) -> str:
    status_lines = _read_text(project_dir / "status.md").splitlines()
    project_name = _line_value(status_lines, "- Project Name:") or project_dir.name
    last_updated = _line_value(status_lines, "- Last Updated:") or _today()

    output_dir = _output_dir(project_dir, requirement_name)
    outputs = _output_files(output_dir)

    req_id = requirement_id or _requirement_id(project_dir, requirement_name)
    ids = _id_map(req_id, _load_registry(project_dir))
    labels = [
        "BRD",
        "FRS",
        "User Story",
        "Acceptance Criteria",
        "Feature List",
        "BPMN",
        "Wireframe",
        "UI HTML",
        "Review Notes",
        "Test Cases",
    ]
    exists = [
        outputs["brd.md"],
        outputs["frs.md"],
        outputs["user-story.md"],
        outputs["acceptance-criteria.md"],
        outputs["feature-list.md"],
        outputs["process-bpmn.md"],
        outputs["wireframe.md"],
        outputs["ui.html"],
        outputs["review-notes.md"],
        outputs["test-cases.md"],
    ]
    status = _status_from_files(exists)
    notes = _notes_from_files(labels, exists)

    tc_text = ", ".join(tc_ids or []) if tc_ids else "-"
    tc_cell = tc_text if tc_text != "-" else ids["tc"]

    row = " | ".join(
        [
            ids["req"],
            input_file.name,
            ids["brd"],
            ids["fr"],
            ids["us"],
            ids["ac"],
            ids["feat"],
            ids["ui"],
            ids["rv"],
            tc_cell,
            "✅" if outputs["brd.md"] else "❌",
            "✅" if outputs["frs.md"] else "❌",
            "✅" if outputs["user-story.md"] else "❌",
            "✅" if outputs["acceptance-criteria.md"] else "❌",
            "✅" if outputs["feature-list.md"] else "❌",
            "✅" if outputs["process-bpmn.md"] else "❌",
            "✅" if outputs["wireframe.md"] else "❌",
            "✅" if outputs["ui.html"] else "❌",
            "✅" if outputs["review-notes.md"] else "❌",
            "✅" if outputs["test-cases.md"] else "❌",
            status,
            notes,
        ]
    )

    return "\n".join(
        [
            "# Requirement Traceability Matrix",
            "",
            "## Requirement Overview",
            f"- Project Name: {project_name}",
            f"- Requirement Name: {requirement_name}",
            f"- Input File: {input_file.name}",
            f"- Last Updated: {last_updated}",
            "",
            "## Traceability Matrix",
            "",
            "| Requirement ID | Source Input | BRD ID | FR ID | Story ID | AC ID | FEAT ID | UI ID | RV ID | TC ID | BRD | FRS | User Story | Acceptance Criteria | Feature List | BPMN | Wireframe | UI HTML | Review Notes | Test Cases | Status | Notes |",
            "|---------------|-------------|--------|------|---------|------|--------|------|------|------|-----|-----|------------|---------------------|--------------|------|-----------|---------|--------------|----------|--------|------|",
            f"| {row} |",
            "",
        ]
    ).rstrip() + "\n"


def build_requirement_traceability_flow(
    project_dir: Path,
    requirement_name: str,
    input_file: Path,
    requirement_id: str | None = None,
    tc_ids: list[str] | None = None,
) -> str:
    status_lines = _read_text(project_dir / "status.md").splitlines()
    project_name = _line_value(status_lines, "- Project Name:") or project_dir.name
    last_updated = _line_value(status_lines, "- Last Updated:") or _today()

    output_dir = _output_dir(project_dir, requirement_name)
    outputs = _output_files(output_dir)
    req_id = requirement_id or _requirement_id(project_dir, requirement_name)
    ids = _id_map(req_id, _load_registry(project_dir))

    def node(label: str, ok: bool) -> str:
        return f"{'✅' if ok else '❌'} {label}"

    tc_label = "test-cases.md"
    if tc_ids:
        tc_label = "test-cases.md (" + ", ".join(tc_ids) + ")"
    tc_id_label = (tc_ids[0] if tc_ids else ids["tc"])

    return "\n".join(
        [
            "# Requirement Traceability Flow",
            "",
            "## Overview",
            f"- Project Name: {project_name}",
            f"- Requirement Name: {requirement_name}",
            f"- Last Updated: {last_updated}",
            "",
            "## Visual Traceability",
            "",
            "```mermaid",
            "graph TD",
            f"    R[{ids['req']} | {input_file.name}] --> B[{ids['brd']} | {node('brd.md', outputs['brd.md'])}]",
            f"    R --> F[{ids['fr']} | {node('frs.md', outputs['frs.md'])}]",
            f"    F --> U[{ids['us']} | {node('user-story.md', outputs['user-story.md'])}]",
            f"    U --> A[{ids['ac']} | {node('acceptance-criteria.md', outputs['acceptance-criteria.md'])}]",
            f"    F --> FL[{ids['feat']} | {node('feature-list.md', outputs['feature-list.md'])}]",
            f"    F --> P[{node('process-bpmn.md', outputs['process-bpmn.md'])}]",
            f"    F --> W[{node('wireframe.md', outputs['wireframe.md'])}]",
            f"    W --> H[{ids['ui']} | {node('ui.html', outputs['ui.html'])}]",
            f"    H --> RV[{ids['rv']} | {node('review-notes.md', outputs['review-notes.md'])}]",
            f"    A --> TC[{tc_id_label} | {node(tc_label, outputs['test-cases.md'])}]",
            "```",
            "",
            "_Legend: ✅ complete, ❌ missing_",
            "",
        ]
    ).rstrip() + "\n"


def write_requirement_traceability(
    project_dir: Path,
    requirement_name: str,
    input_file: Path,
    requirement_id: str | None = None,
    tc_ids: list[str] | None = None,
) -> list[Path]:
    output_dir = _output_dir(project_dir, requirement_name)
    output_dir.mkdir(parents=True, exist_ok=True)
    matrix_path = output_dir / "requirement-traceability-matrix.md"
    flow_path = output_dir / "requirement-traceability-flow.md"
    matrix_path.write_text(
        build_requirement_traceability_matrix(
            project_dir, requirement_name, input_file, requirement_id, tc_ids
        ),
        encoding="utf-8",
    )
    flow_path.write_text(
        build_requirement_traceability_flow(
            project_dir, requirement_name, input_file, requirement_id, tc_ids
        ),
        encoding="utf-8",
    )
    return [matrix_path, flow_path]


def build_project_traceability_summary(project_dir: Path) -> str:
    status_lines = _read_text(project_dir / "status.md").splitlines()
    project_name = _line_value(status_lines, "- Project Name:") or project_dir.name
    last_updated = _line_value(status_lines, "- Last Updated:") or _today()

    rows: list[str] = []
    registry = _load_registry(project_dir)
    requirements = _list_requirements(project_dir)
    for requirement in requirements:
        output_dir = _output_dir(project_dir, requirement.stem)
        outputs = _output_files(output_dir)
        exists = list(outputs.values())
        status = _status_from_files(exists)
        notes = _notes_from_files(list(outputs.keys()), exists)
        extracted_tc_ids = _extract_tc_ids_from_test_cases(output_dir)
        requirements = registry.get("requirements", {})
        req_id = requirement.name.upper()
        if isinstance(requirements, dict) and requirement.name in requirements:
            req_id = requirements[requirement.name]
        ids = _id_map(req_id, registry)
        tc_cell = ", ".join(extracted_tc_ids) if extracted_tc_ids else ids["tc"]
        rows.append(
            "| "
            + " | ".join(
                [
                    ids["req"],
                    requirement.name,
                    ids["brd"],
                    ids["fr"],
                    ids["us"],
                    ids["ac"],
                    ids["feat"],
                    ids["ui"],
                    ids["rv"],
                    tc_cell,
                    "✅" if outputs["brd.md"] else "❌",
                    "✅" if outputs["frs.md"] else "❌",
                    "✅" if outputs["user-story.md"] else "❌",
                    "✅" if outputs["acceptance-criteria.md"] else "❌",
                    "✅" if outputs["feature-list.md"] else "❌",
                    "✅" if outputs["process-bpmn.md"] else "❌",
                    "✅" if outputs["wireframe.md"] else "❌",
                    "✅" if outputs["ui.html"] else "❌",
                    "✅" if outputs["review-notes.md"] else "❌",
                    "✅" if outputs["test-cases.md"] else "❌",
                    status,
                    notes,
                ]
            )
            + " |"
        )

    if not rows:
        rows.append("| No requirements | - | - | - | - | - | - | - | - | - | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | Missing | No requirements yet |")

    return "\n".join(
        [
            "# Requirement Traceability Summary",
            "",
            "## Project Overview",
            f"- Project Name: {project_name}",
            f"- Last Updated: {last_updated}",
            "",
            "## Traceability Coverage",
            "",
            "| Requirement ID | Source Input | BRD ID | FR ID | Story ID | AC ID | FEAT ID | UI ID | RV ID | TC ID | BRD | FRS | User Story | Acceptance Criteria | Feature List | BPMN | Wireframe | UI HTML | Review Notes | Test Cases | Status | Notes |",
            "|---------------|-------------|--------|------|---------|------|--------|------|------|------|-----|-----|------------|---------------------|--------------|------|-----------|---------|--------------|----------|--------|------|",
            *rows,
            "",
        ]
    ).rstrip() + "\n"


def write_project_traceability_summary(project_dir: Path) -> Path:
    summary_path = project_dir / "requirement-traceability-summary.md"
    summary_path.write_text(build_project_traceability_summary(project_dir), encoding="utf-8")
    return summary_path
