---
file_type: "Skill"
primary_agents: ["PO"]
supporting_agents: []
activation_mode: "Triggered By Need"
lifecycle_stage: "System Core"
purpose: "Provide a reusable capability for PO during output generation."
---
# Market Research Synthesizer

## Name

Market Research Synthesizer

## Purpose

Help the PO agent summarize current market conditions, competitor patterns, and user expectations when product direction depends on what is happening in the market now.

## When To Use

Use this skill when:
- current market conditions could change product direction
- competitor patterns may affect scope or positioning
- the requirement asks for a product decision that depends on current user expectations

## Input Format

- business requirement
- project context
- existing market notes if available
- current web findings when needed

## Output Format

- observed market signals
- comparable patterns
- risks or opportunities
- inference
- recommendation
- confidence note

## Step-by-Step Logic

1. Identify what product decision depends on market context.
2. Gather only the market facts that materially affect that decision.
3. Separate verified observations from interpretation.
4. Summarize relevant competitor or market patterns.
5. Explain what those findings mean for scope, priority, or positioning.
6. State recommendation and confidence level clearly.

## Constraints

- do not present old or uncertain market information as current fact
- separate `observed data`, `inference`, and `recommendation`
- keep research focused on decisions that change scope, value, or priority
- if current data is required and missing from the repo, use web research

## Expected Markdown Outputs

- a `Market Context` section inside `brd.md`
- optional supporting notes inside project `03-context/market-research.md`
