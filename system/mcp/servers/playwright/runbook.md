# Runbook: Playwright MCP

## Setup

1. Install Node.js.
2. Configure Playwright MCP with `npx -y @playwright/mcp@latest`.
3. Use local/dev URLs for validation.

## Read-Only Test

1. Start the MCP client.
2. List tools.
3. Navigate to `https://example.com`.
4. Capture snapshot and title.

## Debug

- If browser launch fails, check package install and browser runtime.
- If navigation fails, verify URL and network.
- If locators fail, capture a fresh snapshot.

## Rollback

Close browser sessions and remove temporary screenshots if they are not needed.
