---
file_type: "Agent Knowledge"
primary_agents: ["BA"]
supporting_agents: []
activation_mode: "Optional Support"
lifecycle_stage: "Agent Support"
purpose: "Provide optional supporting knowledge for the BA agent when extra depth is needed."
---
# BA Question Strategy

Ask only when the missing answer materially changes the BA package.

## Ask Immediately When

- the primary actor is unclear
- the business value could be interpreted in more than one meaningful way
- a pricing, approval, compliance, or policy rule would change the flow
- release scope is broad enough to change feature slicing
- unauthorized access, missing data, or unavailable dependency behavior is unknown

## Record As Assumption When

- a reasonable default can keep the package reviewable
- the uncertainty does not change the first release slice
- the assumption can be made visible without misleading delivery teams

## Stop And Mark Needs-Review When

- multiple assumptions would stack together and distort the output
- BRD and FRS would tell different stories depending on the answer
- UXUI or FE would be forced to guess behavior

## Preferred Question Outcomes

Aim to clarify:
- who the user is
- what business pain exists today
- why the outcome matters
- which rule constrains the feature
- which cases are out of scope for release one
