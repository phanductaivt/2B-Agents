# BPMN Process: Ticket Booking Modification Improvement

- Requirement ID: `REQ-001`
## Mermaid Diagram
```mermaid
flowchart TD
    A[Start] --> B[Customer opens booking change page]
    B --> C[System checks booking eligibility]
    C --> D{Online change allowed?}
    D -->|Yes| E[Show change options and fees]
    D -->|No| F[Show support or refund guidance]
    E --> G[Customer confirms change]
    G --> H[System updates booking]
    F --> I[End]
    H --> I[End]
```
