from __future__ import annotations

from typing import Any


class JiraConnector:
    """Simple Jira-style payload builder for future integration."""

    def build_story_payload(
        self,
        title: str,
        story: str,
        acceptance_criteria: list[str] | None = None,
        labels: list[str] | None = None,
    ) -> dict[str, Any]:
        acceptance_criteria = acceptance_criteria or []
        labels = labels or []

        description_lines = [story, "", "Acceptance Criteria:"]
        description_lines.extend([f"- {item}" for item in acceptance_criteria])

        # TODO: Replace this local payload with a real Jira API request.
        return {
            "project": "DEMO",
            "issue_type": "Story",
            "summary": title,
            "description": "\n".join(description_lines),
            "labels": labels,
        }
