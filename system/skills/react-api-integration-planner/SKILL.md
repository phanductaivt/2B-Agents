---
name: react-api-integration-planner
description: Plan how a React frontend consumes API endpoints, handles responses, and presents errors. Use before or during FE implementation when backend contract matters.
---
# React API Integration Planner

## Use When

- FE depends on BE endpoints and response branches
- API errors or validation responses change UI behavior

## Output

A Markdown API integration plan covering:
- endpoint usage by screen/action
- request payloads
- response fields consumed by UI
- error mapping
- retry or recovery behavior

## Rules

- align endpoint names with the BE API contract
- do not invent response fields
- flag conflicts between UI and API behavior
