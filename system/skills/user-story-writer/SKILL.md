# User Story Writer

## Name

User Story Writer

## Purpose

Convert clarified requirements into user stories that are easy for product and delivery teams to review.

## When To Use

Use this skill when:
- the feature goal is clear enough to write a story
- a backlog item needs a standard story format
- a BA or PO wants a first draft for refinement

## Input Format

- clarified requirement
- actor or user role
- business goal
- expected value

## Output Format

- story title
- user story statement
- context notes
- INVEST check
- dependencies

## Step-by-Step Logic

1. Identify the user role.
2. Define the need or action.
3. State the business value.
4. Confirm the story is INVEST-compliant.
5. Add helpful context and dependencies.
6. Keep the story focused on one clear outcome.

## Constraints

- do not mix many unrelated outcomes in one story
- use plain business language
- point out missing actor, value, or scope if needed
- note which INVEST elements are weak or missing

## Business Thinking

- A good story explains who needs something, what they need, and why it matters.
- The value should make sense to the business, not only to the system.
- If one story contains many outcomes, split it into smaller stories before refinement.
- A story should describe the need, not the technical solution.
- INVEST helps you keep the story independent, negotiable, valuable, estimable, small, and testable.

## Realistic Example

Example input:

```text
Customers cannot see whether their order is confirmed, packed, or shipped.
Support gets many calls because of this.
```

What a BA should notice:
- the actor is the customer
- the need is order status visibility
- the business value is fewer support calls and better customer confidence
- if returns, cancellations, and delivery tracking are also requested, they may need separate stories

## Expected Markdown Outputs

- `user-story.md`
- optional input to `review-notes.md`

## Example Markdown Output

```md
# User Story: Customer Order Status Visibility

## Story
As a customer, I want to view my order status so that I can understand order progress without contacting support.

## Context
This story comes from a requirement about reducing avoidable support calls.

## INVEST Check
- Independent: This story can be delivered without a separate return flow story.
- Negotiable: Details of the status labels can be refined with business stakeholders.
- Valuable: It reduces support calls and improves customer confidence.
- Estimable: Scope is limited to one status view in the portal.
- Small: Focused on one page and one visible status update.
- Testable: Acceptance criteria describe observable outcomes.

## Dependencies
- agreed status labels
- portal release scope
```
