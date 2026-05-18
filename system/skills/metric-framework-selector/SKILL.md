---
name: metric-framework-selector
description: Select the right product or feature measurement framework for a slice. Use when a Data output needs metrics that PO can use for feature-health decisions.
---
# Metric Framework Selector

## Why This Skill Exists

PO decisions need different measurement lenses depending on the feature, domain, maturity, and user journey. This skill prevents agents from forcing every feature into one framework.

## When To Use It

- a feature needs key metrics or health metrics
- the team needs to explain why a funnel, HEART, AARRR, North Star, task-success, retention, or operational-health lens fits
- metrics must stay aligned with BRD, FRS, acceptance criteria, NFR, and QA risk

## Inputs It Expects

- PO BRD and success measures
- BA FRS, acceptance criteria, and feature list
- architecture and NFR review when available
- wireframe, FE flow, API contract, or BE spec when available

## Output It Should Produce

A short framework decision covering:
- selected framework or hybrid
- why it fits the feature
- why other common frameworks are not primary
- how the framework maps to PO decision needs
- which downstream agents must align with it

## Steps

1. Identify the feature type: acquisition, activation, workflow completion, retention, monetization, operational quality, support reduction, or risk control.
2. Identify the primary PO decision: invest, simplify, fix quality, improve conversion, reduce support, scale, or stop.
3. Select the lightest framework that explains the decision clearly.
4. Use a hybrid only when one framework misses a critical decision signal.
5. State framework limitations and any missing baseline or target.

## Limits

- do not hard-code one framework for every feature
- do not invent baselines, targets, or production benchmarks
- do not select vanity metrics that cannot change a PO decision
- do not replace QA readiness or NFR review
