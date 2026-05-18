---
file_type: "Factory Runbook"
primary_agents: ["PO", "BA", "Architect", "Data", "BE", "UIUX", "FE", "QA", "Release"]
supporting_agents: []
activation_mode: "Triggered By Workflow"
lifecycle_stage: "System Core"
purpose: "Create a new runtime template through the isolated Component Factory workflow."
---
# Create Template Runbook

## Purpose

Create a new runtime template that standardizes structure cleanly.

## When To Use

Use when a new document structure is needed and is not already covered by the template library.

## Prerequisites

- checked `system/templates/`
- checked document-type overlap

## Steps

1. Confirm the target document type.
2. Search for overlap in the current template folders.
3. Use `templates/template-template.md`.
4. Draft the structure with clear placeholders.
5. Produce `artifacts/component-creation-report.md`.

## Validation Checklist

- template is document-type-oriented
- placeholders are usable
- structure is not redundant with an existing template

## Expected Output

- a template definition ready for runtime placement
- a creation report

## Recovery / Rollback Note

If the need is better solved by a checklist or artifact contract, stop and redirect.
