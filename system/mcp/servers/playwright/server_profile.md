# Server Profile: Playwright MCP

| Field | Value |
|---|---|
| Server name | Playwright MCP |
| Category | Browser Automation |
| Status | Approved |
| Owner | Workspace owner |
| Allowed Agents | UX, FE, QA, Release |
| Main use cases | UI smoke test, page inspection, screenshots, console logs, local/dev flow validation. |
| Disabled use cases | Production checkout/payment/send/share/destructive flows without approval. |
| Risk level | Medium |
| Required environment variables | `MCP_DRY_RUN`, `MCP_LOG_LEVEL` |
| Dependencies | `@playwright/mcp`, Node.js, browser runtime |
