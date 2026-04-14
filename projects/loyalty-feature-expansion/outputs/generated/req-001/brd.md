# BRD: Loyalty Overview Expansion

- BRD ID: `BRD-001`
- Parent REQ ID: `REQ-001`
## Business Problem
Members contact support because loyalty points, tier progress, and recent activity are not clear enough.

## Business Goals
- Reduce avoidable loyalty-related support calls.
- Improve member confidence in points and tier progress.
- Create a simple first dashboard release for web users.

## Stakeholders
- Business Analyst
- Business Stakeholder
- Support Team
- End User

## Scope
- Show available points, tier progress, and recent activity in one member view.
- Separate available values from expired or unavailable values clearly.
- Guide the member when loyalty data is delayed or missing.

## Business Rules
- Only posted transactions can add to available loyalty points.
- Expired points must be shown separately from available points.
- Tier progress must follow approved membership rules.
- If loyalty data is delayed or unavailable, the page must show a clear guidance message.
- Pending activity must not change available points until posting.
- If tier data is missing, the system must show guidance instead of a blank panel.

## Assumptions
- A measurable success metric is still missing.
- System integration details are not described yet.

## Expected Benefits
- Fewer avoidable support questions.
- Better alignment between business and delivery teams.
