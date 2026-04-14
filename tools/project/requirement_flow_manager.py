from __future__ import annotations

from datetime import date
from pathlib import Path


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


def _trace_node(label: str, exists: bool, blocked: bool) -> str:
    if exists:
        return f"✅ {label}"
    if blocked:
        return f"⛔ {label}"
    return f"❌ {label}"


def build_requirement_flow(
    project_dir: Path,
    requirement_name: str,
    input_file: Path,
    requirement_id: str | None = None,
) -> str:
    status_lines = _read_text(project_dir / "status.md").splitlines()
    project_name = _line_value(status_lines, "- Project Name:") or project_dir.name
    last_updated = _line_value(status_lines, "- Last Updated:") or _today()
    requirement_status = _requirement_status(status_lines, requirement_name)
    requirement_id_text = requirement_id or requirement_name.upper()
    is_blocked = requirement_status.lower() == "blocked"

    output_dir = project_dir / "outputs" / "generated" / requirement_name
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

    output_rows = [
        f"| clarification.md | {_status_symbol(output_dir / 'clarification.md', is_blocked)} |",
        f"| process-bpmn.md | {_status_symbol(output_dir / 'process-bpmn.md', is_blocked)} |",
        f"| user-story.md | {_status_symbol(output_dir / 'user-story.md', is_blocked)} |",
        f"| acceptance-criteria.md | {_status_symbol(output_dir / 'acceptance-criteria.md', is_blocked)} |",
        f"| brd.md | {_status_symbol(output_dir / 'brd.md', is_blocked)} |",
        f"| frs.md | {_status_symbol(output_dir / 'frs.md', is_blocked)} |",
        f"| feature-list.md | {_status_symbol(output_dir / 'feature-list.md', is_blocked)} |",
        f"| wireframe.md | {_status_symbol(output_dir / 'wireframe.md', is_blocked)} |",
        f"| ui.html | {_status_symbol(output_dir / 'ui.html', is_blocked)} |",
        f"| review-notes.md | {_status_symbol(output_dir / 'review-notes.md', is_blocked)} |",
    ]

    next_actions: list[str] = []
    if is_blocked:
        next_actions.append("Unblock the requirement by resolving the blocker in status.md.")
    if not outputs["clarification.md"]:
        next_actions.append("Complete clarification.md before drafting downstream outputs.")
    if not outputs["frs.md"]:
        next_actions.append("Complete frs.md to unlock UXUI and FE work.")
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
            f"- Input File Path: {input_file}",
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
            f"    REQ[{input_file.name}] --> CLAR[{_trace_node('clarification.md', outputs['clarification.md'], is_blocked)}]",
            f"    CLAR --> BPMN[{_trace_node('process-bpmn.md', outputs['process-bpmn.md'], is_blocked)}]",
            f"    BPMN --> STORY[{_trace_node('user-story.md', outputs['user-story.md'], is_blocked)}]",
            f"    STORY --> AC[{_trace_node('acceptance-criteria.md', outputs['acceptance-criteria.md'], is_blocked)}]",
            f"    AC --> BRD[{_trace_node('brd.md', outputs['brd.md'], is_blocked)}]",
            f"    BRD --> FRS[{_trace_node('frs.md', outputs['frs.md'], is_blocked)}]",
            f"    FRS --> FEATURE[{_trace_node('feature-list.md', outputs['feature-list.md'], is_blocked)}]",
            f"    FEATURE --> WIRE[{_trace_node('wireframe.md', outputs['wireframe.md'], is_blocked)}]",
            f"    WIRE --> UI[{_trace_node('ui.html', outputs['ui.html'], is_blocked)}]",
            f"    UI --> REVIEW[{_trace_node('review-notes.md', outputs['review-notes.md'], is_blocked)}]",
            "```",
            "",
            "_Legend: ✅ done, ❌ missing, ⛔ blocked_",
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
    output_dir = project_dir / "outputs" / "generated" / requirement_name
    output_dir.mkdir(parents=True, exist_ok=True)
    flow_path = output_dir / "requirement-flow.md"
    flow_path.write_text(
        build_requirement_flow(project_dir, requirement_name, input_file, requirement_id),
        encoding="utf-8",
    )
    return flow_path
