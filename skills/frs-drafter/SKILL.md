# FRS Drafter

## Name

FRS Drafter

## Purpose

Create an agile-style Functional Requirement Specification that explains what the product must do in a structured way.

## When To Use

Use this skill when:
- the team needs a more functional handoff after the BRD
- BA outputs must become clearer for UX/UI and FE work
- business rules need to become functional statements

## Input Format

- clarification
- user story
- acceptance criteria
- business rules
- process notes

## Output Format

- functional summary
- actors
- functional requirements
- main flow
- alternative flows
- business rules
- validations
- edge cases
- dependencies
- open questions

## Step-by-Step Logic

1. Summarize the function in plain English.
2. Identify the main actors.
3. Turn the business need into numbered functional requirements.
4. Describe the main flow in simple steps that match the functional requirements.
5. Describe alternative flows for failures, exceptions, or business rule branches.
6. Add business rules that control what is allowed, limited, or blocked.
7. Add validations and rule-driven behavior.
8. Add edge cases such as missing data, invalid status, or out-of-scope scenarios.
9. Note dependencies and open questions.

## Constraints

- keep the FRS readable for agile teams
- do not turn it into a heavy technical spec
- make each functional requirement observable
- make business rules and edge cases explicit instead of hiding them in general wording
- keep flows short enough for BA, UXUI, and FE teams to follow without guesswork

## Business Thinking

- FRS should help delivery teams understand what the product must do, what rules apply, and how the product behaves when things go wrong.
- Business rules should state what is allowed, restricted, or required.
- Edge cases should cover realistic situations that often cause support issues or implementation confusion.
- If an edge case is not yet decided, record it as an open question instead of inventing an answer.
- Main and alternative flows should show the normal path plus the most common exception paths.

## Expected Markdown Outputs

- `frs.md`

## Example Markdown Output

```md
# FRS: Order Status Visibility

## Functional Summary
The portal must show the latest approved order status to the customer.

## Actors
- Customer
- Order status service

## Functional Requirements
- FR-1: The customer can open the order page and view the latest status.
- FR-2: The system only shows approved status values.
- FR-3: If no valid status is available, the page shows a support message.

## Main Flow
1. Customer opens the order page.
2. System loads the latest approved status.
3. System displays the approved status to the customer.

## Alternative Flows
1. If no valid status is available, show a support guidance message.
2. If the status service is unavailable, show a fallback message and avoid stale data.

## Business Rules
- Only approved order statuses can be shown to the customer.
- Customers can only view their own orders.
- The first release supports confirmed, packed, and shipped statuses.

## Validations
- The page must not show another customer's order data.
- Status labels must match business-approved wording.

## Edge Cases
- If no valid status is returned, show support guidance.
- If the order is cancelled, show the approved cancelled message if it is in scope.
- If the status service is temporarily unavailable, show a fallback message.
```
