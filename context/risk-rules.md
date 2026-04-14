# Risk Rules

## Risk Types
- Scope risk (missing or shifting scope)
- Requirement clarity risk (ambiguous wording)
- Dependency risk (upstream gaps block downstream)
- Delivery risk (incomplete outputs)
- Quality risk (non-testable criteria)

## Severity Levels
- High: blocks delivery or creates critical mismatch
- Medium: impacts quality but can proceed with mitigation
- Low: minor clarity or formatting issue

## Evaluation Inputs
- `status.md` blockers
- validator findings
- missing critical outputs (FRS, AC, review notes)
- traceability gaps

## Rule
- Capture high-risk items clearly in status and review artifacts.

<!-- TODO: Add lightweight risk scoring helper script. -->
