from __future__ import annotations

import importlib.util
from pathlib import Path
import sys


def _load_module(module_name: str, file_path: Path):
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Could not load module: {file_path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


_PATHS = _load_module(
    "project_paths_for_project_flow_manager",
    Path(__file__).resolve().parent / "project_paths.py",
)


def _read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8")


def _line_value(lines: list[str], prefix: str) -> str:
    for line in lines:
        if line.strip().startswith(prefix):
            return line.split(":", 1)[1].strip()
    return ""


def _status_symbol(path: Path) -> str:
    return "✅" if path.exists() else "❌"


def _list_requirements(project_dir: Path) -> list[Path]:
    requirements_dir = _PATHS.requirements_dir(project_dir)
    if not requirements_dir.exists():
        return []
    return sorted(path for path in requirements_dir.iterdir() if path.is_file())


def _output_folder(project_dir: Path, requirement_name: str) -> Path:
    return _PATHS.requirement_output_dir(project_dir, requirement_name)


def _existing_outputs(output_dir: Path) -> dict[str, bool]:
    return {
        "clarification.md": (output_dir / "clarification.md").exists(),
        "process-bpmn.md": (output_dir / "process-bpmn.md").exists(),
        "user-story.md": (output_dir / "user-story.md").exists(),
        "acceptance-criteria.md": (output_dir / "acceptance-criteria.md").exists(),
        "brd.md": (output_dir / "brd.md").exists(),
        "frs.md": (output_dir / "frs.md").exists(),
        "feature-list.md": (output_dir / "feature-list.md").exists(),
        "wireframe.md": (output_dir / "wireframe.md").exists(),
        "ui.html": (output_dir / "ui.html").exists(),
        "review-notes.md": (output_dir / "review-notes.md").exists(),
    }


def _trace_node(label: str, exists: bool) -> str:
    if exists:
        return f"✅ {label}"
    return f"❌ {label}"


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


def build_project_flow(project_dir: Path) -> str:
    status_lines = _read_text(_PATHS.status_path(project_dir)).splitlines()
    project_name = _line_value(status_lines, "- Project Name:") or project_dir.name
    stage = _line_value(status_lines, "- Current Stage:") or "Draft"
    last_updated = _line_value(status_lines, "- Last Updated:") or "Unknown"

    requirements = _list_requirements(project_dir)
    requirement_names = [req.stem for req in requirements]
    requirement_rows: list[str] = []
    trace_sections: list[str] = []

    for requirement in requirements:
        output_dir = _output_folder(project_dir, requirement.stem)
        outputs = _existing_outputs(output_dir)

        ba_done = all(
            outputs[name]
            for name in [
                "clarification.md",
                "process-bpmn.md",
                "user-story.md",
                "acceptance-criteria.md",
                "brd.md",
                "frs.md",
                "feature-list.md",
            ]
        )
        uxui_done = outputs["wireframe.md"]
        fe_done = outputs["ui.html"]
        reviewer_done = outputs["review-notes.md"]

        requirement_status = _requirement_status(status_lines, requirement.stem)
        requirement_rows.append(
            "| "
            + " | ".join(
                [
                    requirement.stem,
                    requirement_status,
                    "✅" if ba_done else "❌",
                    "✅" if uxui_done else "❌",
                    "✅" if fe_done else "❌",
                    "✅" if reviewer_done else "❌",
                    f"_ops/generated/{requirement.stem}",
                ]
            )
            + " |"
        )

        trace_sections.extend(
            [
                f"### Traceability: {requirement.name}",
                "",
                "```mermaid",
                "flowchart LR",
                f"    REQ[{requirement.name}] --> CLAR[{_trace_node('clarification.md', outputs['clarification.md'])}]",
                f"    CLAR --> BPMN[{_trace_node('process-bpmn.md', outputs['process-bpmn.md'])}]",
                f"    BPMN --> STORY[{_trace_node('user-story.md', outputs['user-story.md'])}]",
                f"    STORY --> AC[{_trace_node('acceptance-criteria.md', outputs['acceptance-criteria.md'])}]",
                f"    AC --> BRD[{_trace_node('brd.md', outputs['brd.md'])}]",
                f"    BRD --> FRS[{_trace_node('frs.md', outputs['frs.md'])}]",
                f"    FRS --> FEATURE[{_trace_node('feature-list.md', outputs['feature-list.md'])}]",
                f"    FEATURE --> WIRE[{_trace_node('wireframe.md', outputs['wireframe.md'])}]",
                f"    WIRE --> UI[{_trace_node('ui.html', outputs['ui.html'])}]",
                f"    UI --> REVIEW[{_trace_node('review-notes.md', outputs['review-notes.md'])}]",
                "```",
                "",
                "_Legend: ✅ complete, ❌ missing_",
                "",
            ]
        )

    if not requirement_rows:
        requirement_rows.append("| No requirements yet | Not Started | ❌ | ❌ | ❌ | ❌ | _ops/generated/ |")

    requirement_input_list = "\n".join(
        f"    R{index}[01-input/requirements/{name}.md]"
        for index, name in enumerate(requirement_names, start=1)
    )
    requirement_edges = "\n".join(
        f"    R{index} --> BA" for index, _ in enumerate(requirement_names, start=1)
    )
    if not requirement_names:
        requirement_input_list = "    R1[01-input/requirements/req-001.md]"
        requirement_edges = "    R1 --> BA"

    return "\n".join(
        [
            "# Project Flow",
            "",
            "## Project Overview",
            f"- Project Name: {project_name}",
            f"- Current Stage: {stage}",
            f"- Last Updated: {last_updated}",
            "",
            "## High-Level Flow",
            "",
            "```mermaid",
            "flowchart LR",
            requirement_input_list,
            "    BA[BA Agent]",
            "    UX[UXUI Agent]",
            "    FE[FE Agent]",
            "    RV[Reviewer / Validators]",
            "    OUT[_ops/generated/<requirement-name>/]",
            requirement_edges,
            "    BA --> UX",
            "    UX --> FE",
            "    FE --> RV",
            "    RV --> OUT",
            "```",
            "",
            "## Current Requirements",
            "",
            "| Requirement | Status | BA | UXUI | FE | Reviewer | Output Folder |",
            "|------------|--------|----|------|----|----------|---------------|",
            *requirement_rows,
            "",
            "## Project Status Flow",
            "",
            "```mermaid",
            "flowchart LR",
            "    IN[Requirement Input] --> GEN[Output Generation]",
            "    GEN --> STATUS[_ops/status.md update]",
            "    STATUS --> DASH[workspace/dashboard.md update]",
            "    DASH --> HTML[workspace/dashboard.html update]",
            "```",
            "",
            *trace_sections,
        ]
    ).rstrip() + "\n"


def write_project_flow(project_dir: Path) -> Path:
    project_flow_path = _PATHS.project_flow_path(project_dir)
    project_flow_path.parent.mkdir(parents=True, exist_ok=True)
    project_flow_path.write_text(build_project_flow(project_dir), encoding="utf-8")
    return project_flow_path
