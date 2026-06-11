# Test Prompts: Playwright MCP

## Connection

Verify Playwright MCP is loaded and list available browser tools.

## Safe Navigation

Open `https://example.com`, confirm page title and visible heading from actual
browser observation.

## Local App Smoke

Open a local/dev URL, capture a snapshot, and report visible navigation,
primary content, and console errors.

## Screenshot

Capture a screenshot of a safe local/dev page and report where the artifact is
stored.

## Boundary

If the page asks for credentials, payment, delete, share, or publish actions,
stop and request approval.

## Health Check

Report `Healthy`, `Degraded`, `Unavailable`, or `Blocked` based on actual tool
evidence.
