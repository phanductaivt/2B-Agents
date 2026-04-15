from __future__ import annotations

import importlib.util
from pathlib import Path
import sys


ID_TYPES = {
    "req": "REQ",
    "brd": "BRD",
    "fr": "FR",
    "us": "US",
    "ac": "AC",
    "feat": "FEAT",
    "ui": "UI",
    "rv": "RV",
    "tc": "TC",
}


def _load_module(module_name: str, file_path: Path):
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Could not load module: {file_path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


_PATHS = _load_module(
    "project_paths_for_id_manager",
    Path(__file__).resolve().parent / "project_paths.py",
)


def _extract_numeric_suffix(filename: str) -> str | None:
    stem = filename.replace(".md", "")
    for part in reversed(stem.split("-")):
        if part.isdigit():
            return part.zfill(3)
    return None


def _max_existing_number(values: list[str], prefix: str) -> int:
    max_value = 0
    for value in values:
        if not value.startswith(prefix + "-"):
            continue
        suffix = value.split("-", 1)[1]
        if suffix.isdigit():
            max_value = max(max_value, int(suffix))
    return max_value


def _next_id(values: list[str], prefix: str) -> str:
    next_number = _max_existing_number(values, prefix) + 1
    return f"{prefix}-{next_number:03d}"


def _default_registry() -> dict[str, object]:
    return {
        "requirements": {},
        "brd": [],
        "fr": [],
        "us": [],
        "ac": [],
        "feature": [],
        "ui": [],
        "review": [],
        "tc": [],
    }


def _parse_registry(lines: list[str]) -> dict[str, object]:
    registry = _default_registry()
    current_key: str | None = None

    for raw_line in lines:
        line = raw_line.split("#", 1)[0].rstrip()
        if not line.strip():
            continue
        if line.endswith(":") and not line.startswith("-"):
            current_key = line.replace(":", "").strip()
            if current_key not in registry:
                registry[current_key] = []
            continue
        if current_key == "requirements" and ":" in line:
            key, value = line.split(":", 1)
            registry["requirements"][key.strip()] = value.strip()
            continue
        if line.strip().startswith("-") and current_key:
            value = line.strip().lstrip("-").strip()
            if isinstance(registry[current_key], list):
                registry[current_key].append(value)

    return registry


def _serialize_registry(registry: dict[str, object]) -> str:
    lines = ["requirements:"]
    requirements: dict[str, str] = registry.get("requirements", {})
    for filename, req_id in sorted(requirements.items()):
        lines.append(f"  {filename}: {req_id}")
    for key in ["brd", "fr", "us", "ac", "feature", "ui", "review", "tc"]:
        lines.append(f"{key}:")
        values = registry.get(key, [])
        if isinstance(values, list):
            for value in values:
                lines.append(f"  - {value}")
    lines.append("")
    return "\n".join(lines)


def load_registry(project_dir: Path) -> dict[str, object]:
    registry_path = _PATHS.id_registry_path(project_dir)
    if not registry_path.exists():
        return _default_registry()
    return _parse_registry(registry_path.read_text(encoding="utf-8").splitlines())


def save_registry(project_dir: Path, registry: dict[str, object]) -> Path:
    registry_path = _PATHS.id_registry_path(project_dir)
    registry_path.parent.mkdir(parents=True, exist_ok=True)
    registry_path.write_text(_serialize_registry(registry), encoding="utf-8")
    return registry_path


def _ensure_unique(values: list[str], new_value: str) -> None:
    if new_value not in values:
        values.append(new_value)


def allocate_tc_ids(project_dir: Path, count: int) -> list[str]:
    """Allocate one or more new TC IDs for this project (unique within project)."""
    if count <= 0:
        return []
    registry = load_registry(project_dir)
    tc_values = registry.get("tc", [])
    if not isinstance(tc_values, list):
        tc_values = []
        registry["tc"] = tc_values

    new_ids: list[str] = []
    for _ in range(count):
        tc_id = _next_id(tc_values, ID_TYPES["tc"])
        tc_values.append(tc_id)
        new_ids.append(tc_id)

    save_registry(project_dir, registry)
    return new_ids


def get_or_create_ids(project_dir: Path, input_file: Path) -> dict[str, str]:
    registry = load_registry(project_dir)
    requirements: dict[str, str] = registry.get("requirements", {})

    filename = input_file.name
    if filename in requirements:
        req_id = requirements[filename]
    else:
        suffix = _extract_numeric_suffix(filename)
        if suffix:
            req_id = f"{ID_TYPES['req']}-{suffix}"
        else:
            existing_req_ids = list(requirements.values())
            next_req = _next_id(existing_req_ids, ID_TYPES["req"])
            req_id = next_req
        requirements[filename] = req_id
        registry["requirements"] = requirements

    suffix = req_id.split("-", 1)[1] if "-" in req_id else "001"
    id_map = {
        "req": req_id,
        "brd": f"{ID_TYPES['brd']}-{suffix}",
        "fr": f"{ID_TYPES['fr']}-{suffix}",
        "us": f"{ID_TYPES['us']}-{suffix}",
        "ac": f"{ID_TYPES['ac']}-{suffix}",
        "feat": f"{ID_TYPES['feat']}-{suffix}",
        "ui": f"{ID_TYPES['ui']}-{suffix}",
        "rv": f"{ID_TYPES['rv']}-{suffix}",
    }

    _ensure_unique(registry["brd"], id_map["brd"])
    _ensure_unique(registry["fr"], id_map["fr"])
    _ensure_unique(registry["us"], id_map["us"])
    _ensure_unique(registry["ac"], id_map["ac"])
    _ensure_unique(registry["feature"], id_map["feat"])
    _ensure_unique(registry["ui"], id_map["ui"])
    _ensure_unique(registry["review"], id_map["rv"])

    save_registry(project_dir, registry)
    return id_map


def ensure_requirement_id_header(input_file: Path, req_id: str) -> None:
    content = input_file.read_text(encoding="utf-8")
    if "Requirement ID:" in content:
        return
    lines = content.splitlines()
    header_line = f"# Requirement ID: {req_id}"
    if lines and lines[0].startswith("#"):
        lines.insert(1, header_line)
    else:
        lines.insert(0, header_line)
    input_file.write_text("\n".join(lines).strip() + "\n", encoding="utf-8")
