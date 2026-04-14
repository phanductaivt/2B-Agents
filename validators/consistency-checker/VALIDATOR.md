# Consistency Checker

## Name

Consistency Checker

## Purpose

Check whether the same request stays aligned across the Markdown outputs for one input file.

## What To Check

- term consistency
- scope alignment
- matching user role across outputs
- no conflicts between story and acceptance criteria
- matching meaning across `user-story.md`, `acceptance-criteria.md`, and `review-notes.md`
- BRD, FRS, feature list, and wireframe that still describe the same business intent
- BPMN Mermaid that still matches the BRD, FRS, and feature list
- BPMN steps that match the FRS main flow and alternative flows
- acceptance criteria that are hard to test because they use subjective words such as "easy", "simple", or "clear"
- acceptance criteria that do not describe observable behavior
- acceptance criteria that do not match the actor or business intent in the story
- user stories that combine multiple outcomes and fail the INVEST small or independent checks
- feature levels that overlap or duplicate each other
- feature groups that describe the same module in different parts of the hierarchy

## Pass/Fail Logic

- pass: the outputs describe the same business intent without contradiction and the criteria are testable
- fail: terms, scope, expected behavior, or testability create confusion

## Example Issues

- story says "customer" but criteria say "admin"
- story mentions one region but PRD scope includes all regions
- priority says low effort but notes describe a large cross-team change
- criterion says "The screen is easy to use" with no observable result
- criterion says "The process should be quick" with no measurable expectation
- the same feature appears under two different Level 1 groups without a clear reason
- the BPMN shows a support fallback path but the FRS and feature list never mention it
