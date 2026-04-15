# Tests

This folder holds simple testing notes for manual checks.

Suggested quick test:

```bash
python3 app.py --project ticket-booking-improvement --input req-001.md
```

Then review:

- `projects/ticket-booking-improvement/_ops/generated/req-001/clarification.md`
- `projects/ticket-booking-improvement/_ops/generated/req-001/process-bpmn.md`
- `projects/ticket-booking-improvement/_ops/generated/req-001/user-story.md`
- `projects/ticket-booking-improvement/_ops/generated/req-001/acceptance-criteria.md`
- `projects/ticket-booking-improvement/_ops/generated/req-001/brd.md`
- `projects/ticket-booking-improvement/_ops/generated/req-001/frs.md`
- `projects/ticket-booking-improvement/_ops/generated/req-001/feature-list.md`
- `projects/ticket-booking-improvement/_ops/generated/req-001/wireframe.md`
- `projects/ticket-booking-improvement/_ops/generated/req-001/review-notes.md`
- `projects/ticket-booking-improvement/_ops/generated/req-001/ui.html`

The main business check is simple:
- the BA package should already contain the feature list
- the UXUI wireframe should follow the BA FRS
- the FE HTML should still match the BA FRS and wireframe
