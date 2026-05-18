---
file_type: "Sample State Artifact"
primary_agents: ["Data"]
supporting_agents: ["BA", "BE", "QA"]
activation_mode: "Reference Sample"
lifecycle_stage: "Project Sample Output"
purpose: "Show the state transition expected for the runnable ticket-change sample."
---
# req-001 State Transition

## Ticket States

- `confirmed`
  - ticket can be quoted for date change before departure
- `changed`
  - ticket date has been updated and confirmation has been sent

## Transitions

- `confirmed -> changed`
  - trigger: customer confirms date change after viewing fees
  - validation: new travel date is before departure
  - validation: payment is confirmed when total due is greater than zero
  - side effect: ticket travel date is updated

## Invalid Transitions

- date change after departure
  - expected result: reject with `change_after_departure`
- confirmation without required payment
  - expected result: reject with `payment_required`
