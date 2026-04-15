from __future__ import annotations

from datetime import date
import importlib.util
from pathlib import Path
import sys


def _today() -> str:
    return date.today().isoformat()


def _load_module(module_name: str, file_path: Path):
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Could not load module: {file_path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


_PATHS = _load_module(
    "project_paths_for_requirement_flow_manager",
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


def _status_symbol(path: Path, blocked: bool) -> str:
    if path.exists():
        return "✅ Done"
    if blocked:
        return "⛔ Blocked"
    return "❌ Missing"


def _trace_node(label: str, exists: bool, blocked: bool, gate_result: str = "") -> str:
    gate_note = f" [{gate_result}]" if gate_result and gate_result != "Not Run" else ""
    if exists:
        return f"✅ {label}{gate_note}"
    if blocked:
        return f"⛔ {label}{gate_note}"
    return f"❌ {label}{gate_note}"


def _artifact_from_output_file(file_name: str) -> str:
    mapping = {
        "clarification.md": "clarification",
        "process-bpmn.md": "process-bpmn",
        "user-story.md": "user-story",
        "acceptance-criteria.md": "acceptance-criteria",
        "brd.md": "brd",
        "frs.md": "frs",
        "feature-list.md": "feature-list",
        "wireframe.md": "wireframe",
        "ui.html": "ui",
        "review-notes.md": "review",
    }
    return mapping.get(file_name, file_name)


def _parse_gate_results(output_dir: Path) -> dict[str, str]:
    path = output_dir / "gate-results.md"
    if not path.exists():
        return {}

    gates: dict[str, str] = {}
    in_table = False
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if line == "| Artifact | Validation Result | Gate Result | Downstream Allowed | Reason |":
            in_table = True
            continue
        if in_table and not line.startswith("|"):
            break
        if in_table and line.startswith("|"):
            columns = [col.strip() for col in line.strip("|").split("|")]
            if len(columns) < 3:
                continue
            artifact_name = columns[0]
            if artifact_name in {"Artifact", "---------"}:
                continue
            gates[artifact_name] = columns[2]
    return gates


def _status_with_gate(path: Path, blocked: bool, gate_result: str) -> str:
    base = _status_symbol(path, blocked)
    if gate_result and gate_result != "Not Run":
        return f"{base} ({gate_result})"
    return base


def build_requirement_flow(
    project_dir: Path,
    requirement_name: str,
    input_file: Path,
    requirement_id: str | None = None,
) -> str:
    status_lines = _read_text(_PATHS.status_path(project_dir)).splitlines()
    project_name = _line_value(status_lines, "- Project Name:") or project_dir.name
    last_updated = _line_value(status_lines, "- Last Updated:") or _today()
    requirement_status = _requirement_status(status_lines, requirement_name)
    requirement_id_text = requirement_id or requirement_name.upper()
    is_blocked = requirement_status.lower() == "blocked"
    try:
        input_file_display = str(input_file.relative_to(project_dir))
    except ValueError:
        input_file_display = input_file.name

    output_dir = _PATHS.requirement_output_dir(project_dir, requirement_name)
    gate_results = _parse_gate_results(output_dir)
    outputs = {
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

    output_rows: list[str] = []
    for file_name, exists in outputs.items():
        gate_result = gate_results.get(_artifact_from_output_file(file_name), "")
        output_rows.append(
            f"| {file_name} | {_status_with_gate(output_dir / file_name, is_blocked, gate_result)} |"
        )

    next_actions: list[str] = []
    if is_blocked:
        next_actions.append("Unblock the requirement by resolving the blocker in _ops/status.md.")
    if not outputs["clarification.md"]:
        next_actions.append("Complete clarification.md before drafting downstream outputs.")
    frs_gate = gate_results.get("frs", "")
    if frs_gate in {"Fail", "Not Allowed"}:
        next_actions.append("Fix FRS quality issues first because downstream UXUI/FE is blocked.")
    if not outputs["frs.md"]:
        next_actions.append("Complete frs.md to unlock UXUI and FE work.")
    if gate_results.get("wireframe") == "Not Allowed":
        next_actions.append("Wireframe is blocked. Ensure FRS gate reaches Pass.")
    if gate_results.get("ui") == "Not Allowed":
        next_actions.append("UI is blocked. Ensure both FRS and wireframe gates reach Pass.")
    if not outputs["wireframe.md"] and outputs["frs.md"]:
        next_actions.append("Create wireframe.md from the FRS.")
    if not outputs["ui.html"] and outputs["wireframe.md"]:
        next_actions.append("Create ui.html from the wireframe and FRS.")
    if not outputs["review-notes.md"]:
        next_actions.append("Run validators and capture review-notes.md.")
    if not next_actions:
        next_actions.append("All outputs complete. Review for final approval.")

    return "\n".join(
        [
            "# Requirement Flow",
            "",
            "## Requirement Overview",
            f"- Project Name: {project_name}",
            f"- Requirement ID: {requirement_id_text}",
            f"- Requirement Name: {requirement_name}",
            f"- Input File Path: {input_file_display}",
            f"- Last Updated: {last_updated}",
            f"- Current Status: {requirement_status}",
            "",
            "## High-Level Requirement Flow",
            "",
            "```mermaid",
            "flowchart LR",
            f"    A[{requirement_id_text} | {input_file.name}] --> B[BA Agent]",
            "    B --> C[FRS + Feature List]",
            "    C --> D[UXUI Agent]",
            "    D --> E[Wireframe]",
            "    E --> F[FE Agent]",
            "    F --> G[ui.html]",
            "    G --> H[Reviewer]",
            "    H --> I[review-notes.md]",
            "```",
            "",
            "## Output Status",
            "",
            "| Output File | Status |",
            "|-------------|--------|",
            *output_rows,
            "",
            "## Traceability",
            "",
            "```mermaid",
            "flowchart LR",
            f"    REQ[{input_file.name}] --> CLAR[{_trace_node('clarification.md', outputs['clarification.md'], is_blocked, gate_results.get('clarification', ''))}]",
            f"    CLAR --> BPMN[{_trace_node('process-bpmn.md', outputs['process-bpmn.md'], is_blocked, gate_results.get('process-bpmn', ''))}]",
            f"    BPMN --> STORY[{_trace_node('user-story.md', outputs['user-story.md'], is_blocked, gate_results.get('user-story', ''))}]",
            f"    STORY --> AC[{_trace_node('acceptance-criteria.md', outputs['acceptance-criteria.md'], is_blocked, gate_results.get('acceptance-criteria', ''))}]",
            f"    AC --> BRD[{_trace_node('brd.md', outputs['brd.md'], is_blocked, gate_results.get('brd', ''))}]",
            f"    BRD --> FRS[{_trace_node('frs.md', outputs['frs.md'], is_blocked, gate_results.get('frs', ''))}]",
            f"    FRS --> FEATURE[{_trace_node('feature-list.md', outputs['feature-list.md'], is_blocked, gate_results.get('feature-list', ''))}]",
            f"    FEATURE --> WIRE[{_trace_node('wireframe.md', outputs['wireframe.md'], is_blocked, gate_results.get('wireframe', ''))}]",
            f"    WIRE --> UI[{_trace_node('ui.html', outputs['ui.html'], is_blocked, gate_results.get('ui', ''))}]",
            f"    UI --> REVIEW[{_trace_node('review-notes.md', outputs['review-notes.md'], is_blocked, gate_results.get('review', ''))}]",
            "```",
            "",
            "_Legend: ✅ done, ❌ missing, ⛔ blocked. Gate result shown in [] when available._",
            "",
            "## Next Actions",
            "",
            *[f"- {action}" for action in next_actions],
            "",
        ]
    ).rstrip() + "\n"


def write_requirement_flow(
    project_dir: Path,
    requirement_name: str,
    input_file: Path,
    requirement_id: str | None = None,
) -> Path:
    output_dir = _PATHS.requirement_output_dir(project_dir, requirement_name)
    output_dir.mkdir(parents=True, exist_ok=True)
    flow_path = output_dir / "requirement-flow.md"
    flow_path.write_text(
        build_requirement_flow(project_dir, requirement_name, input_file, requirement_id),
        encoding="utf-8",
    )
    return flow_path
    try:
        input_file_display = str(input_file.relative_to(project_dir))
    except ValueError:
        input_file_display = input_file.name
