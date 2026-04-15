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
    "project_paths_for_artifact_review_manager",
    Path(__file__).resolve().parent / "project_paths.py",
)


def _review_dir(project_dir: Path, requirement_name: str) -> Path:
    return _PATHS.requirement_output_dir(project_dir, requirement_name) / "artifact-reviews"


def _read_text_if_exists(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8")


def _artifact_review_file_name(artifact_name: str) -> str:
    mapping = {
        "clarification": "clarification-review.md",
        "brd": "brd-review.md",
        "frs": "frs-review.md",
        "user-story": "user-story-review.md",
        "acceptance-criteria": "acceptance-criteria-review.md",
        "feature-list": "feature-list-review.md",
        "wireframe": "wireframe-review.md",
        "ui": "ui-review.md",
        "test-cases": "test-case-review.md",
        "requirement-traceability-matrix": "traceability-review.md",
        "requirement-traceability-flow": "traceability-review.md",
        "review": "traceability-review.md",
    }
    return mapping.get(artifact_name, f"{artifact_name}-review.md")


def _artifact_checklist_template_name(artifact_name: str) -> str:
    mapping = {
        "clarification": "clarification-checklist.md",
        "brd": "brd-checklist.md",
        "frs": "frs-checklist.md",
        "user-story": "user-story-checklist.md",
        "acceptance-criteria": "acceptance-criteria-checklist.md",
        "feature-list": "feature-list-checklist.md",
        "wireframe": "wireframe-checklist.md",
        "ui": "ui-checklist.md",
        "test-cases": "test-case-checklist.md",
        "requirement-traceability-matrix": "traceability-checklist.md",
        "requirement-traceability-flow": "traceability-checklist.md",
        "review": "traceability-checklist.md",
    }
    return mapping.get(artifact_name, "")


def _build_review_content(
    project_name: str,
    requirement_name: str,
    requirement_id: str,
    artifact_name: str,
    approval_state: str,
    gate_result: str,
    notes: str,
    checklist_template_text: str,
) -> str:
    major_issue = "None."
    minor_issue = "None."
    next_action = "No action needed."

    if gate_result in {"Fail", "Not Allowed"} or approval_state in {"Blocked", "Rework Needed"}:
        major_issue = notes or "Quality gate failed or dependency blocked."
        next_action = "Fix major issues, then rerun this artifact."
    elif gate_result == "Warning" or approval_state == "In Review":
        minor_issue = notes or "Minor quality issue needs review."
        next_action = "Review noted issues and approve when ready."

    checklist_summary = "Pending"
    if approval_state == "Approved":
        checklist_summary = "Pass"
    elif approval_state in {"In Review", "Rework Needed"}:
        checklist_summary = "Needs Attention"
    elif approval_state == "Blocked":
        checklist_summary = "Blocked"

    checklist_lines = checklist_template_text.splitlines()
    checklist_lines = [line for line in checklist_lines if not line.strip().startswith("#")]
    checklist_block = "\n".join(checklist_lines).strip()
    if not checklist_block:
        checklist_block = "- No checklist template found."

    return "\n".join(
        [
            f"# {artifact_name} Review",
            "",
            "## Overview",
            f"- Project Name: {project_name}",
            f"- Requirement Name: {requirement_name}",
            f"- Requirement ID: {requirement_id}",
            f"- Artifact Name: {artifact_name}",
            f"- Current Approval State: {approval_state}",
            f"- Gate Result: {gate_result}",
            f"- Last Updated: {_today()}",
            "",
            "## Checklist Result",
            f"- Overall: {checklist_summary}",
            "",
            checklist_block,
            "",
            "## Major Issues",
            f"- {major_issue}",
            "",
            "## Minor Issues",
            f"- {minor_issue}",
            "",
            "## Recommended Next Action",
            f"- {next_action}",
            "",
            "<!-- TODO: Add reviewer name and approval timestamp. -->",
            "",
        ]
    )


def ensure_artifact_reviews(
    project_dir: Path,
    requirement_name: str,
    requirement_id: str,
    catalog: list[dict[str, object]],
    checklist_templates_dir: Path,
) -> Path:
    review_dir = _review_dir(project_dir, requirement_name)
    review_dir.mkdir(parents=True, exist_ok=True)
    for item in catalog:
        artifact_name = str(item.get("name", "")).strip()
        if not artifact_name:
            continue
        file_name = _artifact_review_file_name(artifact_name)
        review_path = review_dir / file_name
        if review_path.exists():
            continue
        template_name = _artifact_checklist_template_name(artifact_name)
        template_text = _read_text_if_exists(checklist_templates_dir / template_name) if template_name else ""
        review_path.write_text(
            _build_review_content(
                project_name=project_dir.name,
                requirement_name=requirement_name,
                requirement_id=requirement_id,
                artifact_name=artifact_name,
                approval_state="Draft",
                gate_result="Not Run",
                notes="Not reviewed yet.",
                checklist_template_text=template_text,
            ),
            encoding="utf-8",
        )
    return review_dir


def update_artifact_review(
    project_dir: Path,
    requirement_name: str,
    requirement_id: str,
    artifact_name: str,
    approval_state: str,
    gate_result: str,
    notes: str,
    checklist_templates_dir: Path,
) -> Path:
    review_dir = _review_dir(project_dir, requirement_name)
    review_dir.mkdir(parents=True, exist_ok=True)
    file_name = _artifact_review_file_name(artifact_name)
    review_path = review_dir / file_name
    template_name = _artifact_checklist_template_name(artifact_name)
    template_text = _read_text_if_exists(checklist_templates_dir / template_name) if template_name else ""
    review_path.write_text(
        _build_review_content(
            project_name=project_dir.name,
            requirement_name=requirement_name,
            requirement_id=requirement_id,
            artifact_name=artifact_name,
            approval_state=approval_state,
            gate_result=gate_result,
            notes=notes,
            checklist_template_text=template_text,
        ),
        encoding="utf-8",
    )
    return review_path
