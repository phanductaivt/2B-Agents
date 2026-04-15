from __future__ import annotations

from datetime import date
from pathlib import Path
import re


def _today() -> str:
    return date.today().isoformat()


def _priority_from_type(case_type: str) -> str:
    if case_type == "Happy Path":
        return "High"
    if case_type in {"Validation / Negative", "Error Handling"}:
        return "High"
    return "Medium"


def _compact_steps(steps: list[str], max_steps: int = 6) -> list[str]:
    clean = [step.strip().lstrip("- ").strip() for step in steps if step.strip()]
    if len(clean) <= max_steps:
        return clean
    return clean[: max_steps - 1] + ["(continue as needed)"]


def _build_test_case_rows(
    tc_ids: list[str],
    ids: dict[str, str],
    frs: dict[str, object],
    acceptance_criteria: list[str],
) -> list[dict[str, str]]:
    main_flow = [str(item) for item in frs.get("main_flow", [])]
    validations = [str(item) for item in frs.get("validations", [])]
    edge_cases = [str(item) for item in frs.get("edge_cases", [])]
    alternative_flows = [str(item) for item in frs.get("alternative_flows", [])]

    cases: list[dict[str, str]] = []

    def add_case(case_type: str, scenario: str, pre: str, steps: list[str], expected: str, notes: str) -> None:
        if len(cases) >= len(tc_ids):
            return
        tc_id = tc_ids[len(cases)]
        cases.append(
            {
                "tc_id": tc_id,
                "ac_id": ids.get("ac", ""),
                "us_id": ids.get("us", ""),
                "fr_id": ids.get("fr", ""),
                "type": case_type,
                "scenario": scenario,
                "pre": pre,
                "steps": " ".join(f"{i+1}. {step}" for i, step in enumerate(_compact_steps(steps))),
                "expected": expected,
                "priority": _priority_from_type(case_type),
                "notes": notes,
            }
        )

    # Happy Path
    if main_flow:
        add_case(
            "Happy Path",
            "Complete the main flow successfully",
            "User is allowed to access the feature and has a valid record (booking/member/etc.)",
            main_flow,
            "The system completes the main flow and shows a clear success outcome.",
            "Core scenario based on FRS main flow.",
        )
    else:
        add_case(
            "Happy Path",
            "Basic end-to-end usage based on acceptance criteria",
            "User is authenticated and has access to the feature.",
            acceptance_criteria or ["Open the feature and complete the intended action."],
            "The expected outcome matches the acceptance criteria.",
            "FRS main flow was not available; used acceptance criteria.",
        )

    # Validation / Negative
    if validations:
        add_case(
            "Validation / Negative",
            "Validation prevents an invalid action",
            "User is on the relevant screen with an invalid input or invalid state.",
            ["Trigger the validation condition.", "Attempt to continue."],
            "The system blocks the action and shows a clear, actionable message.",
            f"Validation reference: {validations[0]}",
        )
    else:
        add_case(
            "Validation / Negative",
            "User tries to proceed with missing required data",
            "User is on the relevant screen and required data is missing.",
            ["Leave required data empty.", "Attempt to submit/continue."],
            "The system blocks the action and highlights the missing data.",
            "Generic validation case.",
        )

    # Edge Case
    if edge_cases:
        add_case(
            "Edge Case",
            "Edge case handling works as expected",
            "User is in a special state that triggers an edge case.",
            ["Set up the edge case state.", "Run the flow step that triggers it."],
            "The system behaves consistently and does not produce confusing results.",
            f"Edge case reference: {edge_cases[0]}",
        )
    else:
        add_case(
            "Edge Case",
            "High volume or unusual but valid input",
            "User has a valid record but with an unusual configuration.",
            ["Prepare the unusual but valid configuration.", "Run the main flow."],
            "The system completes the flow and shows correct data.",
            "Generic edge case.",
        )

    # Error Handling
    if alternative_flows:
        add_case(
            "Error Handling",
            "Alternative flow is shown when main flow cannot continue",
            "Main flow is blocked by a known condition.",
            ["Trigger the alternative flow condition.", "Attempt the main flow."],
            "The system routes to the alternative flow and clearly explains next steps.",
            f"Alternative flow reference: {alternative_flows[0]}",
        )
    else:
        add_case(
            "Error Handling",
            "System handles a temporary error gracefully",
            "A temporary service error is simulated.",
            ["Trigger a temporary error.", "Retry if available."],
            "The system shows a friendly error and provides a retry or support path.",
            "Generic error handling case.",
        )

    return cases


def generate_test_cases(
    project_dir: Path,
    project_name: str,
    requirement_name: str,
    ids: dict[str, str],
    ba_package: dict[str, object],
    id_manager_module,
    output_dir: Path,
) -> tuple[str, list[str]]:
    """Return test-cases.md content plus the list of TC IDs used."""
    # Keep it small and practical by default: one per category (4 total).
    planned_count = 4

    existing_tc_ids = extract_tc_ids(output_dir / "test-cases.md")
    tc_ids = existing_tc_ids[:planned_count]
    if len(tc_ids) < planned_count:
        tc_ids.extend(id_manager_module.allocate_tc_ids(project_dir, planned_count - len(tc_ids)))
    frs = ba_package.get("frs", {})
    acceptance_criteria = [str(item) for item in ba_package.get("acceptance_criteria", [])]

    cases = _build_test_case_rows(tc_ids, ids, frs if isinstance(frs, dict) else {}, acceptance_criteria)
    used_tc_ids = [case["tc_id"] for case in cases]

    lines = [
        "# Test Cases",
        "",
        "## Overview",
        f"- Project Name: {project_name}",
        f"- Requirement Name: {requirement_name}",
        f"- Linked Requirement ID: {ids.get('req', '')}",
        f"- Last Updated: {_today()}",
        "",
        "## Test Case Matrix",
        "",
        "| TC ID | Linked AC ID | Linked US ID | Linked FR ID | Test Type | Test Scenario | Preconditions | Test Steps | Expected Result | Priority | Notes |",
        "|------|---------------|--------------|--------------|----------|---------------|---------------|------------|-----------------|----------|------|",
    ]

    for case in cases:
        lines.append(
            "| "
            + " | ".join(
                [
                    case["tc_id"],
                    case["ac_id"] or "-",
                    case["us_id"] or "-",
                    case["fr_id"] or "-",
                    case["type"],
                    case["scenario"],
                    case["pre"],
                    case["steps"],
                    case["expected"],
                    case["priority"],
                    case["notes"],
                ]
            )
            + " |"
        )

    lines.append("")
    lines.append("<!-- TODO: Expand test case generation to create one TC per acceptance criterion when needed. -->")
    lines.append("")

    return "\n".join(lines).rstrip() + "\n", used_tc_ids


def write_test_cases(output_dir: Path, content: str) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    path = output_dir / "test-cases.md"
    path.write_text(content, encoding="utf-8")
    return path


def extract_tc_ids(path: Path) -> list[str]:
    """Extract TC IDs from an existing test-cases.md if present."""
    if not path.exists():
        return []
    text = path.read_text(encoding="utf-8")
    found = re.findall(r"\bTC-\d{3}\b", text)
    # Preserve order of first appearance.
    seen: set[str] = set()
    result: list[str] = []
    for item in found:
        if item in seen:
            continue
        seen.add(item)
        result.append(item)
    return result
