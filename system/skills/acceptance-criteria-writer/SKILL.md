# Acceptance Criteria Writer

## Name

Acceptance Criteria Writer

## Purpose

Write testable acceptance criteria that describe when a story should be considered complete.

## When To Use

Use this skill when:
- a user story already exists
- a team needs clear scope boundaries
- testers and developers need shared completion rules

## Input Format

- user story
- business rules
- edge cases
- assumptions or constraints

## Output Format

- acceptance criteria list
- happy path
- exceptions or edge cases
- notes on non-functional needs if relevant

## Step-by-Step Logic

1. Review the user story and business rules.
2. Describe the expected success path.
3. Add error, exception, or edge case behavior.
4. Check that each criterion is observable and testable.
5. Remove vague wording.
6. Prefer Given/When/Then phrasing for clarity.

## Constraints

- avoid technical implementation detail unless needed for clarity
- each criterion should be testable
- flag missing business rules before finalizing
- avoid words like "simple", "fast", "easy", or "user-friendly" unless you define them

## Business Thinking

- Acceptance criteria should tell the team when the story is done from a business point of view.
- Good criteria describe visible behavior, not hidden system logic.
- Always check for edge cases such as missing data, invalid status, approval rules, or out-of-scope scenarios.
- If a criterion cannot be tested or observed, it is usually too vague.
- Given/When/Then phrasing helps keep the criteria unambiguous and testable.

## Realistic Example

Example user story:

```text
As a customer, I want to view my order status so that I can understand order progress without contacting support.
```

What a BA should notice:
- the happy path is that the customer sees the current status
- there may be business rules about which statuses are allowed
- there may be exceptions such as cancelled orders or missing tracking data
- wording such as "status should be clear" is too vague unless the visible labels are defined

## Expected Markdown Outputs

- `acceptance-criteria.md`
- optional input to `review-notes.md`

## Example Markdown Output

```md
# Acceptance Criteria: Customer Order Status Visibility

## Criteria
- Given a customer opens their order page, when a valid status exists, then the portal shows the approved order status label.
- Given the portal shows an order status, when a label is displayed, then it matches the agreed business wording.
- Given no valid status exists, when the portal loads the order page, then a support guidance message is shown.
- Given the customer is not authorized, when they attempt to view another order, then the portal blocks access.
```
