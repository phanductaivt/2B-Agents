# FRS: Loyalty Overview Expansion

- FR ID: `FR-001`
- Parent REQ ID: `REQ-001`
## Functional Summary
The portal must show available points, tier progress, and recent loyalty activity for the current member.

## Actors
- member
- business service

## Functional Requirements
- FR-1: The member can open the loyalty overview page and view available points for the current account.
- FR-2: The system displays the current tier and progress toward the next tier using approved membership rules.
- FR-3: The page displays recent loyalty activity for the current member account.
- FR-4: The page displays guidance when loyalty data is unavailable or delayed.

## Main Flow
- Member opens the loyalty overview page.
- System loads points, tier progress, and recent activity.
- System displays the loyalty summary to the member.

## Alternative Flows
- If loyalty data is delayed, show a guidance message and hide incomplete totals.
- If activity data is missing, show a placeholder and a support path.
- If the member account is invalid, show an access error message.

## Business Rules
- Only posted transactions can add to available loyalty points.
- Expired points must be shown separately from available points.
- Tier progress must follow approved membership rules.
- If loyalty data is delayed or unavailable, the page must show a clear guidance message.
- Pending activity must not change available points until posting.
- If tier data is missing, the system must show guidance instead of a blank panel.

## Validations
- Show only the current member's loyalty data.
- Separate available points from expired points.
- Keep tier wording aligned with approved business labels.

## Edge Cases
- If loyalty data is delayed, display a clear message instead of blank sections.
- If a transaction is pending, do not add it to available points before posting.
- If points have expired, show them separately from available points.
- If the member account is not valid, do not display another member's loyalty data.

## Dependencies
- Loyalty data service is available.
- Tier rules and point labels are approved by business stakeholders.

## Open Questions
- Are there any approvals, exceptions, or out-of-scope cases to capture?
