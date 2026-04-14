# Prioritization Helper

## Name

Prioritization Helper

## Purpose

Help the BA Agent compare work items using common prioritization methods such as RICE and MoSCoW.

## When To Use

Use this skill when:
- backlog items compete for limited capacity
- roadmap decisions need a clear method
- stakeholders ask why one item should come before another

## Input Format

- feature list
- expected value
- effort estimate
- reach or impact notes
- strategic importance

## Output Format

- prioritization method used
- scored or grouped items
- short rationale
- risks or assumptions

## Step-by-Step Logic

1. Choose the prioritization method.
2. Review the value and effort for each item.
3. Score or group the items.
4. Explain the ranking in plain English.
5. Capture assumptions that may change the order later.

## Constraints

- do not present rough scores as exact truth
- explain trade-offs simply
- call out low-confidence inputs

## Business Thinking

- Prioritization should make trade-offs visible, not pretend every number is exact.
- A high-value item may still move later if the team lacks confidence, ownership, or key dependencies.
- Always explain why an item is high, medium, or low priority in business terms.
- If effort or impact is uncertain, say that clearly in the review notes.

## Realistic Example

Example items:

```text
1. Show order status in the customer portal
2. Add export to CSV for internal users
3. Redesign dashboard colors
```

What a BA should notice:
- order status may have stronger business value because it reduces support calls
- CSV export may help operations, but perhaps with lower customer impact
- dashboard color changes may matter, but could rank lower if they do not solve a clear business problem

## Expected Markdown Outputs

- `review-notes.md`
- optional prioritization section inside `brd.md` or another BA review file

## Example Markdown Output

```md
# Prioritization Notes

## Method
MoSCoW

## Suggested Priority
- Must Have: Show order status in the customer portal
- Should Have: Add export to CSV for internal users
- Could Have: Redesign dashboard colors

## Rationale
- Order status directly supports a known business pain point.
- CSV export is useful but less urgent.
- Dashboard color changes do not solve the main problem.
```
