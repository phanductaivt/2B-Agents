from __future__ import annotations

from datetime import date
import importlib.util
from pathlib import Path
import re
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
    "project_paths_for_artifact_runner",
    Path(__file__).resolve().parent / "project_paths.py",
)


def _strip_comment(line: str) -> str:
    if "#" not in line:
        return line.rstrip()
    head, _tail = line.split("#", 1)
    return head.rstrip()


def _parse_inline_list(value: str) -> list[str]:
    raw = value.strip()
    if raw == "[]":
        return []
    if not (raw.startswith("[") and raw.endswith("]")):
        return []
    body = raw[1:-1].strip()
    if not body:
        return []
    return [item.strip().strip("'\"") for item in body.split(",") if item.strip()]


def load_artifact_catalog(catalog_path: Path) -> list[dict[str, object]]:
    if not catalog_path.exists():
        raise FileNotFoundError(f"Missing artifact catalog: {catalog_path}")

    artifacts: list[dict[str, object]] = []
    current: dict[str, object] | None = None
    current_list_key: str | None = None

    for raw in catalog_path.read_text(encoding="utf-8").splitlines():
        line = _strip_comment(raw)
        stripped = line.strip()
        if not stripped or stripped == "artifacts:":
            continue

        if stripped.startswith("- name:"):
            if current:
                artifacts.append(current)
            current = {
                "name": stripped.split(":", 1)[1].strip(),
                "stage": "",
                "owner": "",
                "dependencies": [],
                "outputs": [],
                "validators": [],
                "gate_required": True,
            }
            current_list_key = None
            continue

        if current is None:
            continue

        if stripped.startswith("- ") and current_list_key:
            value = stripped[2:].strip()
            values = current.get(current_list_key, [])
            if isinstance(values, list):
                values.append(value)
                current[current_list_key] = values
            continue

        if ":" not in stripped:
            continue

        key, value = stripped.split(":", 1)
        key = key.strip()
        value = value.strip()

        if key in {"dependencies", "outputs", "validators"}:
            if value:
                current[key] = _parse_inline_list(value)
                current_list_key = None
            else:
                current[key] = []
                current_list_key = key
            continue

        if key == "gate_required":
            current[key] = value.lower() == "true"
            current_list_key = None
            continue

        current[key] = value
        current_list_key = None

    if current:
        artifacts.append(current)

    return artifacts


def load_gates_config(path: Path) -> dict[str, dict[str, list[str]]]:
    if not path.exists():
        return {}
    config: dict[str, dict[str, list[str]]] = {}
    current_artifact: str | None = None
    current_list_key: str | None = None

    for raw in path.read_text(encoding="utf-8").splitlines():
        line = _strip_comment(raw)
        stripped = line.strip()
        if not stripped or stripped == "gates:":
            continue

        if stripped.endswith(":") and not stripped.startswith("-"):
            key = stripped[:-1]
            if key and key != "allow_downstream_if":
                current_artifact = key
                config.setdefault(
                    current_artifact,
                    {
                        "allow_downstream_if": ["Pass"],
                        "allow_approval_if": ["Approved", "In Review"],
                    },
                )
                current_list_key = None
            continue

        if stripped.startswith("allow_downstream_if:"):
            value = stripped.split(":", 1)[1].strip()
            if current_artifact is None:
                continue
            if value:
                config[current_artifact]["allow_downstream_if"] = _parse_inline_list(value)
                current_list_key = None
            else:
                config[current_artifact]["allow_downstream_if"] = []
                current_list_key = "allow_downstream_if"
            continue

        if stripped.startswith("allow_approval_if:"):
            value = stripped.split(":", 1)[1].strip()
            if current_artifact is None:
                continue
            if value:
                config[current_artifact]["allow_approval_if"] = _parse_inline_list(value)
                current_list_key = None
            else:
                config[current_artifact]["allow_approval_if"] = []
                current_list_key = "allow_approval_if"
            continue

        if stripped.startswith("- ") and current_artifact and current_list_key == "allow_downstream_if":
            config[current_artifact]["allow_downstream_if"].append(stripped[2:].strip().strip("'\""))
            continue

        if stripped.startswith("- ") and current_artifact and current_list_key == "allow_approval_if":
            config[current_artifact]["allow_approval_if"].append(stripped[2:].strip().strip("'\""))

    return config


def catalog_by_name(catalog: list[dict[str, object]]) -> dict[str, dict[str, object]]:
    result: dict[str, dict[str, object]] = {}
    for item in catalog:
        name = str(item.get("name", "")).strip()
        if name:
            result[name] = item
    return result


def _resolve_dependencies(
    artifact_name: str,
    indexed: dict[str, dict[str, object]],
    visited: set[str],
    stack: set[str],
    ordered: list[str],
) -> None:
    if artifact_name in visited:
        return
    if artifact_name in stack:
        raise ValueError(f"Circular artifact dependency detected at '{artifact_name}'.")
    if artifact_name not in indexed:
        raise ValueError(f"Artifact '{artifact_name}' is not defined in artifact catalog.")

    stack.add(artifact_name)
    dependencies = indexed[artifact_name].get("dependencies", [])
    if isinstance(dependencies, list):
        for dep in dependencies:
            dep_name = str(dep).strip()
            if dep_name:
                _resolve_dependencies(dep_name, indexed, visited, stack, ordered)
    stack.remove(artifact_name)
    visited.add(artifact_name)
    ordered.append(artifact_name)


def build_execution_plan(
    catalog: list[dict[str, object]],
    target_artifact: str | None = None,
    target_stage: str | None = None,
) -> list[str]:
    indexed = catalog_by_name(catalog)

    if target_artifact:
        artifact_key = target_artifact.strip()
        if artifact_key not in indexed:
            raise ValueError(f"Unknown artifact '{target_artifact}'.")
        selected = [artifact_key]
        visited: set[str] = set()
        ordered: list[str] = []
        for name in selected:
            _resolve_dependencies(name, indexed, visited, set(), ordered)
        return ordered

    if target_stage:
        selected = [
            str(item.get("name", "")).strip()
            for item in catalog
            if str(item.get("stage", "")).strip() == target_stage
        ]
        if not selected:
            raise ValueError(f"Unknown stage '{target_stage}'.")

        selected_scope = set(selected)
        visited: set[str] = set()
        ordered: list[str] = []

        def resolve_in_stage(name: str, stack: set[str]) -> None:
            if name in visited:
                return
            if name in stack:
                raise ValueError(f"Circular artifact dependency detected at '{name}'.")
            if name not in indexed:
                raise ValueError(f"Artifact '{name}' is not defined in artifact catalog.")
            stack.add(name)
            deps = indexed[name].get("dependencies", [])
            if isinstance(deps, list):
                for dep in deps:
                    dep_name = str(dep).strip()
                    if dep_name and dep_name in selected_scope:
                        resolve_in_stage(dep_name, stack)
            stack.remove(name)
            visited.add(name)
            ordered.append(name)

        for name in selected:
            resolve_in_stage(name, set())
        return ordered

    selected = [str(item.get("name", "")).strip() for item in catalog if str(item.get("name", "")).strip()]
    visited = set()
    ordered: list[str] = []
    for name in selected:
        _resolve_dependencies(name, indexed, visited, set(), ordered)
    return ordered


def _status_path(project_dir: Path, requirement_name: str) -> Path:
    return _PATHS.requirement_output_dir(project_dir, requirement_name) / "artifact-status.md"


def _gate_results_path(project_dir: Path, requirement_name: str) -> Path:
    return _PATHS.requirement_output_dir(project_dir, requirement_name) / "gate-results.md"


def _default_state(catalog: list[dict[str, object]]) -> dict[str, dict[str, str]]:
    state: dict[str, dict[str, str]] = {}
    for item in catalog:
        name = str(item.get("name", "")).strip()
        if not name:
            continue
        deps = item.get("dependencies", [])
        dep_text = "None"
        if isinstance(deps, list):
            dep_items = [str(dep).strip() for dep in deps if str(dep).strip()]
            if dep_items:
                dep_text = ", ".join(dep_items)
        state[name] = {
            "status": "Not Started",
            "approval": "Draft",
            "gate": "N/A",
            "notes": "-",
            "dependencies": dep_text,
        }
    return state


def parse_artifact_status(
    project_dir: Path,
    requirement_name: str,
    catalog: list[dict[str, object]],
) -> dict[str, dict[str, str]]:
    path = _status_path(project_dir, requirement_name)
    state = _default_state(catalog)
    if not path.exists():
        return state

    in_table = False
    table_has_dependencies = False
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if line == "| Artifact | Stage | Owner | Status | Dependencies | Gate | Notes |":
            in_table = True
            table_has_dependencies = True
            continue
        if line == "| Artifact | Stage | Owner | Status | Approval State | Gate | Notes |":
            in_table = True
            table_has_dependencies = False
            continue
        if in_table and not line.startswith("|"):
            break
        if in_table and line.startswith("|"):
            cols = [col.strip() for col in line.strip("|").split("|")]
            if len(cols) < 7:
                continue
            artifact = cols[0]
            if artifact not in state:
                continue
            state[artifact]["status"] = cols[3]
            if table_has_dependencies:
                state[artifact]["dependencies"] = cols[4] or "None"
                inferred = {
                    "Done": "Approved",
                    "In Review": "In Review",
                    "Rework Needed": "Rework Needed",
                    "Blocked": "Blocked",
                    "In Progress": "In Review",
                }
                state[artifact]["approval"] = inferred.get(cols[3], "Draft")
            else:
                state[artifact]["approval"] = cols[4] or "Draft"
            state[artifact]["gate"] = cols[5]
            state[artifact]["notes"] = cols[6] or "-"
    return state


def write_artifact_status(
    project_dir: Path,
    requirement_name: str,
    requirement_id: str,
    catalog: list[dict[str, object]],
    state: dict[str, dict[str, str]],
) -> Path:
    output_dir = _PATHS.requirement_output_dir(project_dir, requirement_name)
    output_dir.mkdir(parents=True, exist_ok=True)
    path = _status_path(project_dir, requirement_name)

    lines = [
        "# Artifact Status",
        "",
        "## Overview",
        f"- Project Name: {project_dir.name}",
        f"- Requirement Name: {requirement_name}",
        f"- Requirement ID: {requirement_id}",
        f"- Last Updated: {_today()}",
        "",
        "## Artifact Table",
        "",
        "| Artifact | Stage | Owner | Status | Approval State | Gate | Notes |",
        "|---------|------|------|--------|----------------|------|------|",
    ]

    for item in catalog:
        name = str(item.get("name", "")).strip()
        if not name:
            continue
        row = state.get(name, {})
        stage = str(item.get("stage", "")).strip()
        owner = str(item.get("owner", "")).strip().replace("-agent", "").upper()
        lines.append(
            "| "
            + " | ".join(
                [
                    name,
                    stage,
                    owner or "-",
                    row.get("status", "Not Started"),
                    row.get("approval", "Draft"),
                    row.get("gate", "N/A"),
                    row.get("notes", "-"),
                ]
            )
            + " |"
        )

    lines.extend(
        [
            "",
            "Suggested status values:",
            "- Not Started",
            "- In Progress",
            "- Done",
            "- In Review",
            "- Blocked",
            "- Rework Needed",
            "",
            "Suggested gate values:",
            "- Pass",
            "- Warning",
            "- Fail",
            "- Not Allowed",
            "- N/A",
            "",
            "Suggested approval values:",
            "- Draft",
            "- In Review",
            "- Approved",
            "- Rework Needed",
            "- Blocked",
            "",
            "<!-- TODO: Add reviewer name and approval date per artifact. -->",
            "",
        ]
    )

    path.write_text("\n".join(lines), encoding="utf-8")
    return path


def parse_gate_results(project_dir: Path, requirement_name: str) -> dict[str, dict[str, str]]:
    path = _gate_results_path(project_dir, requirement_name)
    results: dict[str, dict[str, str]] = {}
    if not path.exists():
        return results
    in_table = False
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if line == "| Artifact | Validation Result | Gate Result | Downstream Allowed | Reason |":
            in_table = True
            continue
        if in_table and not line.startswith("|"):
            break
        if in_table and line.startswith("|"):
            cols = [col.strip() for col in line.strip("|").split("|")]
            if len(cols) < 5:
                continue
            results[cols[0]] = {
                "validation_result": cols[1],
                "gate_result": cols[2],
                "downstream_allowed": cols[3],
                "reason": cols[4],
            }
    return results


def write_gate_results(
    project_dir: Path,
    requirement_name: str,
    requirement_id: str,
    catalog: list[dict[str, object]],
    gate_results: dict[str, dict[str, str]],
) -> Path:
    path = _gate_results_path(project_dir, requirement_name)
    lines = [
        "# Gate Results",
        "",
        "## Overview",
        f"- Project Name: {project_dir.name}",
        f"- Requirement Name: {requirement_name}",
        f"- Requirement ID: {requirement_id}",
        f"- Last Updated: {_today()}",
        "",
        "## Gate Table",
        "",
        "| Artifact | Validation Result | Gate Result | Downstream Allowed | Reason |",
        "|---------|-------------------|------------|--------------------|--------|",
    ]
    for item in catalog:
        name = str(item.get("name", "")).strip()
        if not name:
            continue
        row = gate_results.get(name, {})
        lines.append(
            "| "
            + " | ".join(
                [
                    name,
                    row.get("validation_result", "Not Run"),
                    row.get("gate_result", "Not Run"),
                    row.get("downstream_allowed", "No"),
                    row.get("reason", "-"),
                ]
            )
            + " |"
        )
    lines.append("")
    path.write_text("\n".join(lines), encoding="utf-8")
    return path


def ensure_artifact_status(
    project_dir: Path,
    requirement_name: str,
    requirement_id: str,
    catalog: list[dict[str, object]],
) -> Path:
    state = parse_artifact_status(project_dir, requirement_name, catalog)
    return write_artifact_status(project_dir, requirement_name, requirement_id, catalog, state)


def ensure_artifact_checklist(
    project_dir: Path,
    requirement_name: str,
    requirement_id: str,
    catalog: list[dict[str, object]],
) -> Path:
    output_dir = _PATHS.requirement_output_dir(project_dir, requirement_name)
    output_dir.mkdir(parents=True, exist_ok=True)
    path = output_dir / "artifact-checklist.md"
    if path.exists():
        return path

    lines = [
        "# Artifact Checklist",
        "",
        f"- Project Name: {project_dir.name}",
        f"- Requirement Name: {requirement_name}",
        f"- Requirement ID: {requirement_id}",
        "",
    ]
    for item in catalog:
        name = str(item.get("name", "")).strip()
        stage = str(item.get("stage", "")).strip()
        deps = item.get("dependencies", [])
        dep_text = "None"
        if isinstance(deps, list):
            dep_items = [str(dep).strip() for dep in deps if str(dep).strip()]
            if dep_items:
                dep_text = ", ".join(dep_items)
        if not name:
            continue
        lines.extend(
            [
                f"## {name}",
                f"- [ ] Stage confirmed: {stage}",
                f"- [ ] Dependencies confirmed: {dep_text}",
                "- [ ] Content quality reviewed",
                "- [ ] Gate status checked in artifact-status.md",
                "",
            ]
        )
    lines.append("<!-- TODO: Add optional owner sign-off checkbox if needed. -->")
    lines.append("")
    path.write_text("\n".join(lines), encoding="utf-8")
    return path


def _is_downstream_allowed(gate_result: str, allowed_states: list[str]) -> bool:
    return gate_result in allowed_states


def check_dependencies(
    artifact_name: str,
    catalog_index: dict[str, dict[str, object]],
    state: dict[str, dict[str, str]],
    gates_config: dict[str, dict[str, list[str]]] | None = None,
    override_gate: bool = False,
) -> tuple[bool, list[str]]:
    item = catalog_index.get(artifact_name, {})
    deps = item.get("dependencies", [])
    issues: list[str] = []
    config = gates_config or {}
    if isinstance(deps, list):
        for dep in deps:
            dep_name = str(dep).strip()
            dep_state = state.get(dep_name, {})
            gate_result = dep_state.get("gate", "N/A")
            approval_state = dep_state.get("approval", "Draft")
            dep_rules = config.get(
                dep_name,
                {"allow_downstream_if": ["Pass"], "allow_approval_if": ["Approved", "In Review"]},
            )
            allowed_gates = dep_rules.get("allow_downstream_if", ["Pass"])
            allowed_approval = dep_rules.get("allow_approval_if", ["Approved", "In Review"])
            if not _is_downstream_allowed(gate_result, allowed_gates):
                issues.append(f"{dep_name} gate '{gate_result}' not in allowed {allowed_gates}")
            if approval_state not in allowed_approval:
                issues.append(f"{dep_name} approval '{approval_state}' not in allowed {allowed_approval}")
    if override_gate and issues:
        return (True, ["Gate override applied: " + "; ".join(issues)])
    return (len(issues) == 0, issues)


def _validator_check(validator: str, content: str) -> tuple[str, str]:
    text = content.strip()
    lower = text.lower()

    if validator == "template-checker":
        if "## " not in text:
            return ("Fail", "Missing expected Markdown section headings.")
        return ("Pass", "Template structure is present.")

    if validator == "ambiguity-checker":
        vague_tokens = ["tbd", "to be decided", "unknown", "maybe", "approximately", "sometime"]
        hits = [token for token in vague_tokens if token in lower]
        if hits:
            return ("Warning", "Ambiguous wording found: " + ", ".join(hits))
        return ("Pass", "No obvious ambiguity markers found.")

    if validator == "completeness-checker":
        missing = []
        for token in ["##", "- "]:
            if token not in text:
                missing.append(token)
        if missing:
            return ("Fail", "Missing basic completeness markers.")
        if "TODO" in text:
            return ("Warning", "Contains TODO placeholders.")
        return ("Pass", "Basic completeness check passed.")

    if validator == "consistency-checker":
        if "mismatch" in lower or "conflict" in lower:
            return ("Fail", "Potential consistency conflict keywords found.")
        if "assumption" in lower:
            return ("Warning", "Contains assumptions that may need confirmation.")
        return ("Pass", "No obvious consistency issue markers found.")

    return ("Pass", f"No custom rule for {validator}, treated as pass.")


def evaluate_validators(validators: list[str], content: str) -> tuple[str, str]:
    if not validators:
        return ("Pass", "No validators configured.")
    worst = "Pass"
    notes: list[str] = []
    order = {"Pass": 0, "Warning": 1, "Fail": 2}

    for validator in validators:
        result, note = _validator_check(validator, content)
        notes.append(f"{validator}: {result}")
        if order[result] > order[worst]:
            worst = result
    return (worst, "; ".join(notes))


def detect_gate(
    artifact_name: str,
    content: str,
    validators: list[str] | None = None,
) -> tuple[str, str, str]:
    text = content.strip()
    if not text:
        return ("Fail", "Fail", "Generated content is empty.")

    # quick structural baseline
    baseline_tokens: dict[str, list[str]] = {
        "clarification": ["## Summary", "## Known Facts"],
        "brd": ["## Business Goals", "## Business Rules"],
        "process-bpmn": ["```mermaid"],
        "frs": ["## Main Flow", "## Alternative Flows", "## Business Rules"],
        "user-story": ["## Story", "## INVEST Check"],
        "acceptance-criteria": ["## Criteria"],
        "feature-list": ["## "],
        "wireframe": ["## Main Sections"],
        "ui": ["<html", "</html>"],
        "review": ["Validation Status"],
        "test-cases": ["| TC ID |"],
        "requirement-traceability-matrix": ["| Requirement ID |"],
        "requirement-traceability-flow": ["```mermaid"],
        "risk-notes": ["## Key Risks"],
        "dependency-map": ["## Dependency Table", "```mermaid"],
    }
    missing = [token for token in baseline_tokens.get(artifact_name, []) if token.lower() not in text.lower()]
    if missing:
        return ("Fail", "Fail", "Missing required tokens: " + ", ".join(missing))

    validation_result, validation_note = evaluate_validators(validators or [], text)
    if validation_result == "Fail":
        return (validation_result, "Fail", validation_note)
    if validation_result == "Warning":
        return (validation_result, "Warning", validation_note)
    return (validation_result, "Pass", validation_note)


def set_in_progress(state: dict[str, dict[str, str]], artifact_name: str) -> None:
    row = state.get(artifact_name, {})
    row["status"] = "In Progress"
    row["approval"] = "In Review"
    row["gate"] = "N/A"
    row["notes"] = "Running artifact generation."
    state[artifact_name] = row


def set_blocked(
    state: dict[str, dict[str, str]],
    artifact_name: str,
    reasons: list[str],
    override_used: bool = False,
) -> None:
    row = state.get(artifact_name, {})
    row["status"] = "Blocked"
    row["approval"] = "Blocked"
    row["gate"] = "Not Allowed"
    note = "; ".join(reasons) if reasons else "Dependency gate is not satisfied."
    if override_used:
        note = "Override used. " + note
    row["notes"] = note
    state[artifact_name] = row


def set_result(
    state: dict[str, dict[str, str]],
    artifact_name: str,
    gate: str,
    note: str,
    override_used: bool = False,
) -> None:
    row = state.get(artifact_name, {})
    if gate == "Pass":
        row["status"] = "Done"
        row["approval"] = "Approved"
    elif gate == "Warning":
        row["status"] = "In Review"
        row["approval"] = "In Review"
    else:
        row["status"] = "Rework Needed"
        row["approval"] = "Rework Needed"
    row["gate"] = gate
    row["notes"] = ("Override used. " if override_used else "") + note
    state[artifact_name] = row


def update_gate_result_row(
    gate_results: dict[str, dict[str, str]],
    artifact_name: str,
    validation_result: str,
    gate_result: str,
    downstream_allowed: bool,
    reason: str,
) -> None:
    gate_results[artifact_name] = {
        "validation_result": validation_result,
        "gate_result": gate_result,
        "downstream_allowed": "Yes" if downstream_allowed else "No",
        "reason": reason,
    }


def write_gate_report(
    project_dir: Path,
    requirement_name: str,
    requirement_id: str,
    catalog: list[dict[str, object]],
    state: dict[str, dict[str, str]],
) -> Path:
    output_dir = _PATHS.requirement_output_dir(project_dir, requirement_name)
    output_dir.mkdir(parents=True, exist_ok=True)
    path = output_dir / "gate-report.md"

    lines = [
        "# Gate Report",
        "",
        f"- Project Name: {project_dir.name}",
        f"- Requirement Name: {requirement_name}",
        f"- Requirement ID: {requirement_id}",
        f"- Last Updated: {_today()}",
        "",
        "| Artifact | Stage | Status | Approval | Gate | Notes |",
        "|---------|------|--------|----------|------|------|",
    ]
    blocked: list[str] = []
    for item in catalog:
        name = str(item.get("name", "")).strip()
        if not name:
            continue
        stage = str(item.get("stage", "")).strip()
        row = state.get(name, {})
        status = row.get("status", "Not Started")
        approval = row.get("approval", "Draft")
        gate = row.get("gate", "N/A")
        notes = row.get("notes", "-")
        lines.append(f"| {name} | {stage} | {status} | {approval} | {gate} | {notes} |")
        if status in {"Blocked", "Rework Needed"} or gate in {"Fail", "Not Allowed"}:
            blocked.append(name)

    lines.extend(["", "## Current Gate State"])
    if blocked:
        for item in blocked:
            lines.append(f"- Blocked artifact: {item}")
    else:
        lines.append("- No blocked artifact.")
    lines.append("")
    path.write_text("\n".join(lines), encoding="utf-8")
    return path


def describe_artifact_state(
    artifact_name: str,
    status: str,
    gate_result: str,
    approval_state: str,
) -> str:
    """Build a concise artifact state label for terminal logs."""
    return (
        f"{artifact_name} | status={status or 'Unknown'} "
        f"| gate={gate_result or 'N/A'} | approval={approval_state or 'Draft'}"
    )
