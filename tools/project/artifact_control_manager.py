from __future__ import annotations

from datetime import date
from pathlib import Path
import re


ARTIFACT_SEQUENCE = [
    "clarification.md",
    "process-bpmn.md",
    "user-story.md",
    "acceptance-criteria.md",
    "brd.md",
    "frs.md",
    "feature-list.md",
    "wireframe.md",
    "ui.html",
    "review-notes.md",
    "test-cases.md",
]


ARTIFACT_PURPOSE = {
    "clarification.md": "Clarify the requirement and list assumptions/questions.",
    "process-bpmn.md": "Show business flow in Mermaid.",
    "user-story.md": "Describe user value and scope in story format.",
    "acceptance-criteria.md": "Define testable acceptance conditions.",
    "brd.md": "Document business goals, scope, and rules.",
    "frs.md": "Document functional behavior, flows, and edge cases.",
    "feature-list.md": "Show hierarchical feature decomposition.",
    "wireframe.md": "Provide UX structure based on FRS/feature scope.",
    "ui.html": "Provide FE demo implementation.",
    "review-notes.md": "Record quality review issues and next actions.",
    "test-cases.md": "Provide test scenarios linked to AC/US/FR.",
}


ARTIFACT_DEPENDENCIES = {
    "clarification.md": [],
    "process-bpmn.md": ["clarification.md"],
    "user-story.md": ["clarification.md"],
    "acceptance-criteria.md": ["user-story.md"],
    "brd.md": ["clarification.md"],
    "frs.md": ["brd.md", "process-bpmn.md"],
    "feature-list.md": ["frs.md"],
    "wireframe.md": ["frs.md", "feature-list.md"],
    "ui.html": ["frs.md", "wireframe.md"],
    "review-notes.md": ["frs.md", "wireframe.md", "ui.html"],
    "test-cases.md": ["frs.md", "user-story.md", "acceptance-criteria.md"],
}


def _today() -> str:
    return date.today().isoformat()


def _output_dir(project_dir: Path, requirement_name: str) -> Path:
    return project_dir / "outputs" / "generated" / requirement_name


def _status_path(project_dir: Path, requirement_name: str) -> Path:
    return _output_dir(project_dir, requirement_name) / "artifact-status.md"


def _checklist_path(project_dir: Path, requirement_name: str) -> Path:
    return _output_dir(project_dir, requirement_name) / "artifact-checklist.md"


def _normalize_artifact_name(name: str) -> str:
    name = name.strip()
    if name in ARTIFACT_SEQUENCE:
        return name
    if not name.endswith(".md") and not name.endswith(".html"):
        guess_md = f"{name}.md"
        if guess_md in ARTIFACT_SEQUENCE:
            return guess_md
    if name == "ui":
        return "ui.html"
    return name


def _default_state() -> dict[str, dict[str, str]]:
    state: dict[str, dict[str, str]] = {}
    for artifact in ARTIFACT_SEQUENCE:
        deps = ARTIFACT_DEPENDENCIES.get(artifact, [])
        state[artifact] = {
            "status": "Not Started",
            "gate": "Pending",
            "approval": "Pending",
            "dependencies": ", ".join(deps) if deps else "-",
            "notes": "-",
            "updated": "-",
        }
    return state


def _parse_status_file(path: Path) -> dict[str, dict[str, str]]:
    if not path.exists():
        return _default_state()

    state = _default_state()
    in_table = False
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip() == (
            "| Artifact | Purpose | Depends On | Status | Gate | Approval | Last Updated | Notes |"
        ):
            in_table = True
            continue
        if in_table and not line.strip().startswith("|"):
            break
        if in_table and line.strip().startswith("|"):
            columns = [col.strip() for col in line.strip().strip("|").split("|")]
            if len(columns) < 8:
                continue
            artifact = _normalize_artifact_name(columns[0])
            if artifact not in state:
                continue
            state[artifact] = {
                "status": columns[3],
                "gate": columns[4],
                "approval": columns[5],
                "dependencies": columns[2],
                "notes": columns[7],
                "updated": columns[6],
            }
    return state


def _write_status_file(
    project_dir: Path,
    requirement_name: str,
    requirement_id: str,
    state: dict[str, dict[str, str]],
) -> Path:
    output_dir = _output_dir(project_dir, requirement_name)
    output_dir.mkdir(parents=True, exist_ok=True)
    path = _status_path(project_dir, requirement_name)

    lines = [
        "# Artifact Status",
        "",
        f"- Requirement Name: {requirement_name}",
        f"- Requirement ID: {requirement_id}",
        f"- Last Updated: {_today()}",
        "",
        "## Artifact Execution Table",
        "",
        "| Artifact | Purpose | Depends On | Status | Gate | Approval | Last Updated | Notes |",
        "|---------|---------|------------|--------|------|----------|--------------|------|",
    ]

    for artifact in ARTIFACT_SEQUENCE:
        info = state[artifact]
        lines.append(
            "| "
            + " | ".join(
                [
                    artifact,
                    ARTIFACT_PURPOSE.get(artifact, "-"),
                    info.get("dependencies", "-"),
                    info.get("status", "Not Started"),
                    info.get("gate", "Pending"),
                    info.get("approval", "Pending"),
                    info.get("updated", "-"),
                    info.get("notes", "-"),
                ]
            )
            + " |"
        )

    lines.extend(
        [
            "",
            "_Status values: Not Started, In Progress, Done, Blocked_",
            "_Gate values: Pending, Pass, Fail_",
            "_Approval values: Pending, Approved, Rejected, N/A_",
            "",
            "<!-- TODO: Add simple score-based quality summary per artifact if needed. -->",
            "",
        ]
    )

    path.write_text("\n".join(lines), encoding="utf-8")
    return path


def _write_checklist_file(project_dir: Path, requirement_name: str, requirement_id: str) -> Path:
    path = _checklist_path(project_dir, requirement_name)
    if path.exists():
        return path

    lines = [
        "# Artifact Checklist",
        "",
        f"- Requirement Name: {requirement_name}",
        f"- Requirement ID: {requirement_id}",
        "",
    ]

    for artifact in ARTIFACT_SEQUENCE:
        lines.extend(
            [
                f"## {artifact}",
                f"- [ ] Purpose reviewed: {ARTIFACT_PURPOSE.get(artifact, '-')}",
                f"- [ ] Dependencies reviewed: {', '.join(ARTIFACT_DEPENDENCIES.get(artifact, [])) or 'None'}",
                "- [ ] Quality check completed",
                "- [ ] Approval decision recorded in artifact-status.md",
                "",
            ]
        )

    lines.append("<!-- TODO: Add role-based approval checklist (BA lead / reviewer) if the team needs it. -->")
    lines.append("")
    path.write_text("\n".join(lines), encoding="utf-8")
    return path


def ensure_artifact_control_files(project_dir: Path, requirement_name: str, requirement_id: str) -> list[Path]:
    state = _parse_status_file(_status_path(project_dir, requirement_name))
    status_path = _write_status_file(project_dir, requirement_name, requirement_id, state)
    checklist_path = _write_checklist_file(project_dir, requirement_name, requirement_id)
    return [status_path, checklist_path]


def _artifact_gate_result(artifact: str, content: str) -> tuple[str, str]:
    text = content.strip()
    if not text:
        return "Fail", "Generated content is empty."

    checks = {
        "clarification.md": ["## Summary", "## Known Facts", "## Open Questions"],
        "process-bpmn.md": ["```mermaid"],
        "user-story.md": ["## Story", "## INVEST Check"],
        "acceptance-criteria.md": ["## Criteria", "- "],
        "brd.md": ["## Business Goals", "## Business Rules"],
        "frs.md": ["## Main Flow", "## Alternative Flows", "## Business Rules"],
        "feature-list.md": ["## "],
        "wireframe.md": ["## Main Sections", "## Wireframe Sketch"],
        "ui.html": ["<html", "</html>"],
        "review-notes.md": ["Validation Status", "## Ambiguity Checker"],
        "test-cases.md": ["| TC ID |", "## Test Case Matrix"],
    }
    required_tokens = checks.get(artifact, [])
    missing = [token for token in required_tokens if token.lower() not in text.lower()]
    if missing:
        return "Fail", "Missing required sections: " + ", ".join(missing)
    return "Pass", "Basic artifact quality check passed."


def _dependency_gate_pass(
    state: dict[str, dict[str, str]],
    artifact: str,
    require_approval: bool = True,
) -> tuple[bool, list[str]]:
    issues: list[str] = []
    for dep in ARTIFACT_DEPENDENCIES.get(artifact, []):
        dep_state = state.get(dep, {})
        if dep_state.get("status") != "Done":
            issues.append(f"Dependency {dep} is not Done.")
        if dep_state.get("gate") != "Pass":
            issues.append(f"Dependency {dep} gate is not Pass.")
        if require_approval and dep_state.get("approval") not in {"Approved", "N/A"}:
            issues.append(f"Dependency {dep} approval is not Approved.")
    return (len(issues) == 0, issues)


def set_artifact_approval(
    project_dir: Path,
    requirement_name: str,
    requirement_id: str,
    artifact_name: str,
    approval_state: str,
    notes: str,
) -> Path:
    artifact = _normalize_artifact_name(artifact_name)
    if artifact not in ARTIFACT_SEQUENCE:
        raise ValueError(f"Unsupported artifact: {artifact_name}")
    if approval_state not in {"Approved", "Rejected", "Pending", "N/A"}:
        raise ValueError("Approval state must be Approved, Rejected, Pending, or N/A.")

    state = _parse_status_file(_status_path(project_dir, requirement_name))
    info = state[artifact]
    info["approval"] = approval_state
    info["updated"] = _today()
    info["notes"] = notes or info.get("notes", "-")
    state[artifact] = info
    return _write_status_file(project_dir, requirement_name, requirement_id, state)


def get_next_runnable_artifact(
    project_dir: Path,
    requirement_name: str,
    require_approval: bool = True,
) -> str | None:
    state = _parse_status_file(_status_path(project_dir, requirement_name))
    for artifact in ARTIFACT_SEQUENCE:
        info = state[artifact]
        if info.get("status") == "Done" and info.get("gate") == "Pass":
            continue
        deps_ok, _ = _dependency_gate_pass(state, artifact, require_approval=require_approval)
        if deps_ok:
            return artifact
    return None


def can_run_artifact(
    project_dir: Path,
    requirement_name: str,
    artifact_name: str,
    require_approval: bool = True,
) -> tuple[bool, list[str]]:
    artifact = _normalize_artifact_name(artifact_name)
    if artifact not in ARTIFACT_SEQUENCE:
        return False, [f"Unsupported artifact: {artifact_name}"]
    state = _parse_status_file(_status_path(project_dir, requirement_name))
    return _dependency_gate_pass(state, artifact, require_approval=require_approval)


def record_artifact_result(
    project_dir: Path,
    requirement_name: str,
    requirement_id: str,
    artifact_name: str,
    content: str,
    auto_approve: bool = False,
) -> tuple[Path, str, str]:
    artifact = _normalize_artifact_name(artifact_name)
    if artifact not in ARTIFACT_SEQUENCE:
        raise ValueError(f"Unsupported artifact: {artifact_name}")

    state = _parse_status_file(_status_path(project_dir, requirement_name))
    gate_result, gate_notes = _artifact_gate_result(artifact, content)
    approval = "Approved" if auto_approve and gate_result == "Pass" else "Pending"

    info = state[artifact]
    info["status"] = "Done" if gate_result == "Pass" else "Blocked"
    info["gate"] = gate_result
    info["approval"] = approval if artifact != "review-notes.md" else "N/A"
    info["updated"] = _today()
    info["notes"] = gate_notes
    state[artifact] = info

    status_path = _write_status_file(project_dir, requirement_name, requirement_id, state)
    return status_path, gate_result, gate_notes


def render_gate_report(
    project_dir: Path,
    requirement_name: str,
    requirement_id: str,
) -> Path:
    state = _parse_status_file(_status_path(project_dir, requirement_name))
    output_dir = _output_dir(project_dir, requirement_name)
    output_dir.mkdir(parents=True, exist_ok=True)
    path = output_dir / "gate-report.md"

    lines = [
        "# Gate Report",
        "",
        f"- Requirement Name: {requirement_name}",
        f"- Requirement ID: {requirement_id}",
        f"- Last Updated: {_today()}",
        "",
        "| Artifact | Gate | Approval | Status | Notes |",
        "|---------|------|----------|--------|------|",
    ]
    for artifact in ARTIFACT_SEQUENCE:
        info = state[artifact]
        lines.append(
            "| "
            + " | ".join(
                [
                    artifact,
                    info.get("gate", "Pending"),
                    info.get("approval", "Pending"),
                    info.get("status", "Not Started"),
                    info.get("notes", "-"),
                ]
            )
            + " |"
        )

    blocked = [
        artifact
        for artifact, info in state.items()
        if info.get("status") == "Blocked" or info.get("gate") == "Fail"
    ]
    lines.extend(["", "## Current Gate State"])
    if blocked:
        for item in blocked:
            lines.append(f"- Blocked artifact: {item}")
    else:
        lines.append("- No blocked artifact.")
    lines.append("")
    path.write_text("\n".join(lines), encoding="utf-8")
    return path


def list_artifacts() -> list[str]:
    return list(ARTIFACT_SEQUENCE)

