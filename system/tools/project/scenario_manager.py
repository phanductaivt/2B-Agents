from __future__ import annotations

from pathlib import Path

try:
    import yaml
except ImportError as error:  # pragma: no cover
    raise ImportError(
        "PyYAML is required for scenario loading. Install with: pip install -r requirements.txt"
    ) from error


SCENARIOS_DIR = Path("system") / "scenarios"
CATALOG_FILE = "scenario-catalog.yaml"
GENERIC_SCENARIO = "generic"


def _read_yaml(path: Path) -> dict[str, object]:
    if not path.exists():
        raise FileNotFoundError(f"Scenario file not found: {path}")
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    if not isinstance(data, dict):
        raise ValueError(f"Scenario YAML must be a dictionary: {path}")
    return data


def load_scenario_catalog(base_dir: Path) -> dict[str, object]:
    return _read_yaml(base_dir / SCENARIOS_DIR / CATALOG_FILE)


def _normalize_key(value: str) -> str:
    return value.strip().lower()


def _resolve_by_domain(catalog: dict[str, object], domain: str) -> str | None:
    scenario_map = catalog.get("scenarios", {})
    if not isinstance(scenario_map, dict):
        return None
    domain_key = _normalize_key(domain)
    if not domain_key:
        return None
    for scenario_name, info in scenario_map.items():
        if not isinstance(info, dict):
            continue
        domains = info.get("domains", [])
        if isinstance(domains, list) and domain_key in [_normalize_key(str(item)) for item in domains]:
            return str(scenario_name)
    return None


def resolve_scenario_name(project_config: dict[str, object], catalog: dict[str, object]) -> tuple[str, str]:
    scenario_map = catalog.get("scenarios", {})
    if not isinstance(scenario_map, dict):
        return (GENERIC_SCENARIO, "fallback-generic")

    configured_scenario = _normalize_key(str(project_config.get("scenario", "")))
    if configured_scenario:
        if configured_scenario in scenario_map:
            return (configured_scenario, "project-scenario")
        return (GENERIC_SCENARIO, "invalid-project-scenario-fallback")

    domain = str(project_config.get("domain", ""))
    by_domain = _resolve_by_domain(catalog, domain)
    if by_domain:
        return (by_domain, "domain-mapping")

    return (GENERIC_SCENARIO, "fallback-generic")


def _deep_merge(base: dict[str, object], override: dict[str, object]) -> dict[str, object]:
    merged: dict[str, object] = dict(base)
    for key, value in override.items():
        if key in merged and isinstance(merged[key], dict) and isinstance(value, dict):
            merged[key] = _deep_merge(
                merged[key] if isinstance(merged[key], dict) else {},
                value,
            )
        else:
            merged[key] = value
    return merged


def load_scenario_definition(
    base_dir: Path,
    catalog: dict[str, object],
    scenario_name: str,
) -> dict[str, object]:
    scenario_map = catalog.get("scenarios", {})
    if not isinstance(scenario_map, dict):
        raise ValueError("Invalid scenario catalog format: 'scenarios' must be a mapping.")

    generic_info = scenario_map.get(GENERIC_SCENARIO, {})
    if not isinstance(generic_info, dict) or "file" not in generic_info:
        raise ValueError("Scenario catalog must include generic scenario with a file.")
    generic_file = base_dir / SCENARIOS_DIR / str(generic_info.get("file", "generic.yaml"))
    generic_data = _read_yaml(generic_file)

    selected_info = scenario_map.get(scenario_name)
    if not isinstance(selected_info, dict) or "file" not in selected_info:
        return generic_data

    selected_file = base_dir / SCENARIOS_DIR / str(selected_info.get("file", ""))
    selected_data = _read_yaml(selected_file)
    return _deep_merge(generic_data, selected_data)


def resolve_project_scenario(base_dir: Path, project_config: dict[str, object]) -> dict[str, object]:
    catalog = load_scenario_catalog(base_dir)
    scenario_name, source = resolve_scenario_name(project_config, catalog)
    scenario_data = load_scenario_definition(base_dir, catalog, scenario_name)
    return {
        "scenario_name": scenario_name,
        "source": source,
        "scenario_data": scenario_data,
    }


def describe_scenario_resolution(result: dict[str, object]) -> str:
    """Return a short human-readable scenario resolution line."""
    name = str(result.get("scenario_name", "generic"))
    source = str(result.get("source", "unknown"))
    return f"Scenario resolved: {name} ({source})"
