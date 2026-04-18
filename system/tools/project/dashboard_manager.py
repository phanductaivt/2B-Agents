from __future__ import annotations

from datetime import date
import importlib.util
from pathlib import Path
import sys

try:
    import yaml
except ImportError:
    yaml = None


def _load_module(module_name: str, file_path: Path):
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Could not load module: {file_path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


_CONSOLE_LOGGER = _load_module(
    "console_logger_for_dashboard_manager",
    Path(__file__).resolve().parents[1] / "logging" / "console_logger.py",
)
_PATHS = _load_module(
    "project_paths_for_dashboard_manager",
    Path(__file__).resolve().parent / "project_paths.py",
)
_SEMANTICS = _load_module(
    "semantic_mapper_for_dashboard_manager",
    Path(__file__).resolve().parent / "semantic_mapper.py",
)
_SUMMARY = _load_module(
    "summary_reader_for_dashboard_manager",
    Path(__file__).resolve().parent / "summary_reader.py",
)


def _today() -> str:
    return date.today().isoformat()


def _read_text(path: Path) -> str:
    return _SUMMARY.read_text(path)


def _line_value(lines: list[str], prefix: str) -> str:
    return _SUMMARY.line_value(lines, [prefix])


def _collect_section(lines: list[str], header: str) -> list[str]:
    return _SUMMARY.collect_section(lines, header)


def _parse_requirements(lines: list[str]) -> list[tuple[str, str]]:
    parsed = _SUMMARY.parse_requirements_table(lines)
    return [(row.get("requirement_name", ""), row.get("current_status", "")) for row in parsed if row.get("requirement_name")]


def _display_requirement_status(raw_status: str, project_status: str) -> str:
    return _SEMANTICS.normalize_requirement_display_status(raw_status, project_status)


def _build_execution_model(project_dir: Path, blockers: list[str]) -> dict[str, object]:
    artifact_rows = _SUMMARY.gather_artifact_rows(project_dir, _PATHS)
    gate_rows = _SUMMARY.gather_gate_rows(project_dir, _PATHS)

    confirmation = _confirmation_items(project_dir)
    confirmation_blockers = _SEMANTICS.parse_confirmation_blockers(confirmation)
    return _SEMANTICS.execution_snapshot(
        artifact_rows=artifact_rows,
        gate_rows=gate_rows,
        project_blockers=blockers,
        confirmation_blockers=confirmation_blockers,
    )


def _build_project_summary_model(
    project_dir: Path,
    status_lines: list[str],
    requirements: list[tuple[str, str]],
    blockers: list[str],
    execution: dict[str, object],
) -> dict[str, object]:
    project_phase = (
        _line_value(status_lines, "- Project Phase:")
        or _line_value(status_lines, "- Current Stage:")
        or "Draft"
    )
    project_owner = (
        _line_value(status_lines, "- Project Owner:")
        or _line_value(status_lines, "- Owner:")
        or "BA Team"
    )
    last_update = _line_value(status_lines, "- Last Updated:") or _today()
    overall_progress = _line_value(status_lines, "- Overall Progress:") or "Not Started"

    total_requirements = len(requirements)
    done_requirements = sum(1 for _, status in requirements if status.lower() == "done")
    project_status, project_progress = _SEMANTICS.project_status_and_readiness(
        requirement_statuses=[status for _, status in requirements],
        blockers=blockers,
        project_phase=project_phase,
        overall_progress_text=overall_progress,
    )

    return {
        "project_name": _line_value(status_lines, "- Project Name:") or project_dir.name,
        "project_phase": project_phase,
        "project_owner": project_owner,
        "project_status": project_status,
        "project_progress": project_progress,
        "last_update": last_update,
        "requirement_count": total_requirements,
        "done_requirement_count": done_requirements,
        "overall_progress_text": overall_progress,
        "execution_model": execution,
    }


def _confirmation_items(project_dir: Path) -> list[dict[str, object]]:
    return _SUMMARY.load_confirmation_items(project_dir, _PATHS, yaml)


def _confirmation_summary(project_dir: Path) -> dict[str, int]:
    return _SUMMARY.confirmation_summary(_confirmation_items(project_dir))


def discover_projects(projects_dir: Path) -> list[Path]:
    projects: list[Path] = []
    for entry in sorted(projects_dir.iterdir()):
        if not entry.is_dir():
            continue
        if entry.name.startswith(".") or entry.name == "project-template":
            continue
        if (entry / "project-config.yaml").exists():
            projects.append(entry)
    return projects


def build_dashboard(projects_dir: Path) -> str:
    project_rows: list[str] = []
    detailed_sections: list[str] = []
    blocker_sections: list[str] = []

    total = 0
    active = 0
    blocked = 0
    completed = 0

    for project_dir in discover_projects(projects_dir):
        total += 1
        status_path = _PATHS.status_path(project_dir)
        status_lines = _read_text(status_path).splitlines()
        requirements = _parse_requirements(status_lines)
        blockers = _collect_section(status_lines, "## Current Blockers")
        execution = _build_execution_model(project_dir, blockers)
        summary = _build_project_summary_model(
            project_dir=project_dir,
            status_lines=status_lines,
            requirements=requirements,
            blockers=blockers,
            execution=execution,
        )
        project_name = str(summary["project_name"])
        project_phase = str(summary["project_phase"])
        project_owner = str(summary["project_owner"])
        project_status = str(summary["project_status"])
        project_progress = int(summary["project_progress"])
        last_updated = str(summary["last_update"])
        requirement_count = int(summary["requirement_count"])
        execution_stage = str(execution.get("current_execution_stage", "Not Started"))
        execution_owner = str(execution.get("current_execution_owner", "-"))
        artifact_completion_rate = int(execution.get("artifact_completion_rate", 0))
        gate_summary = str(execution.get("gate_summary", "No gate data"))
        artifact_statuses = str(execution.get("current_artifact_statuses", "No artifact data"))
        blocked_reason = str(execution.get("blocked_reason", "No blocker reason recorded."))
        confirmation = _confirmation_summary(project_dir)

        if project_status == "Blocked":
            blocked += 1
        elif project_status == "Done":
            completed += 1
        else:
            active += 1

        status_icon = "🟡"
        if project_status == "Done":
            status_icon = "🟢"
        if project_status == "Blocked":
            status_icon = "🔴"

        project_rows.append(
            "| "
            + " | ".join(
                [
                    project_name,
                    project_phase,
                    f"{project_progress}%",
                    project_owner,
                    f"{status_icon} {project_status}",
                    f"[Open](../projects/{project_dir.name}/)",
                ]
            )
            + " |"
        )

        display_done_count = 0
        requirement_lines = []
        for name, status in requirements:
            display_status = _display_requirement_status(status, project_status)
            if display_status in {"Processed", "Approved"}:
                display_done_count += 1
            requirement_lines.append(f"  - {name}: {display_status}")
        if not requirement_lines:
            requirement_lines = ["  - No requirements tracked yet"]
        requirement_summary_label = "approved" if project_status == "Done" else "processed"

        risk_lines = _collect_section(status_lines, "## Current Risks") or ["Risk list not started"]
        blocker_lines = blockers or ["No blockers listed"]
        action_lines = _collect_section(status_lines, "## Next Actions") or ["No next actions listed"]

        if blockers:
            blocker_sections.extend(
                [
                    f"### {project_name}",
                    *[f"- {blocker}" for blocker in blockers],
                    "",
                ]
            )

        detailed_sections.extend(
            [
                f"## Project: {project_name}",
                "",
                "### Project Summary",
                f"- Project Phase: {project_phase}",
                f"- Project Owner: {project_owner}",
                f"- Project Status: {project_status}",
                f"- Project Readiness: {project_progress}%",
                f"- Last Update: {last_updated}",
                "",
                "### Execution Snapshot",
                f"- Current Execution Stage: {execution_stage}",
                f"- Current Execution Owner: {execution_owner}",
                f"- Artifact Completion Rate: {artifact_completion_rate}%",
                f"- Gate Summary: {gate_summary}",
                f"- Current Artifact Statuses: {artifact_statuses}",
                f"- Pending Confirmations: {confirmation['pending']} (needs-more-info: {confirmation['needs_more_info']})",
                f"- Blocked Reason: {blocked_reason if project_status == 'Blocked' else 'N/A'}",
                "",
                "### Requirement Summary",
                f"- Requirements: {display_done_count}/{requirement_count} {requirement_summary_label}",
                "- Requirements:",
                *requirement_lines,
                "- Current Risks:",
                *[f"  - {risk}" for risk in risk_lines],
                "- Current Blockers:",
                *[f"  - {blocker}" for blocker in blocker_lines],
                "- Next Actions:",
                *[f"  - {action}" for action in action_lines],
                "- Quick Links:",
                f"  - [Project README](../projects/{project_dir.name}/README.md)",
                f"  - [Status](../projects/{project_dir.name}/_ops/status.md)",
                f"  - [Decision Log](../projects/{project_dir.name}/_ops/decision-log.md)",
                f"  - [Task Tracker](../projects/{project_dir.name}/_ops/task-tracker.md)",
                f"  - [Outputs](../projects/{project_dir.name}/02-output/)",
                "",
            ]
        )

    dashboard_lines = [
        "# Project Dashboard (Visual)",
        "",
        "## 1. Overview Summary",
        f"- Total Projects: {total}",
        f"- Active: {active}",
        f"- Blocked: {blocked}",
        f"- Done: {completed}",
        "",
        "## 2. Status Highlight Table",
        "",
        "| Project | Project Phase | Project Readiness | Project Owner | Project Status | Link |",
        "|--------|---------------|------------------|---------------|----------------|------|",
        *project_rows,
        "",
        "## 3. Status Breakdown (Pie)",
        "",
        "```mermaid",
        "pie title Project Status",
        f"    \"Active\" : {active}",
        f"    \"Blocked\" : {blocked}",
        f"    \"Done\" : {completed}",
        "```",
        "",
        "## 4. Project Pipeline View",
        "",
        "```mermaid",
        "flowchart LR",
        "    A[Input] --> B[BA Agent]",
        "    B --> C[FRS + Feature]",
        "    C --> D[UXUI Agent]",
        "    D --> E[Wireframe]",
        "    E --> F[FE Agent]",
        "    F --> G[HTML Output]",
        "```",
        "",
        "## 5. Blockers (All Projects)",
        "",
        *(
            blocker_sections
            if blocker_sections
            else ["- No blockers listed in any project.", ""]
        ),
        *detailed_sections,
    ]

    return "\n".join(dashboard_lines).rstrip() + "\n"


def build_dashboard_html(projects_dir: Path) -> str:
    rows = []
    cards = []
    blocked_cards = []
    last_updated = _today()

    total = 0
    active = 0
    blocked = 0
    done = 0

    for project_dir in discover_projects(projects_dir):
        total += 1
        status_path = _PATHS.status_path(project_dir)
        status_lines = _read_text(status_path).splitlines()
        requirements = _parse_requirements(status_lines)
        blockers = _collect_section(status_lines, "## Current Blockers")
        execution = _build_execution_model(project_dir, blockers)
        summary = _build_project_summary_model(
            project_dir=project_dir,
            status_lines=status_lines,
            requirements=requirements,
            blockers=blockers,
            execution=execution,
        )
        project_name = str(summary["project_name"])
        project_phase = str(summary["project_phase"])
        project_owner = str(summary["project_owner"])
        project_status = str(summary["project_status"])
        project_progress = int(summary["project_progress"])
        last_updated = str(summary["last_update"])
        execution_stage = str(execution.get("current_execution_stage", "Not Started"))
        execution_owner = str(execution.get("current_execution_owner", "-"))
        artifact_completion_rate = int(execution.get("artifact_completion_rate", 0))
        gate_summary = str(execution.get("gate_summary", "No gate data"))
        blocked_reason = str(execution.get("blocked_reason", "No blocker reason recorded."))
        confirmation = _confirmation_summary(project_dir)

        status_class = "active"
        if project_status == "Blocked":
            status_class = "blocked"
            blocked += 1
        elif project_status == "Done":
            status_class = "done"
            done += 1
        else:
            active += 1

        rows.append(
            "\n".join(
                [
                    f"<tr class=\"data-row\" data-status=\"{project_status.lower()}\" data-name=\"{project_name.lower()}\">",
                    f"<td class=\"project-name\">{project_name}</td>",
                    f"<td>{project_phase}</td>",
                    "<td>",
                    "<div class=\"progress-wrap\">",
                    f"<span class=\"progress-label\">{project_progress}%</span>",
                    f"<div class=\"progress-bar {status_class}\">",
                    f"<div class=\"progress-fill\" style=\"width:{project_progress}%\"></div>",
                    "</div>",
                    "</div>",
                    "</td>",
                    f"<td>{project_owner}</td>",
                    f"<td><span class=\"badge {status_class}\">{project_status}</span></td>",
                    f"<td>{last_updated}</td>",
                    f"<td><a href=\"../projects/{project_dir.name}/\">Open</a></td>",
                    "</tr>",
                ]
            )
        )

        blocker_html = ""
        if blockers:
            blocker_items = "".join(f"<li>{blocker}</li>" for blocker in blockers)
            blocker_html = f"<ul>{blocker_items}</ul>"

        card = "\n".join(
            [
                f"<div class=\"card\" data-status=\"{project_status.lower()}\" data-name=\"{project_name.lower()}\">",
                "<div class=\"card-header\">",
                f"<h3>{project_name}</h3>",
                f"<span class=\"badge {status_class}\">{project_status}</span>",
                "</div>",
                "<h4 class=\"card-subtitle\">Project Summary</h4>",
                f"<p class=\"muted\">Project Phase: {project_phase}</p>",
                f"<p class=\"muted\">Project Owner: {project_owner}</p>",
                "<div class=\"progress-wrap\">",
                f"<span class=\"progress-label\">{project_progress}%</span>",
                f"<div class=\"progress-bar {status_class}\">",
                f"<div class=\"progress-fill\" style=\"width:{project_progress}%\"></div>",
                "</div>",
                "</div>",
                f"<p class=\"muted\">Project Readiness (Milestones): {project_progress}%</p>",
                "<h4 class=\"card-subtitle\">Execution Snapshot</h4>",
                f"<p class=\"muted\">Current Execution Stage: {execution_stage}</p>",
                f"<p class=\"muted\">Current Execution Owner: {execution_owner}</p>",
                "<div class=\"progress-wrap\">",
                f"<span class=\"progress-label\">{artifact_completion_rate}%</span>",
                f"<div class=\"progress-bar {status_class}\">",
                f"<div class=\"progress-fill\" style=\"width:{artifact_completion_rate}%\"></div>",
                "</div>",
                "</div>",
                f"<p class=\"muted\">Artifact Completion Rate: {artifact_completion_rate}%</p>",
                f"<p class=\"muted\">Gate Summary: {gate_summary}</p>",
                f"<p class=\"muted\">Pending Confirmations: {confirmation['pending']} (needs-more-info: {confirmation['needs_more_info']})</p>",
                (
                    f"<p class=\"muted\">Blocked Reason: {blocked_reason}</p>"
                    if project_status == "Blocked"
                    else "<p class=\"muted\">Blocked Reason: N/A</p>"
                ),
                blocker_html if blocker_html else "<p class=\"muted\">No blockers listed.</p>",
                "<div class=\"card-links\">",
                f"<a href=\"../projects/{project_dir.name}/\">Project Folder</a>",
                f"<a href=\"../projects/{project_dir.name}/_ops/status.md\">Status</a>",
                f"<a href=\"../projects/{project_dir.name}/02-output/\">Outputs</a>",
                "</div>",
                "</div>",
            ]
        )
        cards.append(card)

        if project_status == "Blocked":
            blocked_cards.append(
                "\n".join(
                    [
                        "<div class=\"blocked-card\">",
                        f"<strong>{project_name}</strong> — Project Phase: {project_phase}",
                        blocker_html if blocker_html else "<p>No blocker details.</p>",
                        f"<p><a href=\"../projects/{project_dir.name}/\">Open project</a></p>",
                        "</div>",
                    ]
                )
            )

    return "\n".join(
        [
            "<!DOCTYPE html>",
            "<html>",
            "<head>",
            "<meta charset=\"utf-8\" />",
            "<title>Project Dashboard</title>",
            "<style>",
            "body { font-family: Arial, sans-serif; margin: 0; background: #f6f7f9; color: #1f2933; }",
            ".page { max-width: 1100px; margin: 0 auto; padding: 24px; }",
            "header { display: flex; flex-direction: column; gap: 6px; margin-bottom: 18px; }",
            "header h1 { margin: 0; font-size: 28px; }",
            "header p { margin: 0; color: #52606d; }",
            ".top-links { display: flex; gap: 12px; margin-top: 8px; }",
            ".top-links a { color: #0b6efd; text-decoration: none; }",
            ".summary { display: grid; grid-template-columns: repeat(auto-fit, minmax(160px, 1fr)); gap: 12px; margin: 20px 0; }",
            ".summary .tile { background: white; border: 1px solid #e5e7eb; padding: 12px; border-radius: 8px; }",
            ".tile .label { color: #6b7280; font-size: 12px; text-transform: uppercase; }",
            ".tile .value { font-size: 22px; font-weight: bold; }",
            ".filter-bar { display: flex; flex-wrap: wrap; gap: 8px; margin: 12px 0 20px; }",
            ".filter-bar button { border: 1px solid #d1d5db; background: white; padding: 6px 12px; border-radius: 6px; cursor: pointer; }",
            ".filter-bar button.active { background: #0b6efd; color: white; border-color: #0b6efd; }",
            ".filter-bar input { padding: 6px 10px; border: 1px solid #d1d5db; border-radius: 6px; }",
            "table { border-collapse: collapse; width: 100%; margin-bottom: 20px; background: white; }",
            "th, td { padding: 10px; text-align: left; border-bottom: 1px solid #e5e7eb; }",
            "thead th { position: sticky; top: 0; background: #f3f4f6; }",
            "tbody tr:nth-child(even) { background: #fafafa; }",
            "tbody tr:hover { background: #f0f9ff; }",
            ".badge { padding: 2px 8px; border-radius: 999px; font-size: 12px; font-weight: bold; }",
            ".badge.active { background: #fff7ed; color: #b45309; }",
            ".badge.blocked { background: #fee2e2; color: #b91c1c; }",
            ".badge.done { background: #dcfce7; color: #15803d; }",
            ".progress-wrap { display: flex; align-items: center; gap: 8px; }",
            ".progress-label { font-size: 12px; color: #6b7280; min-width: 36px; }",
            ".progress-bar { background: #e5e7eb; height: 8px; border-radius: 999px; overflow: hidden; width: 100%; }",
            ".progress-bar.active .progress-fill { background: #f59e0b; }",
            ".progress-bar.blocked .progress-fill { background: #ef4444; }",
            ".progress-bar.done .progress-fill { background: #22c55e; }",
            ".progress-fill { height: 8px; }",
            ".cards { display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 12px; }",
            ".card { background: white; border: 1px solid #e5e7eb; padding: 14px; border-radius: 10px; }",
            ".card-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px; }",
            ".card-subtitle { margin: 10px 0 6px; font-size: 13px; color: #374151; text-transform: uppercase; letter-spacing: 0.02em; }",
            ".card-links { display: flex; gap: 10px; margin-top: 8px; }",
            ".card-links a { color: #0b6efd; text-decoration: none; font-size: 12px; }",
            ".muted { color: #6b7280; font-size: 12px; }",
            ".blocked-list { background: white; border: 1px solid #e5e7eb; border-radius: 8px; padding: 12px; }",
            ".blocked-card { border-bottom: 1px dashed #e5e7eb; padding: 8px 0; }",
            ".blocked-card:last-child { border-bottom: none; }",
            "@media (prefers-color-scheme: dark) {",
            "  body { background: #0b0f14; color: #e5e7eb; }",
            "  .tile, table, .card, .blocked-list { background: #111827; border-color: #1f2937; }",
            "  thead th { background: #1f2937; }",
            "  tbody tr:nth-child(even) { background: #0f172a; }",
            "  tbody tr:hover { background: #1f2937; }",
            "  header p, .muted, .progress-label { color: #9ca3af; }",
            "  .card-subtitle { color: #cbd5e1; }",
            "  .filter-bar button { background: #111827; color: #e5e7eb; border-color: #374151; }",
            "  .filter-bar button.active { background: #2563eb; border-color: #2563eb; }",
            "  .filter-bar input { background: #111827; color: #e5e7eb; border-color: #374151; }",
            "}",
            "</style>",
            "</head>",
            "<body>",
            "<div class=\"page\">",
            "<header>",
            "<h1>Project Dashboard</h1>",
            "<p>Manage all BA and delivery projects in one place.</p>",
            f"<p class=\"muted\">Last updated: {last_updated}</p>",
            "<div class=\"top-links\">",
            "<a href=\"../projects/\">Open projects folder</a>",
            "<a href=\"./dashboard.md\">Open dashboard.md</a>",
            "<span class=\"muted\">Refresh by running: python3 app.py</span>",
            "</div>",
            "</header>",
            "<section class=\"summary\">",
            f"<div class=\"tile\"><div class=\"label\">Total Projects</div><div class=\"value\">{total}</div></div>",
            f"<div class=\"tile\"><div class=\"label\">Active Projects</div><div class=\"value\">{active}</div></div>",
            f"<div class=\"tile\"><div class=\"label\">Blocked Projects</div><div class=\"value\">{blocked}</div></div>",
            f"<div class=\"tile\"><div class=\"label\">Done Projects</div><div class=\"value\">{done}</div></div>",
            "</section>",
            "<section class=\"filter-bar\">",
            "<button class=\"active\" data-filter=\"all\">All</button>",
            "<button data-filter=\"active\">Active</button>",
            "<button data-filter=\"blocked\">Blocked</button>",
            "<button data-filter=\"done\">Done</button>",
            "<input type=\"search\" id=\"search\" placeholder=\"Search project name\" />",
            "</section>",
            "<section>",
            "<table>",
            "<thead><tr><th>Project</th><th>Project Phase</th><th>Project Readiness</th><th>Project Owner</th><th>Project Status</th><th>Last Update</th><th>Link</th></tr></thead>",
            "<tbody>",
            *rows,
            "</tbody>",
            "</table>",
            "</section>",
            "<section>",
            "<h2>Project Cards</h2>",
            "<div class=\"cards\">",
            *cards,
            "</div>",
            "</section>",
            "<section>",
            "<h2>Blocked Projects</h2>",
            "<div class=\"blocked-list\">",
            *(
                blocked_cards
                if blocked_cards
                else ["<p class=\"muted\">No blocked projects.</p>"]
            ),
            "</div>",
            "</section>",
            "</div>",
            "<script>",
            "const buttons = document.querySelectorAll('.filter-bar button');",
            "const rows = document.querySelectorAll('tr.data-row');",
            "const cards = document.querySelectorAll('.card');",
            "const search = document.getElementById('search');",
            "function applyFilter(filter, term) {",
            "  const query = term ? term.toLowerCase() : '';",
            "  rows.forEach(row => {",
            "    const status = row.dataset.status;",
            "    const name = row.dataset.name || '';",
            "    const matchesFilter = filter === 'all' || status === filter;",
            "    const matchesSearch = !query || name.includes(query);",
            "    row.style.display = matchesFilter && matchesSearch ? '' : 'none';",
            "  });",
            "  cards.forEach(card => {",
            "    const status = card.dataset.status;",
            "    const name = card.dataset.name || '';",
            "    const matchesFilter = filter === 'all' || status === filter;",
            "    const matchesSearch = !query || name.includes(query);",
            "    card.style.display = matchesFilter && matchesSearch ? '' : 'none';",
            "  });",
            "}",
            "buttons.forEach(button => {",
            "  button.addEventListener('click', () => {",
            "    buttons.forEach(btn => btn.classList.remove('active'));",
            "    button.classList.add('active');",
            "    applyFilter(button.dataset.filter, search.value);",
            "  });",
            "});",
            "search.addEventListener('input', () => {",
            "  const activeButton = document.querySelector('.filter-bar button.active');",
            "  const filter = activeButton ? activeButton.dataset.filter : 'all';",
            "  applyFilter(filter, search.value);",
            "});",
            "</script>",
            "</body>",
            "</html>",
        ]
    )


def write_dashboard(projects_dir: Path, workspace_dir: Path) -> Path:
    workspace_dir.mkdir(parents=True, exist_ok=True)
    dashboard_path = workspace_dir / "dashboard.md"
    dashboard_path.write_text(build_dashboard(projects_dir), encoding="utf-8")
    return dashboard_path


def write_dashboard_html(projects_dir: Path, workspace_dir: Path) -> Path:
    workspace_dir.mkdir(parents=True, exist_ok=True)
    dashboard_path = workspace_dir / "dashboard.html"
    dashboard_path.write_text(build_dashboard_html(projects_dir), encoding="utf-8")
    return dashboard_path


def main() -> None:
    base_dir = Path(__file__).resolve().parents[3]
    projects_dir = base_dir / "projects"
    workspace_dir = base_dir / "workspace"
    _CONSOLE_LOGGER.section("Dashboard Refresh")
    _CONSOLE_LOGGER.step("DASHBOARD", f"Scanning projects in {projects_dir}")
    dashboard_path = write_dashboard(projects_dir, workspace_dir)
    _CONSOLE_LOGGER.step("DASHBOARD", "Generating HTML dashboard")
    html_path = write_dashboard_html(projects_dir, workspace_dir)
    _CONSOLE_LOGGER.success(f"Dashboard updated: {dashboard_path}")
    _CONSOLE_LOGGER.success(f"HTML dashboard generated: {html_path}")


if __name__ == "__main__":
    # TODO: Add optional filters for stages or owners.
    main()
