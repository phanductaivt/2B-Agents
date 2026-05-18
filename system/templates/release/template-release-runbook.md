---
file_type: "Template"
primary_agents: ["Release"]
supporting_agents: ["QA", "BE", "FE"]
activation_mode: "On-Demand Reference"
lifecycle_stage: "System Core"
purpose: "Provide the standard structure for local run instructions and release discussion notes."
---
# Template - Release Runbook

## 1. Prerequisites

- project:
- requirement:
- backend path:
- frontend path:
- backend URL:
- frontend URL:
- health check URL:

## 2. Terminal 1 - Backend

- setup commands:
- test command:
- run command:
- expected startup:

## 3. Terminal 2 - Frontend

- setup command:
- build command:
- run command:
- expected startup:

## 4. Database

- setup/reset:
- seed data:

## 5. Browser Smoke Flow

- steps:
- expected result:

## 6. Troubleshooting

- if backend fails:
- if frontend fails:
- if API calls fail:
- if ports are busy:

## 7. Readiness Notes

- blockers:
- known gaps:
- recommendation:
