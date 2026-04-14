# Dependency Rules

## Dependency Direction
- Requirement -> BA outputs
- FRS -> UXUI wireframe
- FRS + wireframe -> UI HTML
- All outputs -> review notes and traceability

## Dependency Types
- Functional dependency (feature/logic)
- Data dependency (required fields/rules)
- Process dependency (step order)
- Output dependency (file must exist before next stage)

## Practical Rule
- Do not run downstream assumptions without required upstream artifacts.
- If FRS is incomplete, treat UX/FE as blocked for that requirement.
- Refresh `projects/<project-name>/dependency-map.md` after runs to keep prerequisite links and risk notes current.

<!-- TODO: Add optional manual dependency tags (for example Depends-On: REQ-00X) in requirement files for richer mapping. -->
