from __future__ import annotations

from typing import Iterable

try:
    from rich.console import Console
    from rich.table import Table
except ImportError:  # pragma: no cover - fallback if dependency is missing.
    Console = None  # type: ignore[assignment]
    Table = None  # type: ignore[assignment]


_console = Console() if Console else None


def _emit(message: str) -> None:
    if _console:
        _console.print(message)
    else:
        print(message)


def section(title: str) -> None:
    if _console:
        _console.rule(f"[bold cyan]{title}")
    else:
        print(f"\n=== {title} ===")


def info(message: str) -> None:
    if _console:
        _emit(f"[cyan][INFO][/cyan] {message}")
    else:
        _emit(f"[INFO] {message}")


def success(message: str) -> None:
    if _console:
        _emit(f"[green][SUCCESS][/green] {message}")
    else:
        _emit(f"[SUCCESS] {message}")


def warning(message: str) -> None:
    if _console:
        _emit(f"[yellow][WARNING][/yellow] {message}")
    else:
        _emit(f"[WARNING] {message}")


def error(message: str) -> None:
    if _console:
        _emit(f"[red][ERROR][/red] {message}")
    else:
        _emit(f"[ERROR] {message}")


def skipped(message: str) -> None:
    if _console:
        _emit(f"[yellow][SKIPPED][/yellow] {message}")
    else:
        _emit(f"[SKIPPED] {message}")


def blocked(message: str) -> None:
    if _console:
        _emit(f"[magenta][BLOCKED][/magenta] {message}")
    else:
        _emit(f"[BLOCKED] {message}")


def step(agent_or_stage: str, message: str) -> None:
    label = agent_or_stage.strip().upper() if agent_or_stage.strip() else "STEP"
    if _console:
        _emit(f"[bold blue][{label}][/bold blue] {message}")
    else:
        _emit(f"[{label}] {message}")


def summary(title: str, items: Iterable[tuple[str, str]]) -> None:
    if _console:
        _console.rule(f"[bold cyan]{title}")
    else:
        print(f"\n=== {title} ===")
    for key, value in items:
        _emit(f"- {key}: {value}")


def simple_table(
    title: str,
    headers: list[str],
    rows: Iterable[list[str]],
) -> None:
    if not _console or not Table:
        print(title)
        print(" | ".join(headers))
        for row in rows:
            print(" | ".join(row))
        return

    table = Table(title=title, header_style="bold cyan")
    for header in headers:
        table.add_column(header)
    for row in rows:
        table.add_row(*row)
    _console.print(table)
