---
name: security-reviewer
description: Review security, privacy, authorization, and sensitive-flow risks before implementation. Use when a feature touches identity, ownership, payment, personal data, or sensitive business rules.
---
# Security Reviewer

## Use When

- data access, ownership, eligibility, payment, or privacy matters
- backend or frontend behavior could expose sensitive information

## Output

A Markdown security review covering:
- actors and access assumptions
- authorization checks
- sensitive data handling
- error message safety
- audit and abuse risks
- open questions

## Rules

- do not claim a feature is secure without explicit checks
- flag missing auth or privacy behavior as a blocker when it changes safe implementation
- keep recommendations practical for local runnable v1
