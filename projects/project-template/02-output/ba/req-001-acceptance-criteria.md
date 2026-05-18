---
file_type: "Sample BA Artifact"
primary_agents: ["BA"]
supporting_agents: ["PO"]
activation_mode: "Reference Sample"
lifecycle_stage: "Project Sample Output"
purpose: "Show the expected quality and structure of the BA artifact for acceptance criteria."
---
# Requirement: req-001

# Acceptance Criteria: Ticket Booking Modification Improvement

- AC ID: `AC-001`
- Parent Story ID: `US-001`

## Criteria
- Given a customer opens the booking change page for their own booking, when eligibility is checked, then the system shows whether the booking can be changed online.
- Given a booking is eligible for online change, when the system shows change options, then the related fee is visible before confirmation.
- Given a booking is not eligible for online change, when the page loads, then the system shows the rejection reason and support guidance.
- Given the booking does not belong to the customer, when they attempt to access the change page, then access is blocked and booking details are not shown.

## Edge Cases
- Given the fee service is unavailable, when the customer tries to review change options, then the system shows a fallback message and stops the change flow.
- Given the change fee is zero, when the customer reviews the selected change, then the system still requires a final confirmation step.
