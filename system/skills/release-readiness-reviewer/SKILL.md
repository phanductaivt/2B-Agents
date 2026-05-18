---
file_type: "Skill"
primary_agents: ["QA"]
supporting_agents: []
activation_mode: "Triggered By Need"
lifecycle_stage: "System Core"
purpose: "Provide a reusable capability for QA during output generation."
---
# Release Readiness Reviewer

## Why This Skill Exists

This skill helps the QA agent judge whether a feature slice is ready for a serious release conversation.

## When To Use It

Use this skill when the team needs:
- visible blockers
- explicit major risks
- a clear readiness recommendation
- quality judgment that spans BA, BE, FE, and business-critical behavior

## Inputs It Expects

- BRD
- FRS
- acceptance criteria
- BE spec
- API contract
- FE output
- test scenarios
- test cases

## Output It Should Produce

A Markdown release-readiness review that explains:
- blockers
- major risks
- acceptable known gaps
- readiness recommendation

## Steps

1. Review the approved scope and critical business behavior
2. Check whether core paths and material negative paths are covered
3. Identify blockers that would make release discussion unsafe
4. Separate major but tolerable risks from blockers
5. State a clear readiness recommendation

## Limits

- do not hide blockers inside general observations
- do not call a slice ready if critical expectations are still undefined
- do not treat FE demo completeness as proof of release readiness
