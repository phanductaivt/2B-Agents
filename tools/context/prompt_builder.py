from __future__ import annotations


def build_prompt_package(
    global_context: str,
    project_context: str,
    task_input: str,
) -> str:
    """Create one compact prompt package from context + task input."""
    sections: list[str] = []

    if global_context.strip():
        sections.append("## Global Context\n" + global_context.strip())
    if project_context.strip():
        sections.append("## Project Context\n" + project_context.strip())
    sections.append("## Task Input\n" + task_input.strip())

    return "\n\n".join(sections).strip() + "\n"
