from __future__ import annotations

from pathlib import Path


def input_root(project_dir: Path) -> Path:
    return project_dir / "01-input"


def requirements_dir(project_dir: Path) -> Path:
    return input_root(project_dir) / "requirements"


def notes_dir(project_dir: Path) -> Path:
    return input_root(project_dir) / "notes"


def assets_dir(project_dir: Path) -> Path:
    return input_root(project_dir) / "assets"


def project_guides_dir(project_dir: Path) -> Path:
    return project_dir / "03-guides"


def knowledge_dir(project_dir: Path) -> Path:
    return project_dir / "04-knowledge"


def ops_dir(project_dir: Path) -> Path:
    return project_dir / "_ops"


def runtime_dir(project_dir: Path) -> Path:
    return ops_dir(project_dir) / "runtime"


def traceability_dir(project_dir: Path) -> Path:
    return ops_dir(project_dir) / "traceability"


def generated_root(project_dir: Path) -> Path:
    return ops_dir(project_dir) / "generated"


def requirement_output_dir(project_dir: Path, requirement_name: str) -> Path:
    return generated_root(project_dir) / requirement_name


def status_path(project_dir: Path) -> Path:
    return ops_dir(project_dir) / "status.md"


def decision_log_path(project_dir: Path) -> Path:
    return ops_dir(project_dir) / "decision-log.md"


def task_tracker_path(project_dir: Path) -> Path:
    return ops_dir(project_dir) / "task-tracker.md"


def change_log_path(project_dir: Path) -> Path:
    return ops_dir(project_dir) / "change-log.md"


def dependency_map_path(project_dir: Path) -> Path:
    return ops_dir(project_dir) / "dependency-map.md"


def project_flow_path(project_dir: Path) -> Path:
    return ops_dir(project_dir) / "project-flow.md"


def traceability_summary_path(project_dir: Path) -> Path:
    return traceability_dir(project_dir) / "requirement-traceability-summary.md"


def id_registry_path(project_dir: Path) -> Path:
    return runtime_dir(project_dir) / "id-registry.yaml"


def processing_state_path(project_dir: Path) -> Path:
    return runtime_dir(project_dir) / "processing-state.yaml"


def curated_output_dir(project_dir: Path) -> Path:
    return project_dir / "02-output"


def curated_ba_dir(project_dir: Path) -> Path:
    return curated_output_dir(project_dir) / "ba"


def curated_design_dir(project_dir: Path) -> Path:
    return curated_output_dir(project_dir) / "design"


def curated_fe_dir(project_dir: Path) -> Path:
    return curated_output_dir(project_dir) / "fe"

