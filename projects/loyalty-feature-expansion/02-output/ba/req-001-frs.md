# Requirement: req-001

# FRS: Loyalty Overview Expansion

- FR ID: `FR-001`
- Parent REQ ID: `REQ-001`
## Functional Summary
The portal must show available points, tier progress, and recent loyalty activity for the current member.

## Actors
- member
- business service

## Functional Requirements
- {'FR-1': 'Member can view available points for current account.'}
- {'FR-2': 'System displays current tier and progress to next tier.'}
- {'FR-3': 'Page displays recent loyalty activity.'}
- {'FR-4': 'Page displays guidance when data is unavailable or delayed.'}

## Main Flow
- Member opens loyalty overview page.
- System loads points, tier progress, and recent activity.
- System displays loyalty summary.

## Alternative Flows
- If loyalty data is delayed, show guidance and hide incomplete totals.
- If activity data is missing, show placeholder and support path.
- If member account is invalid, show access error message.

## Business Rules
- Only posted transactions can add to available loyalty points.
- Expired points must be shown separately from available points.
- Tier progress must follow approved membership rules.
- If loyalty data is delayed or unavailable, the page must show a clear guidance message.
- Only posted transactions can add to available points.
- Expired points must be shown separately.
- Tier progress follows approved membership rules.
- Pending activity must not affect available points until posted.

## Validations
- Show only current member's loyalty data.
- Separate available and expired points clearly.
- Keep tier wording aligned with approved labels.

## Edge Cases
- Delayed loyalty data from source.
- Pending transactions not yet posted.
- Expired points present in account.
- Invalid member account access attempt.

## Dependencies
- Loyalty data service is available.
- Tier and point rules are approved.

## Open Questions
- Are there any approvals, exceptions, or out-of-scope cases to capture?
