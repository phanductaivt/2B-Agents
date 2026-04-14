# Project Flow

## Project Overview
- Project Name: ticket-booking-improvement
- Current Stage: Analysis
- Last Updated: 2026-04-15

## High-Level Flow

```mermaid
flowchart LR
    R1[inputs/requirements/req-001.md]
    BA[BA Agent]
    UX[UXUI Agent]
    FE[FE Agent]
    RV[Reviewer / Validators]
    OUT[outputs/generated/<requirement-name>/]
    R1 --> BA
    BA --> UX
    UX --> FE
    FE --> RV
    RV --> OUT
```

## Current Requirements

| Requirement | Status | BA | UXUI | FE | Reviewer | Output Folder |
|------------|--------|----|------|----|----------|---------------|
| req-001 | Done | ✅ | ✅ | ✅ | ✅ | outputs/generated/req-001 |

## Project Status Flow

```mermaid
flowchart LR
    IN[Requirement Input] --> GEN[Output Generation]
    GEN --> STATUS[status.md update]
    STATUS --> DASH[dashboard.md update]
    DASH --> HTML[dashboard.html update]
```

### Traceability: req-001.md

```mermaid
flowchart LR
    REQ[req-001.md] --> CLAR[✅ clarification.md]
    CLAR --> BPMN[✅ process-bpmn.md]
    BPMN --> STORY[✅ user-story.md]
    STORY --> AC[✅ acceptance-criteria.md]
    AC --> BRD[✅ brd.md]
    BRD --> FRS[✅ frs.md]
    FRS --> FEATURE[✅ feature-list.md]
    FEATURE --> WIRE[✅ wireframe.md]
    WIRE --> UI[✅ ui.html]
    UI --> REVIEW[✅ review-notes.md]
```

_Legend: ✅ complete, ❌ missing_
