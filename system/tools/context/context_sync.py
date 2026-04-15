from __future__ import annotations

from datetime import datetime
import importlib.util
from pathlib import Path
import sys

AUTO_SYNC_START = "<!-- AUTO-SYNC:START -->"
AUTO_SYNC_END = "<!-- AUTO-SYNC:END -->"


def _load_module(module_name: str, file_path: Path):
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Could not load module: {file_path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


_DIFF_MODULE = _load_module(
    "context_diff_report_for_sync",
    Path(__file__).resolve().parent / "context_diff_report.py",
)
_CONSOLE_LOGGER = _load_module(
    "console_logger_for_context_sync",
    Path(__file__).resolve().parents[1] / "logging" / "console_logger.py",
)


def _now_iso() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def _read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8")


def _write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def _ensure_auto_sync_block(existing_text: str, generated_block: str) -> str:
    generated_block = generated_block.strip()
    new_block = f"{AUTO_SYNC_START}\n{generated_block}\n{AUTO_SYNC_END}"
    if AUTO_SYNC_START in existing_text and AUTO_SYNC_END in existing_text:
        start = existing_text.index(AUTO_SYNC_START)
        end = existing_text.index(AUTO_SYNC_END) + len(AUTO_SYNC_END)
        return existing_text[:start] + new_block + existing_text[end:]

    base = existing_text.rstrip()
    if base:
        return f"{base}\n\n{new_block}\n"
    return f"{new_block}\n"


def _read_catalog_and_gates(base_dir: Path) -> tuple[list[dict[str, object]], dict[str, dict[str, list[str]]]]:
    runner_path = base_dir / "system" / "tools" / "project" / "artifact_runner.py"
    artifact_runner = _load_module("artifact_runner_for_context_sync", runner_path)
    catalog = artifact_runner.load_artifact_catalog(base_dir / "system" / "artifacts" / "artifact-catalog.yaml")
    gates = artifact_runner.load_gates_config(base_dir / "system" / "configs" / "gates.yaml")
    return catalog, gates


def _artifact_model_section(
    catalog: list[dict[str, object]],
    gates: dict[str, dict[str, list[str]]],
) -> str:
    stages: dict[str, list[str]] = {}
    for item in catalog:
        stage = str(item.get("stage", "")).strip() or "unknown"
        stages.setdefault(stage, []).append(str(item.get("name", "")).strip())

    lines = [
        "## Level 1 Auto-Synced Artifact Model",
        "",
        "### Stage Mapping",
    ]
    for stage_name, artifacts in stages.items():
        lines.append(f"- `{stage_name}`: {', '.join([a for a in artifacts if a])}")

    lines.extend(
        [
            "",
            "### Artifact Catalog Summary",
            "",
            "| Artifact | Stage | Owner | Dependencies | Outputs | Gate Required |",
            "|---------|-------|-------|--------------|---------|---------------|",
        ]
    )
    for item in catalog:
        name = str(item.get("name", "")).strip()
        stage = str(item.get("stage", "")).strip()
        owner = str(item.get("owner", "")).strip()
        deps_raw = item.get("dependencies", [])
        deps = ", ".join([str(dep).strip() for dep in deps_raw]) if isinstance(deps_raw, list) and deps_raw else "None"
        outputs_raw = item.get("outputs", [])
        outputs = ", ".join([str(out).strip() for out in outputs_raw]) if isinstance(outputs_raw, list) and outputs_raw else "-"
        gate_required = str(item.get("gate_required", True))
        lines.append(f"| {name} | {stage} | {owner} | {deps} | {outputs} | {gate_required} |")

    lines.extend(
        [
            "",
            "### Gate and Approval Rules (from system/configs/gates.yaml)",
            "",
            "| Artifact | Allowed Gate Results | Allowed Approval States |",
            "|---------|----------------------|-------------------------|",
        ]
    )
    for item in catalog:
        name = str(item.get("name", "")).strip()
        rules = gates.get(name, {})
        allow_gate = ", ".join(rules.get("allow_downstream_if", ["Pass"]))
        allow_approval = ", ".join(rules.get("allow_approval_if", ["Approved", "In Review"]))
        lines.append(f"| {name} | {allow_gate} | {allow_approval} |")

    lines.extend(
        [
            "",
            "<!-- TODO: Add lightweight artifact-level quality score when needed. -->",
        ]
    )
    return "\n".join(lines)


def _context_summary_section(catalog: list[dict[str, object]]) -> str:
    artifact_names = [str(item.get("name", "")).strip() for item in catalog if str(item.get("name", "")).strip()]
    stage_names: list[str] = []
    for item in catalog:
        stage = str(item.get("stage", "")).strip()
        if stage and stage not in stage_names:
            stage_names.append(stage)

    lines = [
        "## Level 1 Auto-Synced Summary",
        "",
        "### Current System Snapshot",
        "- Project-based pipeline under `projects/<project-name>/...`.",
        "- BA-led artifact generation with UXUI, FE, and Reviewer stages.",
        f"- Artifact count: {len(artifact_names)}.",
        f"- Stages: {', '.join(stage_names)}.",
        "",
        "### Execution Model",
        "- Full mode: generate all artifacts in dependency order.",
        "- Controlled mode: run by artifact/stage with gate + approval checks.",
        "- Governance files per requirement:",
        "  - `artifact-status.md`",
        "  - `artifact-checklist.md`",
        "  - `gate-results.md`",
        "  - `gate-report.md`",
        "  - `artifact-reviews/*.md`",
        "",
        "### Gate and Approval Model",
        "- Gate states: Pass, Warning, Fail, Not Allowed.",
        "- Approval states: Draft, In Review, Approved, Rework Needed, Blocked.",
        "- Downstream execution depends on both gate and approval rules in `system/configs/gates.yaml`.",
        "",
        "### Quick Links",
        "- [artifact-model.md](./artifact-model.md)",
        "- [workflow-playbook.md](./workflow-playbook.md)",
        "- [load-profiles.md](./load-profiles.md)",
        "- [output-standards.md](./output-standards.md)",
        "- [id-system.md](./id-system.md)",
        "",
        "<!-- TODO: Add sample command snippets for common controlled-run cases. -->",
    ]
    return "\n".join(lines)


def _workflow_playbook_section(catalog: list[dict[str, object]]) -> str:
    stages: dict[str, list[str]] = {}
    for item in catalog:
        stage = str(item.get("stage", "")).strip() or "unknown"
        stages.setdefault(stage, []).append(str(item.get("name", "")).strip())

    lines = [
        "## Level 1 Auto-Synced Playbook View",
        "",
        "### High-Level Project Flow",
        "1. Read requirement input from `projects/<project-name>/01-input/requirements/`.",
        "2. Run BA artifacts.",
        "3. Run UXUI artifact (`wireframe`).",
        "4. Run FE artifact (`ui`).",
        "5. Run review/quality artifacts.",
        "6. Write outputs to `projects/<project-name>/_ops/generated/<requirement-name>/` and curated copies in `02-output/`.",
        "7. Update project status and dashboards.",
        "",
        "### Stage Flow (from artifact catalog)",
    ]
    for stage_name, artifacts in stages.items():
        lines.append(f"- `{stage_name}`: {', '.join([a for a in artifacts if a])}")

    lines.extend(
        [
            "",
            "### Artifact Execution Logic",
            "- Full run mode uses dependency order.",
            "- Controlled run mode supports `--artifact` and `--stage`.",
            "- Existing outputs can be skipped unless `--force` is used.",
            "",
            "### Gate-Aware Flow",
            "- Before each artifact, dependency gate and approval are checked.",
            "- If not allowed, artifact is marked blocked/not allowed.",
            "- Optional `--override-gate` allows manual continuation with notes.",
            "",
            "<!-- TODO: Add a compact visual snippet linking stages to gate checkpoints. -->",
        ]
    )
    return "\n".join(lines)


def _load_profiles_section() -> str:
    return "\n".join(
        [
            "## Level 1 Auto-Synced Load Profiles",
            "",
            "### BA-basic",
            "- `system/context/context-summary.md`",
            "- `system/context/workflow-playbook.md`",
            "- `system/context/output-standards.md`",
            "- `system/context/id-system.md`",
            "",
            "### BA-full",
            "- `system/context/context-summary.md`",
            "- `system/context/artifact-model.md`",
            "- `system/context/workflow-playbook.md`",
            "- `system/context/output-standards.md`",
            "- `system/context/output-checklists.md`",
            "- `system/context/anti-patterns.md`",
            "",
            "### review",
            "- `system/context/context-summary.md`",
            "- `system/context/output-standards.md`",
            "- `system/context/output-checklists.md`",
            "- `system/context/anti-patterns.md`",
            "",
            "### traceability",
            "- `system/context/context-summary.md`",
            "- `system/context/traceability-rules.md`",
            "- `system/context/id-system.md`",
            "- `system/context/output-standards.md`",
            "",
            "### execution-control",
            "- `system/context/context-summary.md`",
            "- `system/context/artifact-model.md`",
            "- `system/context/workflow-playbook.md`",
            "- `system/artifacts/artifact-catalog.yaml`",
            "- `system/configs/gates.yaml`",
            "",
            "<!-- TODO: Add a small profile for dashboard-only maintenance. -->",
        ]
    )


def _update_with_auto_sync(path: Path, generated_block: str, default_title: str) -> dict[str, object]:
    old_text = _read_text(path)
    if not old_text.strip():
        old_text = f"# {default_title}\n\nThis file supports safe context sync using AUTO-SYNC markers.\n"
    new_text = _ensure_auto_sync_block(old_text, generated_block)
    updated = new_text != old_text
    if updated:
        _write_text(path, new_text)
    summary = _DIFF_MODULE.summarize_text_change(old_text, new_text)
    return {"path": path, "updated": updated, "summary": summary}


def _append_change_log(context_dir: Path, results: list[dict[str, object]]) -> None:
    path = context_dir / "change-log.md"
    previous = _read_text(path).rstrip()
    updated_files = [str(item["path"].name) for item in results if item["updated"]]
    entry_lines = [
        "",
        f"## Context Sync ({_now_iso()})",
        "- Scope: Level 1 safe auto-sync",
        f"- Updated files: {', '.join(updated_files) if updated_files else 'None'}",
        "- Notes: Only AUTO-SYNC sections were updated.",
    ]
    _write_text(path, previous + "\n" + "\n".join(entry_lines) + "\n")


def _append_sync_log(logs_dir: Path, results: list[dict[str, object]]) -> None:
    path = logs_dir / "context-sync.log"
    lines = [f"[{_now_iso()}] Level 1 context sync started"]
    for item in results:
        status = "UPDATED" if item["updated"] else "UNCHANGED"
        lines.append(f"[{_now_iso()}] {status} {item['path']}")
    lines.append(f"[{_now_iso()}] Level 1 context sync completed")
    _write_text(path, _read_text(path) + "\n".join(lines) + "\n")


def _write_sync_report(context_dir: Path, results: list[dict[str, object]]) -> Path:
    report_path = context_dir / "context-sync-report.md"
    updated_files = [item for item in results if item["updated"]]
    unchanged_files = [item for item in results if not item["updated"]]
    manual_review_candidates = [
        "system/context/traceability-rules.md",
        "system/context/id-system.md",
        "system/context/output-standards.md",
        "system/context/test-case-rules.md",
        "system/context/versioning-rules.md",
        "system/context/dependency-rules.md",
        "system/context/risk-rules.md",
        "system/context/anti-patterns.md",
        "system/context/output-checklists.md",
    ]

    lines = [
        "# Context Sync Report",
        "",
        f"- Run Time: {_now_iso()}",
        "- Sync Level: Level 1 (safe/conservative)",
        "",
        "## Source of Truth Used",
        "- `system/artifacts/artifact-catalog.yaml`",
        "- `system/configs/gates.yaml`",
        "- Existing context docs (for safe summary alignment)",
        "",
        "## Files Updated",
    ]
    if updated_files:
        for item in updated_files:
            lines.append(f"- `{item['path']}`: {item['summary']}")
    else:
        lines.append("- No file changed.")

    lines.extend(["", "## Files Unchanged"])
    if unchanged_files:
        for item in unchanged_files:
            lines.append(f"- `{item['path']}`: {item['summary']}")
    else:
        lines.append("- None.")

    lines.extend(
        [
            "",
            "## Manual Review Suggested",
            "These files are intentionally not auto-synced in Level 1:",
        ]
    )
    for path in manual_review_candidates:
        lines.append(f"- `{path}` may need manual review when architecture rules change.")

    lines.extend(
        [
            "",
            "<!-- TODO: Add simple severity tags (Low/Medium/High) for manual review suggestions. -->",
            "",
        ]
    )

    _write_text(report_path, "\n".join(lines))
    return report_path


def run_level1_sync(base_dir: Path | None = None) -> dict[str, object]:
    repo_dir = base_dir or Path(__file__).resolve().parents[3]
    context_dir = repo_dir / "system" / "context"
    logs_dir = repo_dir / "workspace" / "logs"

    catalog, gates = _read_catalog_and_gates(repo_dir)
    results: list[dict[str, object]] = []

    results.append(
        _update_with_auto_sync(
            path=context_dir / "context-summary.md",
            generated_block=_context_summary_section(catalog),
            default_title="Context Summary",
        )
    )
    results.append(
        _update_with_auto_sync(
            path=context_dir / "artifact-model.md",
            generated_block=_artifact_model_section(catalog, gates),
            default_title="Artifact Model",
        )
    )
    results.append(
        _update_with_auto_sync(
            path=context_dir / "workflow-playbook.md",
            generated_block=_workflow_playbook_section(catalog),
            default_title="Workflow Playbook",
        )
    )
    results.append(
        _update_with_auto_sync(
            path=context_dir / "load-profiles.md",
            generated_block=_load_profiles_section(),
            default_title="Load Profiles",
        )
    )

    _append_change_log(context_dir, results)
    _append_sync_log(logs_dir, results)
    report_path = _write_sync_report(context_dir, results)

    return {
        "updated_files": [str(item["path"]) for item in results if item["updated"]],
        "unchanged_files": [str(item["path"]) for item in results if not item["updated"]],
        "report_path": str(report_path),
    }


if __name__ == "__main__":
    _CONSOLE_LOGGER.section("Context Sync")
    _CONSOLE_LOGGER.step("CONTEXT", "Running safe Level 1 sync...")
    output = run_level1_sync()
    _CONSOLE_LOGGER.success("Level 1 context sync completed.")
    _CONSOLE_LOGGER.info(f"Report: {output['report_path']}")
    if hasattr(_CONSOLE_LOGGER, "summary"):
        _CONSOLE_LOGGER.summary(
            "Context Sync Summary",
            [
                ("Updated Files", str(len(output.get("updated_files", [])))),
                ("Unchanged Files", str(len(output.get("unchanged_files", [])))),
            ],
        )
