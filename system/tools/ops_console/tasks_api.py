from __future__ import annotations

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
    "state_mapper_for_ops_tasks_api",
    Path(__file__).resolve().parent / "state_mapper.py",
)


def get_tasks(base_dir: Path, project_name: str) -> dict[str, Any]:
    project_dir = _MAPPER.resolve_project_dir(base_dir, project_name)
    return {
        "project": project_name,
        "tasks": _MAPPER.task_models(project_dir),
    }


def get_requirements(base_dir: Path, project_name: str) -> dict[str, Any]:
    project_dir = _MAPPER.resolve_project_dir(base_dir, project_name)
    return {
        "project": project_name,
        "requirements": _MAPPER.requirement_processing_models(project_dir),
    }

