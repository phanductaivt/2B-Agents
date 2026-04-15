from __future__ import annotations


def summarize_text_change(old_text: str, new_text: str) -> str:
    """Return a short human-readable summary of text changes."""
    if old_text == new_text:
        return "No content change."

    old_lines = old_text.splitlines()
    new_lines = new_text.splitlines()
    old_count = len(old_lines)
    new_count = len(new_lines)
    delta = new_count - old_count

    if delta > 0:
        delta_text = f"+{delta} lines"
    elif delta < 0:
        delta_text = f"{delta} lines"
    else:
        delta_text = "line count unchanged"

    return f"Changed ({old_count} -> {new_count}, {delta_text})."

