# PRD Drafter

## Name

PRD Drafter

## Purpose

Draft a simple Product Requirements Document from clarified business and product inputs.

## When To Use

Use this skill when:
- an initiative needs a PRD
- a feature group needs product framing
- stakeholders need one document for review

## Input Format

- feature or initiative summary
- problem statement
- goals
- scope
- dependencies

## Output Format

- problem statement
- objectives
- scope in and out
- user impact
- risks
- open questions

## Step-by-Step Logic

1. Define the problem clearly.
2. Capture goals and success measures.
3. Describe in-scope and out-of-scope areas.
4. Summarize user impact and dependencies.
5. Note risks and open questions.

## Constraints

- keep the PRD focused on business value
- avoid long technical design detail in the first draft
- separate confirmed facts from assumptions

## Business Thinking

- A PRD should explain why the work matters before it explains what will be built.
- Scope is easier to review when the first release is narrow and realistic.
- Always include risks and open questions so stakeholders can discuss them early.
- If the document becomes too detailed too quickly, pull it back to the business problem, goals, and scope.

## Realistic Example

Example initiative:

```text
Customers need to see order status in the self-service portal.
The business wants to reduce support calls in the first release.
```

What a BA should notice:
- the problem is lack of visibility, not only missing portal screens
- the goal should connect to fewer support calls and better confidence
- the first release may only need a small status set
- integrations, status mapping, and exception handling are likely risks

## Expected Markdown Outputs

- `mini-prd.md`
- optional input to `review-notes.md`

## Example Markdown Output

```md
# Mini PRD: Customer Order Status Visibility

## Problem
Customers cannot easily see order progress, so support receives avoidable calls.

## Goal
Provide basic order status visibility in the portal for the first release.

## Users
Customers using the portal

## Scope
Show confirmed, packed, and shipped statuses in the first release.

## Risks
Status mapping and exception handling may still need clarification.

## Open Questions
- Are cancelled orders included in the first release?
```
