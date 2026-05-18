---
file_type: "Agent Knowledge"
primary_agents: ["PO"]
supporting_agents: []
activation_mode: "Optional Support"
lifecycle_stage: "Agent Support"
purpose: "Provide optional supporting knowledge for the PO agent when extra depth is needed."
---
# PO Market Research Policy

Use market research only when current market conditions materially affect product direction.

## Research Triggers

- competitor behavior may change scope or positioning
- current user expectations may change the recommended first slice
- the requirement depends on market timing, policy, or external product patterns

## Output Discipline

Always separate:
- `observed market data`
- `inference`
- `recommendation`

## Safety Rule

- if the repository does not contain enough current market information and the decision is time-sensitive, use web research
- do not present stale or uncertain market information as confirmed fact
