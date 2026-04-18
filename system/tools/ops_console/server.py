from __future__ import annotations

from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import importlib.util
import json
from pathlib import Path
import sys
from urllib.parse import parse_qs, urlparse


def _load_module(module_name: str, file_path: Path):
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Could not load module: {file_path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


_LOGGER = _load_module(
    "console_logger_for_ops_console_server",
    Path(__file__).resolve().parents[1] / "logging" / "console_logger.py",
)
_PROJECT_API = _load_module(
    "project_api_for_ops_console_server",
    Path(__file__).resolve().parent / "project_api.py",
)
_TASKS_API = _load_module(
    "tasks_api_for_ops_console_server",
    Path(__file__).resolve().parent / "tasks_api.py",
)
_CONFIRMATIONS_API = _load_module(
    "confirmations_api_for_ops_console_server",
    Path(__file__).resolve().parent / "confirmations_api.py",
)
_DOCS_API = _load_module(
    "docs_api_for_ops_console_server",
    Path(__file__).resolve().parent / "docs_api.py",
)
_ACTIONS_API = _load_module(
    "actions_api_for_ops_console_server",
    Path(__file__).resolve().parent / "actions_api.py",
)


def _json_response(handler: BaseHTTPRequestHandler, payload: dict, status: int = HTTPStatus.OK) -> None:
    body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    handler.send_response(status)
    handler.send_header("Content-Type", "application/json; charset=utf-8")
    handler.send_header("Content-Length", str(len(body)))
    handler.end_headers()
    handler.wfile.write(body)


def _text_response(
    handler: BaseHTTPRequestHandler,
    text: str,
    content_type: str = "text/html; charset=utf-8",
    status: int = HTTPStatus.OK,
) -> None:
    body = text.encode("utf-8")
    handler.send_response(status)
    handler.send_header("Content-Type", content_type)
    handler.send_header("Content-Length", str(len(body)))
    handler.end_headers()
    handler.wfile.write(body)


def run_server(base_dir: Path, host: str = "127.0.0.1", port: int = 8790) -> None:
    ui_dir = base_dir / "workspace" / "ops-console"

    class Handler(BaseHTTPRequestHandler):
        def log_message(self, format: str, *args):  # noqa: A003
            return

        def _project_name(self, query: dict[str, list[str]]) -> str:
            return str((query.get("project", query.get("name", [""]))[0] or "")).strip()

        def _serve_ui_file(self, file_name: str, content_type: str) -> bool:
            file_path = ui_dir / file_name
            if not file_path.exists():
                return False
            _text_response(self, file_path.read_text(encoding="utf-8"), content_type=content_type)
            return True

        def do_GET(self) -> None:  # noqa: N802
            parsed = urlparse(self.path)
            query = parse_qs(parsed.query)

            try:
                if parsed.path in {"/", "/index.html"}:
                    if not self._serve_ui_file("index.html", "text/html; charset=utf-8"):
                        _text_response(self, "<h1>Ops Console UI not found.</h1>", status=HTTPStatus.NOT_FOUND)
                    return
                if parsed.path == "/app.js":
                    if not self._serve_ui_file("app.js", "application/javascript; charset=utf-8"):
                        _text_response(
                            self,
                            "// app.js not found",
                            "application/javascript; charset=utf-8",
                            HTTPStatus.NOT_FOUND,
                        )
                    return
                if parsed.path == "/styles.css":
                    if not self._serve_ui_file("styles.css", "text/css; charset=utf-8"):
                        _text_response(self, "/* styles.css not found */", "text/css; charset=utf-8", HTTPStatus.NOT_FOUND)
                    return

                if parsed.path == "/api/overview":
                    _json_response(self, _PROJECT_API.get_overview(base_dir))
                    return
                if parsed.path == "/api/projects":
                    _json_response(self, _PROJECT_API.get_projects(base_dir))
                    return
                if parsed.path == "/api/project":
                    project_name = self._project_name(query)
                    if not project_name:
                        _json_response(self, {"error": "Missing project query parameter."}, HTTPStatus.BAD_REQUEST)
                        return
                    _json_response(self, _PROJECT_API.get_project(base_dir, project_name))
                    return
                if parsed.path == "/api/requirements":
                    project_name = self._project_name(query)
                    if not project_name:
                        _json_response(self, {"error": "Missing project query parameter."}, HTTPStatus.BAD_REQUEST)
                        return
                    _json_response(self, _TASKS_API.get_requirements(base_dir, project_name))
                    return
                if parsed.path == "/api/tasks":
                    project_name = self._project_name(query)
                    if not project_name:
                        _json_response(self, {"error": "Missing project query parameter."}, HTTPStatus.BAD_REQUEST)
                        return
                    _json_response(self, _TASKS_API.get_tasks(base_dir, project_name))
                    return
                if parsed.path == "/api/confirmations":
                    project_name = self._project_name(query)
                    if not project_name:
                        _json_response(self, {"error": "Missing project query parameter."}, HTTPStatus.BAD_REQUEST)
                        return
                    status_filter = str((query.get("status", ["all"])[0] or "all")).strip()
                    type_filter = str((query.get("type", ["all"])[0] or "all")).strip()
                    owner_filter = str((query.get("owner", ["all"])[0] or "all")).strip()
                    search = str((query.get("search", [""])[0] or "")).strip()
                    _json_response(
                        self,
                        _CONFIRMATIONS_API.get_confirmations(
                            base_dir,
                            project_name,
                            status_filter=status_filter,
                            type_filter=type_filter,
                            owner_filter=owner_filter,
                            search=search,
                        ),
                    )
                    return
                if parsed.path == "/api/confirmations/projects":
                    _json_response(self, _CONFIRMATIONS_API.get_confirmation_projects(base_dir))
                    return
                if parsed.path == "/api/docs":
                    project_name = self._project_name(query)
                    if not project_name:
                        _json_response(self, {"error": "Missing project query parameter."}, HTTPStatus.BAD_REQUEST)
                        return
                    group_filter = str((query.get("group", ["all"])[0] or "all")).strip()
                    _json_response(self, _DOCS_API.get_documents(base_dir, project_name, group_filter=group_filter))
                    return
                if parsed.path == "/api/doc-preview":
                    project_name = self._project_name(query)
                    relative_path = str((query.get("path", [""])[0] or "")).strip()
                    if not project_name or not relative_path:
                        _json_response(
                            self,
                            {"error": "Missing project or path query parameter."},
                            HTTPStatus.BAD_REQUEST,
                        )
                        return
                    _json_response(self, _DOCS_API.get_document_preview(base_dir, project_name, relative_path))
                    return
                if parsed.path == "/api/actions":
                    project_name = self._project_name(query)
                    _json_response(self, _ACTIONS_API.get_actions_capabilities(base_dir, project_name=project_name))
                    return
                if parsed.path == "/api/actions/context":
                    project_name = self._project_name(query)
                    if not project_name:
                        _json_response(self, {"error": "Missing project query parameter."}, HTTPStatus.BAD_REQUEST)
                        return
                    _json_response(self, _ACTIONS_API.get_rerun_context(base_dir, project_name))
                    return

                _json_response(self, {"error": "Not found."}, status=HTTPStatus.NOT_FOUND)
            except ValueError as error:
                _json_response(self, {"error": str(error)}, status=HTTPStatus.BAD_REQUEST)
            except Exception as error:  # pragma: no cover - defensive server fallback.
                _json_response(self, {"error": f"Internal error: {error}"}, status=HTTPStatus.INTERNAL_SERVER_ERROR)

        def do_POST(self) -> None:  # noqa: N802
            parsed = urlparse(self.path)
            content_length = int(self.headers.get("Content-Length", "0"))
            raw = self.rfile.read(content_length) if content_length else b"{}"
            try:
                payload = json.loads(raw.decode("utf-8") or "{}")
            except json.JSONDecodeError:
                _json_response(self, {"error": "Invalid JSON payload."}, status=HTTPStatus.BAD_REQUEST)
                return

            try:
                if parsed.path == "/api/confirmations/refresh":
                    project_name = str(payload.get("project", "")).strip()
                    _json_response(self, _CONFIRMATIONS_API.refresh_confirmations(base_dir, project_name=project_name))
                    return
                if parsed.path == "/api/confirmations/update":
                    _json_response(self, _CONFIRMATIONS_API.update_confirmation(base_dir, payload))
                    return
                if parsed.path == "/api/doc-save":
                    _json_response(self, _DOCS_API.save_document(base_dir, payload))
                    return
                if parsed.path == "/api/actions/check":
                    _json_response(self, _ACTIONS_API.check_rerun_eligibility(base_dir, payload))
                    return
                if parsed.path == "/api/actions/execute":
                    _json_response(self, _ACTIONS_API.execute_rerun_action(base_dir, payload))
                    return
            except ValueError as error:
                _json_response(self, {"error": str(error)}, status=HTTPStatus.BAD_REQUEST)
                return
            except Exception as error:  # pragma: no cover - defensive server fallback.
                _json_response(self, {"error": f"Internal error: {error}"}, status=HTTPStatus.INTERNAL_SERVER_ERROR)
                return

            _json_response(
                self,
                {"error": "Unsupported write endpoint in Phase 3B."},
                status=HTTPStatus.METHOD_NOT_ALLOWED,
            )

    server = ThreadingHTTPServer((host, port), Handler)
    url = f"http://{host}:{port}"
    _LOGGER.section("Operations Console V2 (Phase 3B)")
    _LOGGER.info(f"Open in browser: {url}")
    _LOGGER.info("Confirmation write actions are enabled in this console.")
    _LOGGER.info("Docs viewer/editor is enabled for allowlisted files.")
    _LOGGER.info("Stale detection and rerun recommendations are enabled.")
    _LOGGER.info("Controlled rerun actions are enabled: project, requirement, and from-stage.")
    _LOGGER.info("Artifact-level rerun and gate override are still disabled in this phase.")
    _LOGGER.info("Press Ctrl+C to stop the server.")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        _LOGGER.warning("Operations console server stopped.")
    finally:
        server.server_close()


if __name__ == "__main__":
    run_server(base_dir=Path(__file__).resolve().parents[3])
