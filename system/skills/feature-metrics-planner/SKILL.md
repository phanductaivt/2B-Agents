---
name: feature-metrics-planner
description: Define decision-ready feature metrics and interpretation guidance. Use when Data needs to create a metric tracking plan for PO feature-health review.
---
# Feature Metrics Planner

## Why This Skill Exists

Feature metrics must help PO understand whether a feature is working, where it is unhealthy, and what decision should follow. Metrics without interpretation create noise.

## When To Use It

- a feature needs measurable outcome, behavior, funnel, quality, or guardrail metrics
- success measures are present but too broad for tracking
- PO needs scenarios for reading actual results after release

## Inputs It Expects

- selected metric framework
- BRD business objective and success measures
- BA flows, acceptance criteria, business rules, and exceptions
- NFR, security, BE, FE, QA, and release context when available

## Output It Should Produce

A metric set where each metric states:
- Metric
- Type: outcome, behavior, funnel, quality, or guardrail
- Why PO cares
- How to calculate
- How to read
- Related tracking events
- Decision scenarios

## Steps

1. Start from the PO decision and business outcome.
2. Add behavior metrics that show whether users actually use the feature.
3. Add funnel or task metrics when the feature has a multi-step path.
4. Add quality or health metrics that show errors, latency, validation friction, dependency failure, or support impact.
5. Add guardrail metrics that prevent misleading conclusions.
6. Write concrete interpretation scenarios that combine metrics instead of reading each one alone.

## Limits

- do not create metrics that have no tracking signal
- do not confuse test pass/fail with product-health metrics
- do not define dashboard layouts in this skill
- mark missing baseline, target, or denominator instead of guessing
