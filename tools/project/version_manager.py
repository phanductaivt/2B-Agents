from __future__ import annotations

from datetime import date
from pathlib import Path
import re


KEY_ARTIFACTS = [
    "brd.md",
    "frs.md",
    "user-story.md",
    "acceptance-criteria.md",
    "feature-list.md",
    "wireframe.md",
    "ui.html",
    "test-cases.md",
    "review-notes.md",
]

CORE_STRUCTURAL_ARTIFACTS = {"brd.md", "frs.md", "feature-list.md"}


def _today() -> str:
    return date.today().isoformat()


def _normalize_text(value: str) -> str:
    return value.strip().replace("\r\n", "\n")


def _read_if_exists(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8")


def _extract_current_version(version_info_path: Path) -> str | None:
    if not version_info_path.exists():
        return None
    for line in version_info_path.read_text(encoding="utf-8").splitlines():
        if line.strip().startswith("- Current Version:"):
            value = line.split(":", 1)[1].strip()
            return value or None
    return None


def _parse_version(version: str) -> tuple[int, int]:
    match = re.match(r"^v(\d+)\.(\d+)$", version.strip())
    if not match:
        return (1, 0)
    return (int(match.group(1)), int(match.group(2)))


def _format_version(major: int, minor: int) -> str:
    return f"v{major}.{minor}"


def _is_major_structural_change(changed_artifacts: list[str]) -> bool:
    changed_core = [name for name in changed_artifacts if name in CORE_STRUCTURAL_ARTIFACTS]
    return len(changed_core) >= 2


def _next_version(current_version: str, changed_artifacts: list[str]) -> str:
    major, minor = _parse_version(current_version)
    if _is_major_structural_change(changed_artifacts):
        return _format_version(major + 1, 0)
    return _format_version(major, minor + 1)


def ensure_project_change_log(project_dir: Path) -> Path:
    """Create project-level change-log.md if missing."""
    path = project_dir / "change-log.md"
    if path.exists():
        return path
    template = "\n".join(
        [
            "# Change Log",
            "",
            "Track meaningful output revisions for this project.",
            "",
            "<!-- TODO: Optional history snapshots can be saved under outputs/generated/<requirement>/history/. -->",
            "",
        ]
    )
    path.write_text(template, encoding="utf-8")
    return path


def detect_artifact_changes(
    output_dir: Path,
    markdown_files: dict[str, str],
    html_files: dict[str, str],
) -> list[str]:
    """
    Compare generated files with current files and return changed key artifacts.
    """
    changed: list[str] = []
    combined: dict[str, str] = {}
    combined.update(markdown_files)
    combined.update(html_files)

    for artifact in KEY_ARTIFACTS:
        if artifact not in combined:
            continue
        old_text = _normalize_text(_read_if_exists(output_dir / artifact))
        new_text = _normalize_text(combined[artifact])
        if old_text != new_text:
            changed.append(artifact)
    return changed


def _write_version_info(
    output_dir: Path,
    requirement_name: str,
    requirement_id: str,
    current_version: str,
    previous_version: str,
    change_summary: str,
    changed_artifacts: list[str],
    affected_ids: list[str],
) -> Path:
    path = output_dir / "version-info.md"
    changed_text = ", ".join(changed_artifacts) if changed_artifacts else "No key artifact changed."
    ids_text = ", ".join(affected_ids) if affected_ids else requirement_id
    content = "\n".join(
        [
            "# Version Info",
            f"- Requirement Name: {requirement_name}",
            f"- Requirement ID: {requirement_id}",
            f"- Current Version: {current_version}",
            f"- Last Updated: {_today()}",
            f"- Previous Version: {previous_version}",
            f"- Change Summary: {change_summary}",
            f"- Changed Artifacts: {changed_text}",
            f"- Affected IDs: {ids_text}",
            "",
            "## Change Summary Template",
            "- What changed:",
            "- Why it changed:",
            "- Which IDs are affected:",
            "",
            "<!-- TODO: Add optional output snapshot files to history/ when the team needs strict audit history. -->",
            "",
        ]
    )
    path.write_text(content, encoding="utf-8")
    return path


def _append_change_log_entry(
    change_log_path: Path,
    version: str,
    requirement_name: str,
    requirement_id: str,
    changed_artifacts: list[str],
    affected_ids: list[str],
    reason: str,
    summary: str,
) -> None:
    changed_text = ", ".join(changed_artifacts) if changed_artifacts else "No key artifact changed."
    changed_text = changed_text.rstrip(".")
    ids_text = ", ".join(affected_ids) if affected_ids else requirement_id
    block = "\n".join(
        [
            f"## Version {version}",
            f"- Date: {_today()}",
            f"- Scope: Requirement package update for {requirement_name}",
            f"- Summary of Changes: {summary}. Changed artifacts: {changed_text}.",
            f"- Affected Requirements: {requirement_name} ({requirement_id})",
            f"- Reason: {reason}. Affected IDs: {ids_text}",
            "",
        ]
    )

    existing = change_log_path.read_text(encoding="utf-8").rstrip()
    change_log_path.write_text(existing + "\n\n" + block, encoding="utf-8")


def update_version_tracking(
    project_dir: Path,
    output_dir: Path,
    requirement_name: str,
    requirement_id: str,
    changed_artifacts: list[str],
    affected_ids: list[str],
    is_new_output: bool,
    reason: str,
) -> dict[str, object]:
    """
    Update requirement-level version-info.md and project-level change-log.md.
    """
    output_dir.mkdir(parents=True, exist_ok=True)
    change_log_path = ensure_project_change_log(project_dir)

    version_info_path = output_dir / "version-info.md"
    previous_version = _extract_current_version(version_info_path)

    if is_new_output or previous_version is None:
        current_version = "v1.0"
        previous_value = "-"
        if is_new_output:
            summary = "Initial generation created the requirement output package"
        else:
            summary = "Version tracking baseline was created for an existing requirement output package"
        append_change_log = True
    elif changed_artifacts:
        current_version = _next_version(previous_version, changed_artifacts)
        previous_value = previous_version
        summary = "Requirement output package was regenerated with meaningful updates"
        append_change_log = True
    else:
        current_version = previous_version
        previous_value = previous_version
        summary = "Re-run completed with no meaningful output change"
        append_change_log = False

    version_info_written = _write_version_info(
        output_dir=output_dir,
        requirement_name=requirement_name,
        requirement_id=requirement_id,
        current_version=current_version,
        previous_version=previous_value,
        change_summary=summary,
        changed_artifacts=changed_artifacts,
        affected_ids=affected_ids,
    )

    if append_change_log:
        _append_change_log_entry(
            change_log_path=change_log_path,
            version=current_version,
            requirement_name=requirement_name,
            requirement_id=requirement_id,
            changed_artifacts=changed_artifacts,
            affected_ids=affected_ids,
            reason=reason,
            summary=summary,
        )

    return {
        "current_version": current_version,
        "previous_version": previous_value,
        "changed_artifacts": changed_artifacts,
        "version_info_path": version_info_written,
        "change_log_path": change_log_path,
        "change_logged": append_change_log,
    }
