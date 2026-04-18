from __future__ import annotations

from typing import Any


STALE_STATES = {"fresh", "stale", "needs-rerun", "manual-override"}

REQ_STATUS_MAP = {
    "not started": "Not Started",
    "in progress": "In Review",
    "blocked": "Blocked",
    "done": "Processed",
    "in review": "In Review",
    "approved": "Approved",
    "processed": "Processed",
}

PROCESSING_STATUS_MAP = {
    "not started": "not-started",
    "in progress": "in-review",
    "in review": "in-review",
    "blocked": "blocked",
    "done": "processed",
    "processed": "processed",
    "approved": "approved",
}


def normalize_execution_owner(raw_owner: str) -> str:
    owner = str(raw_owner or "").strip()
    if not owner:
        return "-"
    if "agent" in owner.lower():
        return owner
    owner_map = {
        "BA": "BA Agent",
        "UXUI": "UXUI Agent",
        "FE": "FE Agent",
        "REVIEWER": "Reviewer Agent",
        "QA": "Reviewer Agent",
    }
    return owner_map.get(owner.upper(), f"{owner} Agent")


def normalize_stale_state(raw_state: str) -> str:
    value = str(raw_state or "").strip().lower()
    if value in STALE_STATES:
        return value
    if value == "needs_rerun":
        return "needs-rerun"
    return "fresh"


def normalize_requirement_display_status(raw_status: str, project_status: str) -> str:
    normalized = REQ_STATUS_MAP.get(str(raw_status or "").strip().lower(), str(raw_status or "").strip() or "Not Started")
    if normalized == "Processed" and str(project_status or "").strip().lower() == "done":
        return "Approved"
    return normalized


def normalize_processing_status(raw_status: str) -> str:
    return PROCESSING_STATUS_MAP.get(str(raw_status or "").strip().lower(), "unknown")


def project_status_and_readiness(
    requirement_statuses: list[str],
    blockers: list[str],
    project_phase: str,
    overall_progress_text: str = "",
) -> tuple[str, int]:
    total = len(requirement_statuses)
    done_count = sum(1 for status in requirement_statuses if str(status).strip().lower() == "done")

    status_weight = {
        "not started": 0,
        "in progress": 60,
        "blocked": 35,
        "done": 100,
    }
    if total:
        weighted = [status_weight.get(str(status).strip().lower(), 40) for status in requirement_statuses]
        readiness = int(round(sum(weighted) / len(weighted)))
    else:
        readiness = 0

    phase_lower = str(project_phase or "").strip().lower()
    status = "Active"
    if blockers or phase_lower == "blocked":
        status = "Blocked"
    elif total > 0 and done_count == total:
        status = "Done"
    elif str(overall_progress_text or "").strip().lower() in {"done", "completed"} and not blockers:
        status = "Done"

    if status != "Done" and readiness >= 100:
        readiness = 95
    if status == "Blocked":
        readiness = min(readiness, 90)
    if status == "Done":
        readiness = max(readiness, 100)
    return status, readiness


def parse_confirmation_blockers(confirmation_items: list[dict[str, Any]]) -> list[str]:
    blockers: list[str] = []
    for item in confirmation_items:
        if not isinstance(item, dict):
            continue
        status = str(item.get("status", "pending")).strip().lower()
        if status not in {"pending", "needs-more-info"}:
            continue
        reason = str(item.get("blocked_reason", "")).strip()
        if reason:
            blockers.append(reason)
    return blockers


def resolve_blocked_reason(
    gate_rows: list[dict[str, str]],
    project_blockers: list[str],
    focus_row: dict[str, str] | None,
    confirmation_blockers: list[str] | None = None,
) -> str:
    """
    Blocked reason precedence:
    1) Gate failure/not-allowed reason
    2) Confirmation blocker
    3) Project blocker list
    4) Focus artifact blocked/rework note
    """
    for row in gate_rows:
        gate_result = str(row.get("gate_result", "")).strip()
        reason = str(row.get("reason", "")).strip()
        if gate_result in {"Fail", "Not Allowed"} and reason and reason not in {"-", "Not Run"}:
            return reason

    for reason in confirmation_blockers or []:
        value = str(reason).strip()
        if value:
            return value

    for blocker in project_blockers:
        value = str(blocker).strip()
        if value:
            return value

    if focus_row and str(focus_row.get("status", "")) in {"Blocked", "Rework Needed"}:
        note = str(focus_row.get("notes", "")).strip()
        if note and note != "-":
            return note

    return "No blocker reason recorded."


def execution_snapshot(
    artifact_rows: list[dict[str, str]],
    gate_rows: list[dict[str, str]],
    project_blockers: list[str],
    confirmation_blockers: list[str] | None = None,
) -> dict[str, Any]:
    total_artifacts = len(artifact_rows)
    done_artifacts = sum(1 for row in artifact_rows if str(row.get("status", "")).strip() == "Done")
    completion_rate = int(round((done_artifacts / total_artifacts) * 100)) if total_artifacts else 0

    status_keys = ["Done", "In Review", "In Progress", "Blocked", "Rework Needed", "Failed", "Not Started"]
    status_counts = {key: 0 for key in status_keys}
    for row in artifact_rows:
        key = str(row.get("status", "")).strip()
        if key in status_counts:
            status_counts[key] += 1

    gate_counts = {"Pass": 0, "Warning": 0, "Fail": 0, "Not Allowed": 0}
    for row in gate_rows:
        key = str(row.get("gate_result", "")).strip()
        if key in gate_counts:
            gate_counts[key] += 1

    prioritized = ["Blocked", "Rework Needed", "In Review", "In Progress", "Not Started", "Done"]
    focus_row: dict[str, str] | None = None
    for status in prioritized:
        focus_row = next((row for row in artifact_rows if str(row.get("status", "")).strip() == status), None)
        if focus_row:
            break

    current_stage = str((focus_row or {}).get("stage", "Not Started")).strip() or "Not Started"
    current_owner = normalize_execution_owner(str((focus_row or {}).get("owner", "-")))
    blocked_reason = resolve_blocked_reason(gate_rows, project_blockers, focus_row, confirmation_blockers)

    health = "Healthy"
    if status_counts["Blocked"] > 0 or status_counts["Rework Needed"] > 0 or gate_counts["Fail"] > 0 or gate_counts["Not Allowed"] > 0:
        health = "At Risk"
    elif status_counts["In Review"] > 0 or gate_counts["Warning"] > 0:
        health = "Needs Attention"
    elif total_artifacts == 0:
        health = "Not Started"

    return {
        "current_execution_stage": current_stage,
        "current_execution_owner": current_owner,
        "artifact_completion_rate": completion_rate,
        "execution_health": health,
        "gate_summary": (
            f"{gate_counts['Pass']} Pass | {gate_counts['Warning']} Warning | "
            f"{gate_counts['Fail']} Fail | {gate_counts['Not Allowed']} Not Allowed"
        ),
        "blocked_reason": blocked_reason,
        "artifact_status_counts": status_counts,
        "current_artifact_statuses": (
            f"Done: {status_counts['Done']} | In Review: {status_counts['In Review']} | "
            f"In Progress: {status_counts['In Progress']} | Blocked: {status_counts['Blocked']} | "
            f"Rework Needed: {status_counts['Rework Needed']} | Failed: {status_counts['Failed']}"
        ),
        "gate_fail_count": gate_counts["Fail"] + gate_counts["Not Allowed"],
    }


def requirement_processing_rows(
    requirement_rows: list[dict[str, str]],
    processing_state_requirements: dict[str, Any],
    project_status: str,
) -> list[dict[str, Any]]:
    results: list[dict[str, Any]] = []
    for row in requirement_rows:
        requirement_name = str(row.get("requirement_name", "")).strip()
        if not requirement_name:
            continue
        state_row = processing_state_requirements.get(f"{requirement_name}.md", {})
        if not isinstance(state_row, dict):
            state_row = {}

        current_status = str(row.get("current_status", "")).strip()
        display_status = normalize_requirement_display_status(current_status, project_status)
        processing_status = normalize_processing_status(current_status)
        if display_status == "Approved":
            processing_status = "approved"
        elif display_status == "Processed":
            processing_status = "processed"
        elif display_status == "In Review":
            processing_status = "in-review"
        elif display_status == "Blocked":
            processing_status = "blocked"

        input_change_state = str(state_row.get("status", "")).strip().lower() or "unknown"
        if input_change_state == "processed":
            input_change_state = "processed"
        elif input_change_state in {"new", "changed", "unchanged", "forced"}:
            pass
        else:
            input_change_state = "unknown"

        results.append(
            {
                "requirement_name": requirement_name,
                "processing_status": processing_status,
                "display_status": display_status,
                "input_change_state": input_change_state,
                "last_processed_at": str(state_row.get("last_processed_at", "")) or "-",
                "rerun_needed": processing_status in {"blocked", "in-review"},
            }
        )
    return results
