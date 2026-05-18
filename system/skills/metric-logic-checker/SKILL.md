---
name: metric-logic-checker
description: Review whether feature metrics and tracking events align with product intent, flows, risks, and downstream implementation. Use before treating a metric tracking plan as ready.
---
# Metric Logic Checker

## Why This Skill Exists

Metrics can look polished while measuring the wrong thing. This skill checks that metrics, events, and interpretation scenarios match the approved feature behavior.

## When To Use It

- a metric tracking plan is being finalized
- metrics or events may conflict with BRD, FRS, API, FE, NFR, security, or QA outputs
- the plan includes funnel, conversion, error, support, payment, privacy, or dependency-sensitive signals

## Inputs It Expects

- metric tracking plan draft
- BRD, FRS, acceptance criteria, feature list, and BPMN when available
- architecture, NFR, security, BE, FE, QA, and release outputs when available

## Output It Should Produce

A short readiness check covering:
- missing metric logic
- missing tracking signals
- unsupported event properties
- privacy or sensitive-data risks
- cross-agent alignment gaps
- final recommendation

## Steps

1. Check that every metric has at least one related tracking event or action.
2. Check that every event supports at least one metric or decision scenario.
3. Check that every metric has a readable interpretation and a PO decision scenario.
4. Check that event source, trigger, required properties, and verification are present.
5. Check that sensitive fields are avoided or justified.
6. Flag gaps instead of inventing unavailable implementation details.

## Limits

- do not approve vanity metrics that do not change a decision
- do not hide missing baselines or targets
- do not override QA, security, or NFR blockers
