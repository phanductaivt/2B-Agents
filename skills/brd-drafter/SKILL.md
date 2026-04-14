# BRD Drafter

## Name

BRD Drafter

## Purpose

Create a simple Business Requirement Document that explains the business need, business value, scope, and rules.

## When To Use

Use this skill when:
- stakeholders need a business-facing requirement document
- the BA wants a clearer summary than raw notes
- scope, benefits, and business rules must be stated clearly

## Input Format

- clarified requirement
- business goals
- stakeholders
- scope notes
- business rules

## Output Format

- business problem
- business goals
- stakeholders
- scope
- business rules
- assumptions
- expected benefits

## Step-by-Step Logic

1. State the business problem clearly.
2. Explain the business goals and expected value.
3. List the main stakeholders and users.
4. Define in-scope and out-of-scope areas.
5. Capture business rules, assumptions, and benefits.

## Constraints

- keep the BRD business-focused
- avoid deep technical design detail
- label assumptions clearly

## Expected Markdown Outputs

- `brd.md`

## Example Markdown Output

```md
# BRD: Order Status Visibility

## Business Problem
Customers call support because they cannot see order progress.

## Business Goals
- Reduce avoidable support calls
- Improve customer confidence

## Stakeholders
- Customers
- Support team
- Product owner

## Business Rules
- Only approved order statuses can be shown
- Portal users can only see their own orders
```
