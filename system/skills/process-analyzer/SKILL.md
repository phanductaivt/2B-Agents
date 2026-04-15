# Process Analyzer

## Name

Process Analyzer

## Purpose

Document and compare the current process (AS-IS) and the future process (TO-BE).

## When To Use

Use this skill when:
- a process has pain points
- handoffs or approvals are unclear
- the team needs a before-and-after process view

## Input Format

- process notes
- stakeholder interview notes
- current pain points
- target improvements

## Output Format

- AS-IS summary
- TO-BE summary
- pain points
- improvement opportunities
- optional process flow notes

## Step-by-Step Logic

1. Describe the current steps.
2. Identify delays, rework, or confusion.
3. Define the desired future flow.
4. Compare AS-IS and TO-BE.
5. Highlight decisions, owners, and impacts.

## Constraints

- do not assume hidden steps without marking them
- keep actor names and process terms consistent
- separate observed facts from proposed changes

## Business Thinking

- Start with what really happens today, not what people think should happen.
- Pay close attention to handoffs, approvals, waiting time, and duplicate work.
- Ask who owns each step and what causes delay or rework.
- The TO-BE process should solve real pain points, not just redraw the same flow with new words.

## Realistic Example

Example process problem:

```text
Invoice approval is handled through email and chat.
Requests are often delayed because nobody is sure who owns the next step.
```

What a BA should notice:
- the AS-IS process may have hidden waiting time
- ownership after each approval step may be unclear
- leave periods or backup approvers may be missing
- the TO-BE process should improve control and visibility, not only speed

## Expected Markdown Outputs

- `clarification.md`
- `review-notes.md`

## Example Markdown Output

```md
# Process Analysis: Invoice Approval

## AS-IS Summary
- Requester sends invoice by email.
- Manager reviews it manually.
- Finance waits for updates in chat.

## TO-BE Summary
- Requester submits invoice in one shared flow.
- Each approval step has a clear owner.
- Requesters can see current approval status.

## Pain Points
- unclear ownership after manager review
- missed approvals during leave periods

## Improvement Opportunities
- add backup approvers
- create visible status tracking
```
