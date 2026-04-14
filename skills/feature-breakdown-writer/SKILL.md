# Feature Breakdown Writer

## Name

Feature Breakdown Writer

## Purpose

Help the BA Agent turn requirements, BRD, and FRS into a clear feature hierarchy and product structure.

## When To Use

Use this skill when:
- the team needs a BA-owned feature breakdown after analysis
- one business request needs smaller delivery slices
- UXUI and FE teams need a clearer handoff

## Input Format

- BRD
- FRS
- user story
- acceptance criteria
- clarified business scope

## Output Format

- Level 1 feature groups
- Level 2 feature groups
- Level 3 feature items
- simple scope notes
- first-slice guidance when needed

## Step-by-Step Logic

1. Identify the main business capability.
2. Group the capability into Level 1 feature areas.
3. Break each area into Level 2 features.
4. Add Level 3 features only when they improve clarity.
5. Check that each level still matches the BRD and FRS.
6. Keep the hierarchy logical, non-overlapping, and easy for stakeholders to review.

## Constraints

- do not create duplicate features across groups
- do not add deep hierarchy unless it helps understanding
- keep naming simple and business-readable
- do not create feature groups that conflict with the BRD or FRS

## Business Thinking

- Feature hierarchy should help stakeholders understand scope, not impress them with structure.
- Level 1 should describe a business area.
- Level 2 should describe a meaningful functional group.
- Level 3 should describe a specific feature or sub-capability.
- If two features overlap strongly, regroup them instead of repeating them.

## Expected Markdown Outputs

- `feature-list.md`

## Example Markdown Output

```md
# Feature Breakdown

## Order Management
### Status Visibility
#### Show Latest Approved Status
#### Show Missing Status Guidance

### Access Control
#### Show Status For The Correct Customer Order
#### Block Unauthorized Order View

## Support Guidance
### Missing Or Invalid Status
#### Explain Why Status Is Not Available
#### Direct User To Help Path
```
