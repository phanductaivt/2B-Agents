# Project Flow Template

Copy this template into a project-specific visual if needed.

```mermaid
flowchart LR
    IN[projects/<project-name>/inputs/requirements/req-001.md] --> BA[BA Agent]
    BA --> OUT[projects/<project-name>/outputs/generated/req-001/]
    OUT --> STATUS[status.md updated]
    STATUS --> DASH[projects/dashboard.md updated]
```

## Notes

- Replace `<project-name>` and `req-001.md` with real names.
- Use this to explain one requirement lifecycle.
