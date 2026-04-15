# Project Flow Template

Copy this template into a project-specific visual if needed.

```mermaid
flowchart LR
    IN[projects/<project-name>/01-input/requirements/req-001.md] --> BA[BA Agent]
    BA --> OUT[projects/<project-name>/_ops/generated/req-001/]
    OUT --> CURATED[projects/<project-name>/02-output/]
    OUT --> STATUS[_ops/status.md updated]
    STATUS --> DASH[workspace/dashboard.md updated]
```

## Notes

- Replace `<project-name>` and `req-001.md` with real names.
- Use this to explain one requirement lifecycle.
