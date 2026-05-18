---
file_type: "Skill"
primary_agents: ["QA"]
supporting_agents: []
activation_mode: "Triggered By Need"
lifecycle_stage: "System Core"
purpose: "Provide a reusable capability for QA during output generation."
---
# Test Case Writer

## Why This Skill Exists

This skill helps the QA agent turn coverage scenarios into concrete, reproducible test cases.

## When To Use It

Use this skill when a slice needs:
- step-by-step test execution guidance
- explicit preconditions and expected results
- reusable cases for manual or future automated testing

## Inputs It Expects

- test scenarios
- acceptance criteria
- FRS
- BE spec
- API contract
- FE output when user-visible steps matter
- Data metric tracking plan when tracking verification is in scope

## Output It Should Produce

A Markdown test case set that explains:
- test case ID
- objective
- preconditions
- steps
- expected result
- evidence or execution record expectation
- automation candidate and priority
- tracking verification when relevant
- priority or severity note when relevant

## Steps

1. Start from approved test scenarios
2. Convert each important scenario into one or more specific test cases
3. Make preconditions explicit
4. Keep steps observable and reproducible
5. Define expected results in business-visible terms
6. Define the evidence to capture, such as command output, API response, screenshot, or manual observation
7. Mark whether each case is a manual-only, API-test, UI-e2e, unit-test, or smoke-test automation candidate
8. Add tracking verification for important metric events when the metric tracking plan requires it
9. Flag missing rule detail if expected results would otherwise be guessed

## Limits

- do not write vague expected results
- do not merge unrelated scenarios into one oversized case
- do not treat open questions as passed behavior
- do not invent tracking events beyond the metric tracking plan
- do not call a case automation-ready unless the trigger, assertion, and stable test data are clear
