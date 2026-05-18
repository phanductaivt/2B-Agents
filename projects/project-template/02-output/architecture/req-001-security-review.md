---
file_type: "Sample Security Artifact"
primary_agents: ["Architect"]
supporting_agents: ["BE", "FE", "QA"]
activation_mode: "Reference Sample"
lifecycle_stage: "Project Sample Output"
purpose: "Show the security review expected for the runnable ticket-change sample."
---
# req-001 Security Review

## 1. Scope

- Feature: self-service ticket date change
- Sensitive areas: ticket ownership, payment requirement, confirmation status

## 2. Actors And Access

- Customer
  - allowed actions: view own ticket, request quote, confirm date change
  - denied actions: change another customer's ticket

## 3. Security Treatment In Sample

- Authentication and ownership are not implemented in the local sample.
- This is acceptable only because the sample is a local runnable demonstration.

## 4. Required Production Controls

- Authenticate customer identity.
- Verify ticket ownership before quote and confirmation.
- Integrate real payment authorization before ticket update.
- Avoid exposing internal rejection details directly.

## 5. Risk

- This sample is not production secure without auth, ownership, and payment integration.
