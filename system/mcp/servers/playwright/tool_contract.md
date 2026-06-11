# Tool Contract: Playwright MCP

| Tool class | Purpose | Input | Output | Allowed scope | Risk | Failure cases |
|---|---|---|---|---|---|---|
| navigate | Open a local/dev or approved URL. | URL. | Page load state. | Safe URLs only. | Medium | Network error, blocked URL, auth required. |
| snapshot | Capture visible page structure. | Current page. | Accessibility/page snapshot. | Current safe page. | Low | No page open, dynamic content missing. |
| screenshot | Capture UI evidence. | Current page or region. | Image artifact. | Current safe page. | Low | Browser unavailable, permission issue. |
| click/type | Interact with UI. | Locator and input. | Updated page state. | Approved test flows. | High | Wrong locator, destructive action risk. |
| console | Collect console messages. | Current page. | Console log summary. | Current safe page. | Low | No page open, logs unavailable. |

Example request:

```json
{
  "url": "http://localhost:5173"
}
```

Example response:

```json
{
  "status": "ok",
  "title": "Local App",
  "observations": ["main navigation visible", "no console errors"]
}
```
