from __future__ import annotations

from datetime import datetime
from pathlib import Path
import importlib.util
import sys
from typing import Any


def _load_module(module_name: str, file_path: Path):
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Could not load module: {file_path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


_MAPPER = _load_module(
    "state_mapper_for_ops_docs_api",
    Path(__file__).resolve().parent / "state_mapper.py",
)
_PATHS = _load_module(
    "project_paths_for_ops_docs_api",
    Path(__file__).resolve().parents[1] / "project" / "project_paths.py",
)
_STALENESS = _load_module(
    "staleness_engine_for_ops_docs_api",
    Path(__file__).resolve().parent / "staleness_engine.py",
)
_SEMANTICS = _load_module(
    "semantic_mapper_for_ops_docs_api",
    Path(__file__).resolve().parents[1] / "project" / "semantic_mapper.py",
)


_ALLOWED_SUFFIX = {".md", ".txt", ".html"}


def _is_within(base: Path, target: Path) -> bool:
    try:
        target.resolve().relative_to(base.resolve())
        return True
    except ValueError:
        return False


def _clean_relative_path(relative_path: str) -> str:
    cleaned = relative_path.replace("\\", "/").strip().lstrip("/")
    if not cleaned:
        raise ValueError("Missing path.")
    if cleaned.startswith("../") or "/../" in cleaned:
        raise ValueError("Invalid relative path.")
    if cleaned.startswith("./"):
        cleaned = cleaned[2:]
    return cleaned


def _source_layer(relative: str) -> str:
    if relative.startswith("01-input/"):
        return "input"
    if relative.startswith("04-knowledge/"):
        return "knowledge"
    if relative.startswith("_ops/"):
        return "ops"
    if relative.startswith("02-output/"):
        return "curated-output"
    return "other"


def _group_from_relative(relative: str) -> str:
    if relative.startswith("01-input/requirements/"):
        return "01-input/requirements"
    if relative.startswith("01-input/notes/"):
        return "01-input/notes"
    if relative.startswith("04-knowledge/"):
        return "04-knowledge"
    if relative == "_ops/decision-log.md":
        return "_ops/decision-log.md"
    if relative.startswith("_ops/confirmations/") and relative.endswith(".md"):
        return "_ops/confirmations/*.md"
    if relative.startswith("02-output/ba/"):
        return "02-output/ba"
    if relative.startswith("02-output/design/"):
        return "02-output/design"
    if relative.startswith("02-output/fe/"):
        return "02-output/fe"
    return "other"


def _doc_type_from_path(path: Path) -> str:
    name = path.name.lower()
    suffix = path.suffix.lower()
    if suffix == ".html":
        return "html"
    if "requirement" in name or name.startswith("req-"):
        return "requirement"
    if "business-rules" in name:
        return "business-rules"
    if "decision-log" in name:
        return "decision-log"
    if "confirmation" in name:
        return "confirmation-log"
    if "note" in name:
        return "notes"
    return "markdown"


def _is_editable(relative: str) -> bool:
    if relative.startswith("01-input/requirements/"):
        return True
    if relative.startswith("01-input/notes/"):
        return True
    if relative == "04-knowledge/business-rules.md":
        return True
    if relative == "04-knowledge/notes.md":
        return True
    if relative == "_ops/decision-log.md":
        return True
    if relative.startswith("_ops/confirmations/") and relative.endswith(".md"):
        return True
    return False


def _protected_reason(relative: str) -> str:
    if relative.startswith("_ops/runtime/"):
        return "Protected runtime state file."
    if relative.startswith("_ops/generated/"):
        return "Protected generated runtime file."
    if "gate-results.md" in relative or "gate-report.md" in relative:
        return "Protected gate file."
    if relative.startswith("02-output/"):
        return "Curated output is view-only in Phase 3B."
    return "Document is view-only in Phase 3B."


def _discover_documents(project_dir: Path) -> list[dict[str, Any]]:
    candidates: list[Path] = []

    roots = [
        _PATHS.requirements_dir(project_dir),
        _PATHS.notes_dir(project_dir),
        _PATHS.knowledge_dir(project_dir),
        _PATHS.confirmations_dir(project_dir),
        _PATHS.curated_ba_dir(project_dir),
        _PATHS.curated_design_dir(project_dir),
        _PATHS.curated_fe_dir(project_dir),
    ]
    for root in roots:
        if not root.exists():
            continue
        for path in sorted(root.rglob("*")):
            if path.is_file() and path.suffix.lower() in _ALLOWED_SUFFIX:
                candidates.append(path)

    decision_log = _PATHS.decision_log_path(project_dir)
    if decision_log.exists():
        candidates.append(decision_log)

    docs: list[dict[str, Any]] = []
    seen: set[str] = set()
    for path in sorted(candidates):
        relative = str(path.relative_to(project_dir)).replace("\\", "/")
        group = _group_from_relative(relative)
        if group == "other":
            continue
        if relative in seen:
            continue
        seen.add(relative)
        stat = path.stat()
        editable = _is_editable(relative)
        docs.append(
            {
                "file_path": relative,
                "group": group,
                "doc_type": _doc_type_from_path(path),
                "editable": editable,
                "view_only": not editable,
                "source_layer": _source_layer(relative),
                "last_modified": datetime.fromtimestamp(stat.st_mtime).strftime("%Y-%m-%d %H:%M:%S"),
                "size_bytes": stat.st_size,
            }
        )
    return docs


def _state_for_documents(project_dir: Path, docs: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    state = _STALENESS.load_state(project_dir)
    by_path: dict[str, dict[str, Any]] = {}
    changed = False
    documents = state.get("documents", {})
    if not isinstance(documents, dict):
        documents = {}
        state["documents"] = documents
    for doc in docs:
        relative = str(doc.get("file_path", "")).strip()
        if not relative:
            continue
        before = dict(documents.get(relative, {})) if isinstance(documents.get(relative, {}), dict) else {}
        evaluated = _STALENESS.evaluate_document(project_dir, state, relative)
        by_path[relative] = evaluated
        after = dict(documents.get(relative, {})) if isinstance(documents.get(relative, {}), dict) else {}
        if before != after:
            changed = True
    if changed:
        _STALENESS.save_state(project_dir, state)
    return by_path


def _resolve_target(project_dir: Path, relative_path: str) -> tuple[Path, str]:
    cleaned = _clean_relative_path(relative_path)
    target = (project_dir / cleaned).resolve()
    if not _is_within(project_dir, target):
        raise ValueError("Invalid relative path.")
    if not target.exists() or not target.is_file():
        raise ValueError("Document not found.")
    if target.suffix.lower() not in _ALLOWED_SUFFIX:
        raise ValueError("Unsupported file type.")
    return target, cleaned


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _write_text_preserve_newline(path: Path, content: str) -> None:
    existing = _read_text(path)
    newline = "\r\n" if "\r\n" in existing else "\n"
    normalized = content.replace("\r\n", "\n").replace("\r", "\n")
    if newline == "\r\n":
        normalized = normalized.replace("\n", "\r\n")
    path.write_text(normalized, encoding="utf-8")


def _append_edit_audit(project_dir: Path, relative: str, byte_size: int) -> None:
    audit_path = _PATHS.ops_dir(project_dir) / "ops-console-edits.log"
    audit_path.parent.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with audit_path.open("a", encoding="utf-8") as handle:
        handle.write(f"{stamp} | edited | {relative} | bytes={byte_size}\n")


def get_documents(base_dir: Path, project_name: str, group_filter: str = "all") -> dict[str, Any]:
    project_dir = _MAPPER.resolve_project_dir(base_dir, project_name)
    docs = _discover_documents(project_dir)
    state_by_path = _state_for_documents(project_dir, docs)
    enriched: list[dict[str, Any]] = []
    for doc in docs:
        relative = str(doc.get("file_path", "")).strip()
        snapshot = state_by_path.get(relative, {})
        enriched.append(
            {
                **doc,
                "stale_state": _SEMANTICS.normalize_stale_state(str(snapshot.get("stale_state", "fresh"))),
                "manual_override": bool(snapshot.get("manual_override", False)),
                "rerun_recommendation": str(snapshot.get("rerun_recommendation", "none")),
                "impacted_artifacts": list(snapshot.get("impacted_artifacts", [])),
                "impacted_stages": list(snapshot.get("impacted_stages", [])),
                "impacted_requirements": list(snapshot.get("impacted_requirements", [])),
            }
        )
    docs = enriched
    groups = sorted({doc["group"] for doc in docs})
    selected = group_filter.strip() if group_filter.strip() else "all"
    if selected != "all":
        docs = [doc for doc in docs if doc["group"] == selected]
    counts = _STALENESS.summary_counts(project_dir)
    return {
        "project": project_name,
        "groups": groups,
        "group_filter": selected,
        "documents": docs,
        "stale_items_count": counts["stale_items_count"],
        "needs_rerun_items_count": counts["needs_rerun_items_count"],
        "mode": "phase-3a",
    }


def get_document_preview(base_dir: Path, project_name: str, relative_path: str) -> dict[str, Any]:
    project_dir = _MAPPER.resolve_project_dir(base_dir, project_name)
    target, cleaned = _resolve_target(project_dir, relative_path)
    text = _read_text(target)
    relative = cleaned.replace("\\", "/")
    editable = _is_editable(relative)
    stat = target.stat()
    state = _STALENESS.load_state(project_dir)
    snapshot = _STALENESS.evaluate_document(project_dir, state, relative, content_for_analysis=text)
    _STALENESS.save_state(project_dir, state)
    return {
        "project": project_name,
        "preview": {
            "file_path": relative,
            "group": _group_from_relative(relative),
            "doc_type": _doc_type_from_path(target),
            "editable": editable,
            "view_only": not editable,
            "protected": not editable,
            "protected_reason": "" if editable else _protected_reason(relative),
            "source_layer": _source_layer(relative),
            "last_modified": datetime.fromtimestamp(stat.st_mtime).strftime("%Y-%m-%d %H:%M:%S"),
            "line_count": len(text.splitlines()),
            "size_bytes": stat.st_size,
            "stale_state": _SEMANTICS.normalize_stale_state(str(snapshot.get("stale_state", "fresh"))),
            "manual_override": bool(snapshot.get("manual_override", False)),
            "rerun_recommendation": str(snapshot.get("rerun_recommendation", "none")),
            "impacted_artifacts": list(snapshot.get("impacted_artifacts", [])),
            "impacted_stages": list(snapshot.get("impacted_stages", [])),
            "impacted_requirements": list(snapshot.get("impacted_requirements", [])),
            "impact_reason": list(snapshot.get("reason", [])),
            "content": text,
        },
    }


def save_document(base_dir: Path, payload: dict[str, Any]) -> dict[str, Any]:
    project_name = str(payload.get("project", "")).strip()
    relative_path = str(payload.get("path", "")).strip()
    content = payload.get("content")

    if not project_name:
        raise ValueError("Missing project.")
    if not relative_path:
        raise ValueError("Missing path.")
    if not isinstance(content, str):
        raise ValueError("Missing content.")

    project_dir = _MAPPER.resolve_project_dir(base_dir, project_name)
    cleaned = _clean_relative_path(relative_path)
    relative = cleaned.replace("\\", "/")

    # Reject protected/view-only scope before touching file content checks.
    if relative.startswith("_ops/runtime/") or relative.startswith("_ops/generated/"):
        raise ValueError(_protected_reason(relative))
    if "gate-results.md" in relative or "gate-report.md" in relative:
        raise ValueError(_protected_reason(relative))
    if relative.startswith("02-output/"):
        raise ValueError(_protected_reason(relative))
    if not _is_editable(relative):
        raise ValueError(_protected_reason(relative))

    target, _ = _resolve_target(project_dir, cleaned)

    _write_text_preserve_newline(target, content)
    _append_edit_audit(project_dir, relative, len(content.encode("utf-8")))
    state = _STALENESS.load_state(project_dir)
    snapshot = _STALENESS.mark_document_edited(
        project_dir,
        state,
        relative,
        content_for_analysis=content,
    )
    _STALENESS.save_state(project_dir, state)

    stat = target.stat()
    return {
        "saved": True,
        "project": project_name,
        "file_path": relative,
        "metadata": {
            "doc_type": _doc_type_from_path(target),
            "editable": True,
            "source_layer": _source_layer(relative),
            "last_modified": datetime.fromtimestamp(stat.st_mtime).strftime("%Y-%m-%d %H:%M:%S"),
            "line_count": len(content.splitlines()),
            "size_bytes": stat.st_size,
            "stale_state": str(snapshot.get("stale_state", "fresh")),
            "manual_override": bool(snapshot.get("manual_override", False)),
            "rerun_recommendation": str(snapshot.get("rerun_recommendation", "none")),
            "impacted_artifacts": list(snapshot.get("impacted_artifacts", [])),
            "impacted_stages": list(snapshot.get("impacted_stages", [])),
            "impacted_requirements": list(snapshot.get("impacted_requirements", [])),
            "impact_reason": list(snapshot.get("reason", [])),
        },
    }
