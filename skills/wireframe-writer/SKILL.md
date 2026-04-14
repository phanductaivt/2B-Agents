# Wireframe Writer

## Name

Wireframe Writer

## Purpose

Turn BA outputs into a simple Markdown wireframe for screen planning.

## When To Use

Use this skill when:
- the BA FRS is ready for UI planning
- the team needs a low-detail screen layout before HTML work
- the page structure must be discussed quickly

## Input Format

- FRS
- optional BPMN process
- optional feature list
- optional acceptance criteria

## Output Format

- screen goal
- layout sections
- component list
- interaction notes
- simple wireframe sketch in Markdown

## Step-by-Step Logic

1. Define the screen goal.
2. List the main visible sections.
3. Add important components and interactions.
4. Keep the layout simple enough for quick review.
5. Make sure the wireframe still reflects the business flow.

## Constraints

- keep the wireframe low detail
- avoid design system complexity in the first version
- make the wireframe readable in plain Markdown

## Expected Markdown Outputs

- `wireframe.md`

## Example Markdown Output

````md
# Wireframe: Order Status Page

## Screen Goal
Help customers view the latest order status quickly.

## Main Sections
- Header
- Order summary
- Status timeline
- Help section

## Wireframe Sketch
```text
+----------------------------------+
| Header                           |
+----------------------------------+
| Order Summary                    |
+----------------------------------+
| Status Timeline                  |
+----------------------------------+
| Need Help?                       |
+----------------------------------+
```
````
