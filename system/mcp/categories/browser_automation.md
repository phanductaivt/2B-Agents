# Browser Automation MCP Category

Use this category for browser interaction, UI testing, screenshots, and smoke
checks.

Primary server:

- `servers/playwright`

Use browser automation when:

- A task needs actual page state evidence.
- UI flows must be smoke tested.
- Screenshots, console logs, or page snapshots are needed.

Do not use browser automation for:

- Production checkout, payment, send, share, or destructive flows without
  approval.
- Credential entry unless the user explicitly approves the target and account.
