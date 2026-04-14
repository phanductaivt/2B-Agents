from __future__ import annotations

from pathlib import Path


def get_project_generated_dir(project_dir: str | Path) -> Path:
    """Create projects/<project-name>/outputs/generated/ when needed."""
    generated_dir = Path(project_dir) / "outputs" / "generated"
    generated_dir.mkdir(parents=True, exist_ok=True)
    return generated_dir


def get_project_output_path(project_dir: str | Path, input_name: str) -> Path:
    """Return the output folder for one input inside the selected project."""
    return Path(project_dir) / "outputs" / "generated" / input_name


def create_project_output_folder(project_dir: str | Path, input_name: str) -> Path:
    """Create projects/<project-name>/outputs/generated/<input-name>/ when needed."""
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
