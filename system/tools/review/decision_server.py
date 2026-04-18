from __future__ import annotations

from pathlib import Path
import importlib.util
import sys


def _load_module(module_name: str, file_path: Path):
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Could not load module: {file_path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


_CONSOLE_LOGGER = _load_module(
    "console_logger_for_legacy_decision_server",
    Path(__file__).resolve().parents[1] / "logging" / "console_logger.py",
)
_OPS_CONSOLE_SERVER = _load_module(
    "ops_console_server_for_legacy_decision_server",
    Path(__file__).resolve().parents[1] / "ops_console" / "server.py",
)


def run_server(base_dir: Path, project_name: str | None = None, host: str = "127.0.0.1", port: int = 8787) -> None:
    _CONSOLE_LOGGER.section("Decision Workspace (Legacy Wrapper)")
    _CONSOLE_LOGGER.warning("decision-review is deprecated and compatibility-only.")
    _CONSOLE_LOGGER.info("Primary console path: python3 app.py --ops-console")
    if project_name:
        _CONSOLE_LOGGER.info(
            f"Requested project filter '{project_name}' is ignored in legacy mode. Use ops_console project selector."
        )
    _OPS_CONSOLE_SERVER.run_server(base_dir=base_dir, host=host, port=port)


if __name__ == "__main__":
    base_dir = Path(__file__).resolve().parents[3]
    run_server(base_dir=base_dir)
