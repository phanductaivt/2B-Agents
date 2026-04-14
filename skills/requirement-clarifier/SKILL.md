# Requirement Clarifier

## Name

Requirement Clarifier

## Purpose

Turn rough stakeholder notes into a clearer and more structured requirement draft.

## When To Use

Use this skill when:
- the request is vague
- important business details are missing
- the team needs clear follow-up questions before writing stories

## Input Format

- free-text requirement note
- meeting summary
- email or chat message
- optional business rules

## Output Format

- requirement title
- short summary
- known facts
- assumptions
- open questions
- next actions

## Step-by-Step Logic

1. Read the raw input.
2. Identify the business problem, not only the requested feature.
3. Pull out the facts that are already clear.
4. Separate facts from assumptions and wishes.
5. Write open questions to remove ambiguity.
6. Suggest next actions for the BA or other stakeholders.

## Constraints

- do not invent business rules without marking them as assumptions
- keep language simple and specific
- highlight gaps instead of hiding them

## Business Thinking

- Ask what problem the business is trying to solve, not only what screen or feature was requested.
- Look for the user, the pain point, the expected value, and the main business rule.
- If success is mentioned only in general words such as "better" or "faster", turn that into an open question.
- If the request mixes many ideas together, keep the first clarification focused on the main outcome.

## Realistic Example

Example input:

```text
Customers keep calling support because they cannot see order progress.
We want order status in the portal.
The first release should be simple.
```

What a BA should notice:
- the user is probably the customer
- the business pain is high support call volume
- "simple" is vague and needs clarification
- the release scope is mentioned, but business rules are still missing

## Expected Markdown Outputs

- `clarification.md`
- optional input to `review-notes.md`

## Example Markdown Output

```md
# Clarification: Customer Order Status Visibility

## Summary
Customers need to see order progress in the portal so support receives fewer avoidable calls.

## Known Facts
- Customers currently call support for status updates.
- The first release is planned for the portal.

## Assumptions
- Detailed status rules are not defined yet.

## Open Questions
- Which status values should customers see?
- Are cancelled or delayed orders included in the first release?

## Next Actions
- Confirm status labels with the BA and business stakeholders.
```
