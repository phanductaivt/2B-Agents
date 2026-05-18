---
file_type: "Skill"
primary_agents: ["PO"]
supporting_agents: []
activation_mode: "Triggered By Need"
lifecycle_stage: "System Core"
purpose: "Provide a reusable capability for PO during output generation."
---
# BRD Drafter

## Name

BRD Drafter

## Purpose

Create a PO-owned Business Requirement Document that explains the business need, business value, scope, BACCM framing, requirement classification, and key rules.

## When To Use

Use this skill when:
- stakeholders need a business-facing requirement document
- the PO needs a structured framing document before BA analysis
- scope, benefits, and business rules must be stated clearly

## Input Format

- clarified requirement
- business objective
- stakeholders
- scope notes
- business rules
- BACCM framing
- requirement classification
- market context when relevant

## Output Format

- business problem
- business objective
- stakeholders
- scope
- BACCM framing
- requirement classification
- market context
- business rules
- assumptions
- expected benefits

## Step-by-Step Logic

1. State the business problem clearly.
2. Explain the business objective and expected value.
3. List the main stakeholders and users.
4. Add BACCM framing so the change and context are visible.
5. Define in-scope and out-of-scope areas.
6. Classify the requirement into business, stakeholder, solution, and transition requirements.
7. Capture business rules, assumptions, market context, and benefits.

## Constraints

- keep the BRD business-focused
- avoid deep technical design detail
- label assumptions clearly
- separate observed market facts from inference and recommendation

## Expected Markdown Outputs

- `brd.md`

## Example Markdown Output

```md
# BRD: Order Status Visibility

## Business Problem
Customers call support because they cannot see order progress.

## Business Objective
- Reduce avoidable support calls
- Improve customer confidence

## Stakeholders
- Customers
- Support team
- Product owner

## Requirement Classification
### Business Requirements
- Reduce avoidable support calls by improving order status visibility.

### Stakeholder Requirements
- Customers need to understand order progress without contacting support.

### Solution Requirements
- The portal must display valid order status information.

### Transition Requirements
- Support wording and status labels must be approved before release.

## Business Rules
- Only approved order statuses can be shown
- Portal users can only see their own orders
```
