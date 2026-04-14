# Ambiguity Checker

## Name

Ambiguity Checker

## Purpose

Find vague wording that makes a Markdown draft hard to understand or test.

## What To Check

- unclear adjectives such as "fast" or "simple"
- missing open questions where detail is still weak
- statements that cannot be measured or observed
- vague wording inside `clarification.md`, `user-story.md`, `brd.md`, or `frs.md`
- assumptions that use words such as "maybe", "probably", "some", or "etc"
- unclear references such as "this", "that", or "the process" when the subject is not obvious

## Pass/Fail Logic

- pass: wording is specific enough for review and next-step drafting
- fail: vague wording blocks shared understanding, hides missing detail, or leaves assumptions too unclear to review

## Example Issues

- "The screen should be user-friendly."
- "The process should be faster."
- "The system should work smoothly."
- "Maybe some requests need manager approval."
- "This should be handled better."
