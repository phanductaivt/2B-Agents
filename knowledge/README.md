# Knowledge

This folder stores shared business context that agents, skills, and playbooks can reuse across many projects.

Use it for:
- domain information
- company standards
- cross-project notes
- glossary terms
- document templates

## Knowledge Priority

The system now uses knowledge in this order:
1. project knowledge in `projects/<project-name>/knowledge/`
2. shared knowledge in this `knowledge/` folder
3. generic fallback in code

The goal is to keep important knowledge consistent while still allowing each project to have its own context first.
