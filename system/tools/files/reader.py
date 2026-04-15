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
    "project_paths_for_reader",
    Path(__file__).resolve().parents[1] / "project" / "project_paths.py",
)


def read_text_file(path: str | Path) -> str:
    """Read one local file as text."""
    file_path = Path(path)
    return file_path.read_text(encoding="utf-8")


def read_text_if_exists(path: str | Path) -> str:
    """Read one local file if it exists, otherwise return an empty string."""
    file_path = Path(path)
    if not file_path.exists():
        return ""
    return file_path.read_text(encoding="utf-8")


def list_markdown_files(path: str | Path) -> list[str]:
    """List Markdown files in one local folder."""
    directory = Path(path)
    if not directory.exists():
        return []
    return sorted(str(file_path) for file_path in directory.glob("*.md"))


def read_simple_yaml_file(path: str | Path) -> dict[str, object]:
    """Read a very small YAML file with top-level keys and simple lists."""
    result: dict[str, object] = {}
    current_list_key: str | None = None

    for raw_line in read_text_file(path).splitlines():
        line = raw_line.split("#", 1)[0].rstrip()
        stripped = line.strip()
        if not stripped:
            continue

        if stripped.startswith("- "):
            if current_list_key is None:
                continue
            result.setdefault(current_list_key, [])
            current_value = result[current_list_key]
            if isinstance(current_value, list):
                current_value.append(stripped[2:].strip())
            continue

        if ":" not in stripped:
            continue

        key, value = stripped.split(":", 1)
        key = key.strip()
        value = value.strip()

        if value == "":
            result[key] = []
            current_list_key = key
        else:
            result[key] = value
            current_list_key = None

    return result


def get_project_dir(base_path: str | Path, project_name: str) -> Path:
    """Return the folder for one project inside projects/."""
    project_dir = Path(base_path) / "projects" / project_name
    if not project_dir.exists():
        raise FileNotFoundError(f"Project '{project_name}' does not exist in projects/.")
    return project_dir


def get_project_input_path(
    project_dir: str | Path, input_type: str, file_name: str
) -> Path:
    """Return a project input path for one input type and file name."""
    project_path = Path(project_dir)
    if input_type == "requirements":
        return _PATHS.requirements_dir(project_path) / file_name
    if input_type == "meeting-notes":
        return _PATHS.notes_dir(project_path) / "meeting-notes" / file_name
    if input_type == "raw":
        return _PATHS.assets_dir(project_path) / "raw" / file_name
    raise ValueError("Input type must be requirements, meeting-notes, or raw.")


def list_project_input_files(project_dir: str | Path) -> list[Path]:
    """List the visible input files for one project."""
    project_path = Path(project_dir)
    input_files: list[Path] = []
    folders = [
        _PATHS.requirements_dir(project_path),
        _PATHS.notes_dir(project_path) / "meeting-notes",
        _PATHS.assets_dir(project_path) / "raw",
    ]
    for folder in folders:
        if not folder.exists():
            continue
        for file_path in sorted(folder.iterdir()):
            if file_path.is_file() and not file_path.name.startswith("."):
                input_files.append(file_path)
    return input_files


def resolve_project_input_file(project_dir: str | Path, input_name: str | None = None) -> Path:
    """Resolve one input file inside the selected project."""
    project_path = Path(project_dir)
    inputs_dir = _PATHS.input_root(project_path)

    if input_name:
        candidate = Path(input_name)
        if candidate.is_absolute():
            raise ValueError("Project runs only support input files inside the project folder.")

        direct_path = inputs_dir / candidate
        if direct_path.exists():
            return direct_path

        nested_folders = [
            inputs_dir / "requirements",
            inputs_dir / "notes" / "meeting-notes",
            inputs_dir / "assets" / "raw",
        ]
        for folder in nested_folders:
            nested_path = folder / candidate
            if nested_path.exists():
                return nested_path

        raise FileNotFoundError(
            f"Could not find input file '{input_name}' in project '{project_path.name}'."
        )

    available_files = list_project_input_files(project_path)
    if not available_files:
        raise FileNotFoundError(
            f"Project '{project_path.name}' does not contain any input files yet."
        )
    return available_files[0]


def read_project_knowledge(project_dir: str | Path) -> dict[str, str]:
    """Read the simple knowledge files for one project."""
    knowledge_dir = _PATHS.knowledge_dir(Path(project_dir))
    return {
        "glossary": read_text_if_exists(knowledge_dir / "glossary.md"),
        "business_rules": read_text_if_exists(knowledge_dir / "business-rules.md"),
        "notes": read_text_if_exists(knowledge_dir / "notes.md"),
    }


# TODO: Add optional parsing for richer YAML and table-shaped business input later.
