from __future__ import annotations

from datetime import datetime
from pathlib import Path
import importlib.util
import re
import sys
from typing import Any

try:
    import yaml
except ImportError:
    yaml = None


STATE_VERSION = "1"
DEFAULT_STAGES = ["ba-core", "design", "fe-prototype"]
DEFAULT_REQ_ARTIFACTS = [
    "brd",
    "process-bpmn",
    "frs",
    "user-story",
    "acceptance-criteria",
    "feature-list",
    "wireframe",
    "ui",
]
REQ_TOKEN = re.compile(r"\b(req-\d+)\b", re.IGNORECASE)
_IMPACT_REQUIRED_KEYS = {
    "kind",
    "requirements",
    "artifacts",
    "stages",
    "reason",
    "recommendation",
}
_IMPACT_ALLOWED_KINDS = {"none", "review-state", "requires-rerun"}


def _load_module(module_name: str, file_path: Path):
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Could not load module: {file_path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


_PATHS = _load_module(
    "project_paths_for_ops_console_staleness_engine",
    Path(__file__).resolve().parents[1] / "project" / "project_paths.py",
)


def _now() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def _parse_time(value: str) -> datetime | None:
    text = str(value or "").strip()
    if not text:
        return None
    for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%d"):
        try:
            return datetime.strptime(text, fmt)
        except ValueError:
            continue
    return None


def _read_yaml(path: Path) -> dict[str, Any]:
    if yaml is None or not path.exists():
        return {}
    raw = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    return raw if isinstance(raw, dict) else {}


def _write_yaml(path: Path, payload: dict[str, Any]) -> None:
    if yaml is None:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(yaml.safe_dump(payload, sort_keys=False, allow_unicode=False), encoding="utf-8")


def _read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8")


def _parse_artifact_status_rows(path: Path) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    in_table = False
    for raw_line in _read_text(path).splitlines():
        line = raw_line.strip()
        if line == "| Artifact | Stage | Owner | Status | Approval State | Gate | Notes |":
            in_table = True
            continue
        if in_table and not line.startswith("|"):
            break
        if in_table and line.startswith("|"):
            cols = [col.strip() for col in line.strip("|").split("|")]
            if len(cols) < 7:
                continue
            if cols[0] in {"Artifact", "---------"}:
                continue
            rows.append(
                {
                    "artifact": cols[0],
                    "stage": cols[1],
                    "status": cols[3],
                }
            )
    return rows


def _empty_state() -> dict[str, Any]:
    return {"version": STATE_VERSION, "updated_at": _now(), "documents": {}}


def load_state(project_dir: Path) -> dict[str, Any]:
    path = _PATHS.ops_console_staleness_path(project_dir)
    payload = _read_yaml(path)
    if not isinstance(payload, dict):
        payload = {}
    if "documents" not in payload or not isinstance(payload.get("documents"), dict):
        payload["documents"] = {}
    if "version" not in payload:
        payload["version"] = STATE_VERSION
    if "updated_at" not in payload:
        payload["updated_at"] = _now()
    return payload


def save_state(project_dir: Path, payload: dict[str, Any]) -> None:
    normalized = payload if isinstance(payload, dict) else _empty_state()
    if "documents" not in normalized or not isinstance(normalized.get("documents"), dict):
        normalized["documents"] = {}
    normalized["version"] = STATE_VERSION
    normalized["updated_at"] = _now()
    _write_yaml(_PATHS.ops_console_staleness_path(project_dir), normalized)


def _processing_last_processed_map(project_dir: Path) -> dict[str, datetime | None]:
    state = _read_yaml(_PATHS.processing_state_path(project_dir))
    reqs = state.get("requirements", {}) if isinstance(state, dict) else {}
    if not isinstance(reqs, dict):
        reqs = {}
    result: dict[str, datetime | None] = {}
    for name, row in reqs.items():
        if not isinstance(row, dict):
            continue
        stem = str(name).strip()
        if stem.endswith(".md"):
            stem = stem[:-3]
        result[stem] = _parse_time(str(row.get("last_processed_at", "")))
    return result


def _discover_known_requirements(project_dir: Path) -> list[str]:
    names: set[str] = set()
    processing = _processing_last_processed_map(project_dir)
    names.update(processing.keys())

    req_dir = _PATHS.requirements_dir(project_dir)
    if req_dir.exists():
        for path in req_dir.iterdir():
            if path.is_file() and path.suffix.lower() in {".md", ".txt"}:
                names.add(path.stem)

    gen_root = _PATHS.generated_root(project_dir)
    if gen_root.exists():
        for path in gen_root.iterdir():
            if path.is_dir():
                names.add(path.name)

    return sorted(name for name in names if name)


def _find_req_tokens(relative_path: str, content: str = "") -> list[str]:
    tokens = {match.group(1).lower() for match in REQ_TOKEN.finditer(f"{relative_path}\n{content}")}
    return sorted(tokens)


def _impact_from_requirement(project_dir: Path, requirement_name: str) -> tuple[list[str], list[str]]:
    req_dir = _PATHS.requirement_output_dir(project_dir, requirement_name)
    rows = _parse_artifact_status_rows(req_dir / "artifact-status.md")
    artifacts = sorted({str(row.get("artifact", "")).strip() for row in rows if str(row.get("artifact", "")).strip()})
    stages = sorted({str(row.get("stage", "")).strip() for row in rows if str(row.get("stage", "")).strip()})
    if not artifacts:
        artifacts = list(DEFAULT_REQ_ARTIFACTS)
    if not stages:
        stages = list(DEFAULT_STAGES)
    return artifacts, stages


def _merge_impacts(project_dir: Path, requirements: list[str]) -> tuple[list[str], list[str]]:
    artifact_set: set[str] = set()
    stage_set: set[str] = set()
    for requirement_name in requirements:
        artifacts, stages = _impact_from_requirement(project_dir, requirement_name)
        artifact_set.update(artifacts)
        stage_set.update(stages)
    if not artifact_set:
        artifact_set.update(DEFAULT_REQ_ARTIFACTS)
    if not stage_set:
        stage_set.update(DEFAULT_STAGES)
    return sorted(artifact_set), sorted(stage_set)


def _impact_rule(project_dir: Path, relative_path: str, content: str = "") -> dict[str, Any]:
    relative = relative_path.replace("\\", "/").strip()
    known_requirements = _discover_known_requirements(project_dir)

    if relative.startswith("01-input/requirements/"):
        requirement = Path(relative).stem.lower()
        requirements = [requirement] if requirement else []
        artifacts, stages = _merge_impacts(project_dir, requirements)
        return {
            "kind": "requires-rerun",
            "requirements": requirements,
            "artifacts": artifacts,
            "stages": stages,
            "reason": [f"Requirement update can affect BA/Design/FE outputs for {requirement or 'target requirement'}."],
            "recommendation": (
                f"needs-rerun: requirement {requirement} from stage ba-core"
                if requirement
                else "needs-rerun: requirement from stage ba-core"
            ),
        }

    if relative.startswith("01-input/notes/"):
        tokens = _find_req_tokens(relative, content)
        requirements = tokens if tokens else known_requirements
        artifacts, stages = _merge_impacts(project_dir, requirements)
        if len(requirements) == 1:
            recommendation = f"needs-rerun: requirement {requirements[0]} from stage ba-core"
        else:
            recommendation = "needs-rerun: project-level BA/Design/FE artifacts due to input notes change"
        return {
            "kind": "requires-rerun",
            "requirements": requirements,
            "artifacts": artifacts,
            "stages": stages,
            "reason": ["Input notes update can affect BA/Design/FE outputs."],
            "recommendation": recommendation,
        }

    if relative in {"04-knowledge/business-rules.md", "04-knowledge/notes.md"}:
        requirements = known_requirements
        artifacts, stages = _merge_impacts(project_dir, requirements)
        source = "business-rules" if relative.endswith("business-rules.md") else "knowledge notes"
        return {
            "kind": "requires-rerun",
            "requirements": requirements,
            "artifacts": artifacts,
            "stages": stages,
            "reason": [f"{source} update can affect BA/Design/FE outputs across the project."],
            "recommendation": f"needs-rerun: project-level BA/Design/FE artifacts due to {source} change",
        }

    if relative == "_ops/decision-log.md" or (
        relative.startswith("_ops/confirmations/") and relative.endswith(".md")
    ):
        return {
            "kind": "review-state",
            "requirements": [],
            "artifacts": [],
            "stages": [],
            "reason": ["Decision/confirmation update can affect blocker visibility and recommendation state."],
            "recommendation": "stale: review blocker visibility and confirmation consistency",
        }

    return {
        "kind": "none",
        "requirements": [],
        "artifacts": [],
        "stages": [],
        "reason": ["No downstream impact rule."],
        "recommendation": "none",
    }


def _validate_impact(impact: dict[str, Any]) -> dict[str, Any]:
    """
    Keep impact payload shape strict so stale/recommendation logic does not
    silently drift if future edits introduce malformed dictionaries.
    """
    if not isinstance(impact, dict):
        return {
            "kind": "none",
            "requirements": [],
            "artifacts": [],
            "stages": [],
            "reason": ["Invalid impact payload. Fallback to no downstream impact."],
            "recommendation": "none",
        }
    missing = [key for key in _IMPACT_REQUIRED_KEYS if key not in impact]
    if missing:
        return {
            "kind": "none",
            "requirements": [],
            "artifacts": [],
            "stages": [],
            "reason": [f"Impact payload missing keys: {', '.join(sorted(missing))}."],
            "recommendation": "none",
        }
    if str(impact.get("kind", "")).strip() not in _IMPACT_ALLOWED_KINDS:
        return {
            "kind": "none",
            "requirements": [],
            "artifacts": [],
            "stages": [],
            "reason": ["Impact payload kind is invalid. Fallback to no downstream impact."],
            "recommendation": "none",
        }

    validated = dict(impact)
    for key in ("requirements", "artifacts", "stages", "reason"):
        value = validated.get(key)
        if not isinstance(value, list):
            validated[key] = []
    validated["recommendation"] = str(validated.get("recommendation", "none"))
    return validated


def _all_processed_after_edit(project_dir: Path, requirements: list[str], edit_at: datetime) -> bool:
    if not requirements:
        return False
    processed = _processing_last_processed_map(project_dir)
    for requirement_name in requirements:
        stamp = processed.get(requirement_name.lower())
        if stamp is None:
            return False
        if stamp < edit_at:
            return False
    return True


def evaluate_document(
    project_dir: Path,
    state: dict[str, Any],
    relative_path: str,
    content_for_analysis: str = "",
) -> dict[str, Any]:
    documents = state.get("documents", {})
    if not isinstance(documents, dict):
        documents = {}
        state["documents"] = documents
    relative = relative_path.replace("\\", "/").strip()
    current = documents.get(relative, {})
    if not isinstance(current, dict):
        current = {}
    manual_override = bool(current.get("manual_override", False))
    last_edit_text = str(current.get("last_edit_at", "")).strip()
    last_edit_at = _parse_time(last_edit_text)
    impact = _validate_impact(_impact_rule(project_dir, relative, content=content_for_analysis))

    stale_state = "fresh"
    recommendation = "none"
    reason = impact["reason"]
    if manual_override:
        stale_state = "manual-override"
        recommendation = str(current.get("rerun_recommendation", "")).strip() or impact["recommendation"]
    elif last_edit_at:
        if impact["kind"] == "review-state":
            stale_state = "stale"
            recommendation = impact["recommendation"]
        elif impact["kind"] == "requires-rerun":
            if _all_processed_after_edit(project_dir, impact["requirements"], last_edit_at):
                stale_state = "fresh"
                recommendation = "none"
            else:
                stale_state = "needs-rerun"
                recommendation = impact["recommendation"]

    evaluated = {
        "stale_state": stale_state,
        "manual_override": manual_override,
        "rerun_recommendation": recommendation,
        "impacted_requirements": impact["requirements"],
        "impacted_artifacts": impact["artifacts"],
        "impacted_stages": impact["stages"],
        "reason": reason,
        "last_edit_at": last_edit_text,
    }
    changed = False
    for key, value in evaluated.items():
        if current.get(key) != value:
            changed = True
            break
    evaluated["last_evaluated_at"] = _now() if changed else str(current.get("last_evaluated_at", ""))
    documents[relative] = {**current, **evaluated}
    return evaluated


def mark_document_edited(
    project_dir: Path,
    state: dict[str, Any],
    relative_path: str,
    content_for_analysis: str = "",
) -> dict[str, Any]:
    documents = state.get("documents", {})
    if not isinstance(documents, dict):
        documents = {}
        state["documents"] = documents
    relative = relative_path.replace("\\", "/").strip()
    existing = documents.get(relative, {})
    if not isinstance(existing, dict):
        existing = {}
    existing["last_edit_at"] = _now()
    documents[relative] = existing
    return evaluate_document(project_dir, state, relative, content_for_analysis=content_for_analysis)


def summary_counts(project_dir: Path, state: dict[str, Any] | None = None) -> dict[str, int]:
    payload = state if isinstance(state, dict) else load_state(project_dir)
    docs = payload.get("documents", {})
    if not isinstance(docs, dict):
        return {"stale_items_count": 0, "needs_rerun_items_count": 0}

    stale_items = 0
    needs_rerun = 0
    for entry in docs.values():
        if not isinstance(entry, dict):
            continue
        state_value = str(entry.get("stale_state", "fresh")).strip().lower()
        if state_value in {"stale", "needs-rerun", "manual-override"}:
            stale_items += 1
        if state_value == "needs-rerun":
            needs_rerun += 1
    return {
        "stale_items_count": stale_items,
        "needs_rerun_items_count": needs_rerun,
    }
