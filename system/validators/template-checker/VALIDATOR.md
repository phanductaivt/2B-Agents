# Template Checker

## Name

Template Checker

## Purpose

Check whether a Markdown document follows the expected business template.

## What To Check

- required headings
- section order if needed
- mandatory fields
- format rules for the target output
- whether the file still remains readable and editable as Markdown
- whether `process-bpmn.md` contains a readable Mermaid block
- whether assumptions are clearly labeled as assumptions and not mixed into facts
- whether review notes clearly show pass or fail status
- whether `frs.md` clearly separates functional requirements, business rules, and edge cases
- whether `frs.md` includes a readable Main Flow and Alternative Flows section
- whether `feature-list.md` uses clear Level 1, Level 2, and Level 3 headings

## Pass/Fail Logic

- pass: the document follows the chosen template well enough for review
- fail: required sections or fields are missing, or assumptions are not clearly labeled

## Example Issues

- PRD has no "Out of Scope" section
- story template is missing the user role
- meeting notes do not include decisions or actions
- clarification mixes assumptions into "Known Facts"
- review notes list issues but do not show an overall validation status
- FRS hides business rules inside general requirement text with no separate section
- feature-list.md uses bullets only and never shows clear Level 1, Level 2, and Level 3 headings
- FRS is missing a Main Flow or Alternative Flows section
