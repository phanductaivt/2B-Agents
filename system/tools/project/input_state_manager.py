from __future__ import annotations

from datetime import datetime
import hashlib
import importlib.util
from pathlib import Path
import sys


def _now_iso() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def _load_module(module_name: str, file_path: Path):
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Could not load module: {file_path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


_PATHS = _load_module(
    "project_paths_for_input_state",
    Path(__file__).resolve().parent / "project_paths.py",
)


def _state_path(project_dir: Path) -> Path:
    return _PATHS.processing_state_path(project_dir)


def _default_state() -> dict[str, object]:
    return {"requirements": {}}


def _strip_quotes(value: str) -> str:
    cleaned = value.strip()
    if cleaned.startswith('"') and cleaned.endswith('"') and len(cleaned) >= 2:
        return cleaned[1:-1]
    return cleaned


def load_processing_state(project_dir: Path) -> dict[str, object]:
    path = _state_path(project_dir)
    if not path.exists():
        return _default_state()

    requirements: dict[str, dict[str, str]] = {}
    current_requirement: str | None = None

    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.rstrip()
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        if stripped == "requirements:":
            continue
        if line.startswith("  ") and not line.startswith("    ") and stripped.endswith(":"):
            current_requirement = stripped[:-1].strip()
            requirements.setdefault(current_requirement, {})
            continue
        if current_requirement and line.startswith("    ") and ":" in stripped:
            key, value = stripped.split(":", 1)
            requirements[current_requirement][key.strip()] = _strip_quotes(value)

    return {"requirements": requirements}


def save_processing_state(project_dir: Path, state: dict[str, object]) -> Path:
    path = _state_path(project_dir)
    path.parent.mkdir(parents=True, exist_ok=True)
    requirements = state.get("requirements", {})
    lines = ["requirements:"]

    if isinstance(requirements, dict):
        for file_name in sorted(requirements.keys()):
            entry = requirements.get(file_name, {})
            if not isinstance(entry, dict):
                continue
            lines.append(f"  {file_name}:")
            lines.append(f'    input_hash: "{entry.get("input_hash", "")}"')
            lines.append(f'    last_processed_at: "{entry.get("last_processed_at", "")}"')
            lines.append(f'    output_version: "{entry.get("output_version", "")}"')
            lines.append(f'    status: "{entry.get("status", "")}"')

    lines.append("")
    path.write_text("\n".join(lines), encoding="utf-8")
    return path


def compute_input_hash(input_file: Path) -> str:
    content = input_file.read_bytes()
    return hashlib.sha256(content).hexdigest()


def classify_requirement_input(
    state: dict[str, object],
    input_file: Path,
) -> tuple[str, str]:
    """
    Return (classification, current_hash):
    - new
    - changed
    - unchanged
    """
    requirements = state.get("requirements", {})
    current_hash = compute_input_hash(input_file)
    if not isinstance(requirements, dict):
        return ("new", current_hash)

    entry = requirements.get(input_file.name)
    if not isinstance(entry, dict):
        return ("new", current_hash)

    previous_hash = str(entry.get("input_hash", "")).strip()
    if not previous_hash:
        return ("new", current_hash)
    if previous_hash != current_hash:
        return ("changed", current_hash)
    return ("unchanged", current_hash)


def describe_input_classification(file_name: str, classification: str) -> str:
    """Return a human-readable incremental classification message."""
    normalized = classification.strip().lower()
    if normalized == "new":
        return f"New input detected: {file_name}"
    if normalized == "changed":
        return f"Changed input detected: {file_name}"
    if normalized == "unchanged":
        return f"Unchanged input skipped: {file_name}"
    if normalized == "forced":
        return f"Force re-run: {file_name}"
    return f"Input state ({normalized}): {file_name}"


def read_output_version(project_dir: Path, requirement_name: str) -> str:
    version_info_path = _PATHS.requirement_output_dir(project_dir, requirement_name) / "version-info.md"
    if not version_info_path.exists():
        return "-"
    for line in version_info_path.read_text(encoding="utf-8").splitlines():
        if line.strip().startswith("- Current Version:"):
            version = line.split(":", 1)[1].strip()
            return version or "-"
    return "-"


def update_requirement_state(
    project_dir: Path,
    state: dict[str, object],
    file_name: str,
    input_hash: str,
    output_version: str,
    status: str = "processed",
) -> Path:
    requirements = state.get("requirements")
    if not isinstance(requirements, dict):
        requirements = {}
        state["requirements"] = requirements

    requirements[file_name] = {
        "input_hash": input_hash,
        "last_processed_at": _now_iso(),
        "output_version": output_version,
        "status": status,
    }
    return save_processing_state(project_dir, state)
