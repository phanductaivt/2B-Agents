---
file_type: "Data Artifact"
primary_agents: ["Data"]
supporting_agents: ["BE", "QA"]
activation_mode: "Generated Output"
lifecycle_stage: "Project Output"
purpose: "State transition rules for inventory status."
---
# req-001 State Transition

## Status Calculation

- Quantity equals 0 -> OUT_OF_STOCK.
- Quantity greater than 0 and minimum_stock exists and quantity <= minimum_stock -> LOW_STOCK.
- Quantity greater than minimum_stock -> ACTIVE.
- Quantity greater than 0 and minimum_stock is empty -> ACTIVE.

## Mutation Transitions

- Create product -> calculate initial status.
- Update product minimum_stock -> recalculate status.
- Update quantity -> recalculate status.
- Delete product -> set is_deleted = true and exclude from active views.

## Invalid Transitions

- Quantity below 0 is rejected.
- Minimum stock below 0 is rejected.
- Updating or deleting a missing/deleted product is rejected.
