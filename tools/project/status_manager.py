from __future__ import annotations

from datetime import date
from pathlib import Path


def _today() -> str:
    return date.today().isoformat()


def _status_cell(value: bool) -> str:
    return "✅" if value else "❌"


def _build_template(project_name: str, owner: str) -> str:
    return "\n".join(
        [
            "# Project Status",
            "",
            "## Project Overview",
            f"- Project Name: {project_name}",
            f"- Owner: {owner}",
            "- Current Stage: Analysis",
            f"- Last Updated: {_today()}",
            "- Overall Progress: In Progress",
            "",
            "## Requirement Status Table",
            "",
            "| Requirement | Current Status | BA | UXUI | FE | Reviewer | Notes |",
            "|------------|----------------|----|------|----|----------|------|",
            "| req-001 | Not Started | ❌ | ❌ | ❌ | ❌ | Add notes here |",
            "",
            "## Current Risks",
            "- Risk 1",
            "- Risk 2",
            "",
            "## Current Blockers",
            "- Blocker 1",
            "- Blocker 2",
            "",
            "## Next Actions",
            "- Action 1",
            "- Action 2",
            "",
        ]
    )


def ensure_status_file(project_dir: str | Path, project_name: str, owner: str) -> Path:
    status_path = Path(project_dir) / "status.md"
    if status_path.exists():
        return status_path
    status_path.write_text(_build_template(project_name, owner), encoding="utf-8")
    return status_path


def update_project_status(
    project_dir: str | Path,
    project_name: str,
    owner: str,
    requirement_name: str,
    ba_done: bool,
    uxui_done: bool,
    fe_done: bool,
    reviewer_done: bool,
    notes: str = "",
) -> None:
    status_path = ensure_status_file(project_dir, project_name, owner)
    status_text = status_path.read_text(encoding="utf-8")
    lines = status_text.splitlines()

    def set_overview_line(prefix: str, value: str) -> None:
        for index, line in enumerate(lines):
            if line.startswith(prefix):
                current_value = line.split(":", 1)[1].strip()
                if current_value:
                    return
                lines[index] = f"{prefix} {value}"
                return

    set_overview_line("- Project Name:", project_name)
    set_overview_line("- Owner:", owner)
    set_overview_line("- Current Stage:", "Analysis")
    for index, line in enumerate(lines):
        if line.startswith("- Last Updated:"):
            lines[index] = f"- Last Updated: {_today()}"
            break

    current_status = "Not Started"
    if any([ba_done, uxui_done, fe_done, reviewer_done]):
        current_status = "In Progress"
    if all([ba_done, uxui_done, fe_done, reviewer_done]):
        current_status = "Done"

    ba_cell = _status_cell(ba_done)
    uxui_cell = _status_cell(uxui_done)
    fe_cell = _status_cell(fe_done)
    reviewer_cell = _status_cell(reviewer_done)
    notes_cell = notes or "Updated by app.py"

    table_header_index = None
    for index, line in enumerate(lines):
        if line.strip() == "| Requirement | Current Status | BA | UXUI | FE | Reviewer | Notes |":
            table_header_index = index
            break

    if table_header_index is None:
        lines = _build_template(project_name, owner).splitlines()
        table_header_index = None
        for index, line in enumerate(lines):
            if line.strip() == "| Requirement | Current Status | BA | UXUI | FE | Reviewer | Notes |":
                table_header_index = index
                break
        if table_header_index is None:
            status_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
            return

    table_start = table_header_index + 2
    table_end = table_start
    while table_end < len(lines):
        if not lines[table_end].startswith("|"):
            break
        table_end += 1

    updated_row = (
        f"| {requirement_name} | {current_status} | {ba_cell} | {uxui_cell} | "
        f"{fe_cell} | {reviewer_cell} | {notes_cell} |"
    )

    for index in range(table_start, table_end):
        row = lines[index]
        columns = [col.strip() for col in row.strip("|").split("|")]
        if columns and columns[0] == requirement_name:
            lines[index] = updated_row
            status_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
            return

    lines.insert(table_end, updated_row)
    status_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
