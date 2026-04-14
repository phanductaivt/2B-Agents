from __future__ import annotations


class ConfluenceConnector:
    """Simple Confluence-style page payload builder for future integration."""

    def build_page_payload(self, title: str, body: str, space_key: str = "DEMO") -> dict[str, str]:
        # TODO: Replace this local payload with a real Confluence API request.
        return {
            "space_key": space_key,
            "title": title,
            "body": body,
            "format": "storage-like-markup",
        }
