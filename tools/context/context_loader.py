from __future__ import annotations

from pathlib import Path


GLOBAL_CONTEXT_FILES = [
    "context-summary.md",
    "workflow-playbook.md",
    "output-standards.md",
    "id-system.md",
    "traceability-rules.md",
]


def _context_dir() -> Path:
    return Path(__file__).resolve().parents[2] / "context"


def _project_dir(project_name: str) -> Path:
    return Path(__file__).resolve().parents[2] / "projects" / project_name


def _join_sections(sections: list[tuple[str, str]]) -> str:
    parts: list[str] = []
    for label, text in sections:
        if not text.strip():
            continue
        parts.append(f"--- {label} ---")
        parts.append(text.strip())
    return "\n\n".join(parts).strip() + ("\n" if parts else "")


def load_specific_context(section_name: str) -> str:
    """Load one context file by section name, e.g. 'id-system'."""
    filename = section_name.strip().lower()
    if not filename.endswith(".md"):
        filename += ".md"
    file_path = _context_dir() / filename
    if not file_path.exists():
        raise FileNotFoundError(f"Context section not found: {section_name}")
    return file_path.read_text(encoding="utf-8")


def load_global_context() -> dict[str, object]:
    """Load global context files from context/."""
    loaded_files: list[str] = []
    missing_files: list[str] = []
    sections: list[tuple[str, str]] = []

    for filename in GLOBAL_CONTEXT_FILES:
        file_path = _context_dir() / filename
        if file_path.exists():
            loaded_files.append(f"context/{filename}")
            sections.append((filename, file_path.read_text(encoding="utf-8")))
        else:
            missing_files.append(f"context/{filename}")

    return {
        "text": _join_sections(sections),
        "loaded_files": loaded_files,
        "missing_files": missing_files,
    }


def load_project_context(project_name: str) -> dict[str, object]:
    """Load project-specific context from projects/<project-name>/knowledge/."""
    project_path = _project_dir(project_name)
    knowledge_dir = project_path / "knowledge"
    targets = [
        "glossary.md",
        "business-rules.md",
        "notes.md",
    ]

    loaded_files: list[str] = []
    missing_files: list[str] = []
    sections: list[tuple[str, str]] = []

    for filename in targets:
        file_path = knowledge_dir / filename
        if file_path.exists():
            loaded_files.append(f"projects/{project_name}/knowledge/{filename}")
            sections.append((filename, file_path.read_text(encoding="utf-8")))
        else:
            missing_files.append(f"projects/{project_name}/knowledge/{filename}")

    return {
        "text": _join_sections(sections),
        "loaded_files": loaded_files,
        "missing_files": missing_files,
    }


def build_full_context(project_name: str) -> dict[str, object]:
    """Combine global + project context in priority order."""
    global_context = load_global_context()
    project_context = load_project_context(project_name)

    full_text = _join_sections(
        [
            ("global-context", str(global_context["text"])),
            ("project-context", str(project_context["text"])),
        ]
    )
    return {
        "text": full_text,
        "global_text": str(global_context["text"]),
        "project_text": str(project_context["text"]),
        "global_loaded_files": list(global_context["loaded_files"]),
        "global_missing_files": list(global_context["missing_files"]),
        "project_loaded_files": list(project_context["loaded_files"]),
        "project_missing_files": list(project_context["missing_files"]),
    }


def load_context_pack() -> str:
    """Backward-compatible helper: return combined core global context text."""
    return str(load_global_context()["text"])


if __name__ == "__main__":
    # Simple local check: print compact context bundle.
    print(load_context_pack())
