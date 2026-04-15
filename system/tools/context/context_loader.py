from __future__ import annotations

import importlib.util
from pathlib import Path
import sys


GLOBAL_CONTEXT_FILES = [
    "context-summary.md",
    "workflow-playbook.md",
    "output-standards.md",
    "id-system.md",
    "traceability-rules.md",
]


def _context_dir() -> Path:
    return Path(__file__).resolve().parents[3] / "system" / "context"


def _project_dir(project_name: str) -> Path:
    return Path(__file__).resolve().parents[3] / "projects" / project_name


def _load_module(module_name: str, file_path: Path):
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Could not load module: {file_path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


_PATHS = _load_module(
    "project_paths_for_context_loader",
    Path(__file__).resolve().parents[1] / "project" / "project_paths.py",
)


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
    """Load global context files from system/context/."""
    loaded_files: list[str] = []
    missing_files: list[str] = []
    sections: list[tuple[str, str]] = []

    for filename in GLOBAL_CONTEXT_FILES:
        file_path = _context_dir() / filename
        if file_path.exists():
            loaded_files.append(f"system/context/{filename}")
            sections.append((filename, file_path.read_text(encoding="utf-8")))
        else:
            missing_files.append(f"system/context/{filename}")

    return {
        "text": _join_sections(sections),
        "loaded_files": loaded_files,
        "missing_files": missing_files,
    }


def load_project_context(project_name: str) -> dict[str, object]:
    """Load project-specific context from projects/<project-name>/04-knowledge/."""
    project_path = _project_dir(project_name)
    knowledge_dir = _PATHS.knowledge_dir(project_path)
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
            loaded_files.append(f"projects/{project_name}/04-knowledge/{filename}")
            sections.append((filename, file_path.read_text(encoding="utf-8")))
        else:
            missing_files.append(f"projects/{project_name}/04-knowledge/{filename}")

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


def _load_module(module_name: str, file_path: Path):
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Could not load module: {file_path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


if __name__ == "__main__":
    # Simple local check: print compact context bundle.
    logger = _load_module(
        "console_logger_for_context_loader",
        Path(__file__).resolve().parents[1] / "logging" / "console_logger.py",
    )
    logger.section("Context Loader")
    logger.info("Loaded global context pack.")
    logger.info(load_context_pack())
