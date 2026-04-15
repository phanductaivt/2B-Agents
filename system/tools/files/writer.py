from __future__ import annotations

import importlib.util
from pathlib import Path
import sys


def _load_module(module_name: str, file_path: Path):
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Could not load module: {file_path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


_PATHS = _load_module(
    "project_paths_for_writer",
    Path(__file__).resolve().parents[1] / "project" / "project_paths.py",
)


def get_project_generated_dir(project_dir: str | Path) -> Path:
    """Create projects/<project-name>/_ops/generated/ when needed."""
    generated_dir = _PATHS.generated_root(Path(project_dir))
    generated_dir.mkdir(parents=True, exist_ok=True)
    return generated_dir


def get_project_output_path(project_dir: str | Path, input_name: str) -> Path:
    """Return the output folder for one input inside the selected project."""
    return _PATHS.requirement_output_dir(Path(project_dir), input_name)


def create_project_output_folder(project_dir: str | Path, input_name: str) -> Path:
    """Create projects/<project-name>/_ops/generated/<input-name>/ when needed."""
    folder = get_project_output_path(project_dir, input_name)
    folder.mkdir(parents=True, exist_ok=True)
    return folder


def write_markdown_file(folder: str | Path, filename: str, content: str) -> Path:
    """Write one Markdown file into a project output folder."""
    output_folder = Path(folder)
    output_folder.mkdir(parents=True, exist_ok=True)

    if not filename.endswith(".md"):
        raise ValueError("Only Markdown files are allowed in project output folders.")

    file_path = output_folder / filename
    file_path.write_text(content.strip() + "\n", encoding="utf-8")
    return file_path


def write_html_file(folder: str | Path, filename: str, content: str) -> Path:
    """Write one HTML file into a project output folder."""
    output_folder = Path(folder)
    output_folder.mkdir(parents=True, exist_ok=True)

    if not filename.endswith(".html"):
        raise ValueError("Only HTML files are allowed for FE demo output.")

    file_path = output_folder / filename
    file_path.write_text(content.strip() + "\n", encoding="utf-8")
    return file_path


# TODO: Add a simple option to avoid overwriting reviewed output files.
