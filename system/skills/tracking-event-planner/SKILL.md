---
name: tracking-event-planner
description: Convert feature metrics into business-readable tracking events and actions. Use when Data must produce event tracking guidance that PO can discuss with FE, BE, QA, and developers.
---
# Tracking Event Planner

## Why This Skill Exists

Metrics are not usable unless the team knows what event or action creates the data. This skill turns a metric plan into a practical event tracking handoff.

## When To Use It

- a metric needs user, system, FE, BE, or manual tracking signals
- PO needs enough detail to discuss implementation with developers
- QA needs checks that important events fire at the correct moment

## Inputs It Expects

- metric list and selected framework
- wireframe or FE interaction flow when available
- API contract or BE spec when available
- acceptance criteria, validation rules, and exception flows
- privacy, security, and sensitive-data notes

## Output It Should Produce

An event or action tracking plan where each item states:
- Event/action name
- Trigger
- Source: FE screen, BE endpoint, system job, or manual operation
- Actor
- Required properties
- Optional properties
- Related metric
- Expected timing
- Verification
- Notes for dev
- Privacy note

## Steps

1. Map each metric to the minimum events or actions needed to calculate it.
2. Name events using a stable object_action_result pattern when possible.
3. Put user-intent events at the user action moment and outcome events after FE or BE result is known.
4. Add properties only when they help calculate, segment, debug, or protect the metric.
5. Prefer identifiers and categories over raw sensitive values.
6. Define how QA or dev can verify the event fired and contains required properties.

## Limits

- do not design a production analytics SDK integration
- do not collect sensitive data without a clear business reason
- do not require FE-only tracking for backend-only outcomes
- do not require backend tracking for purely UI intent unless server confirmation matters
