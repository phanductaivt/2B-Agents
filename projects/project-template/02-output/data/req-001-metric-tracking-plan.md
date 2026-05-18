---
file_type: "Data Artifact"
primary_agents: ["Data"]
supporting_agents: ["PO", "BA", "BE", "FE", "QA"]
activation_mode: "Generated Output"
lifecycle_stage: "Project Output"
purpose: "Show the expected quality and structure of the metric tracking plan artifact."
---
# Metric Tracking Plan: Ticket Booking Modification Improvement

## 1. Feature And Decision Context

- Feature: online ticket booking modification.
- PO decision this plan supports: decide whether customers can understand eligibility, fees, and fallback paths well enough to reduce avoidable support contact.
- Source BRD: `02-output/po/req-001-brd.md`
- Source FRS: `02-output/ba/req-001-frs.md`
- Source acceptance criteria: `02-output/ba/req-001-acceptance-criteria.md`
- Source FE/API artifacts: `02-output/be/req-001-api-contract.md`, `02-output/design/req-001-wireframe.md`

## 2. Measurement Framework

- selected framework or hybrid: Funnel + Guardrail Metrics.
- why this framework fits: the feature has a clear customer journey from eligibility check to fee review to confirmation or support fallback.
- why other common frameworks are not primary: AARRR is too growth-oriented; HEART can be added later when satisfaction feedback exists.
- downstream alignment needed: FE tracks customer intent and viewed states, BE tracks eligibility/fee/confirmation outcomes, QA verifies the critical event sequence.

## 3. Key Metrics

- Metric: Online modification funnel completion rate
- Type: funnel
- Why PO cares: shows whether customers can move from starting a change to completing an eligible modification.
- How to calculate: confirmed online modifications divided by modification flows started.
- How to read: a drop between fee review and confirmation may mean fee surprise, unclear copy, or payment/reissue complexity.
- Related tracking events: `booking_change_started`, `booking_change_eligibility_returned`, `booking_change_fee_viewed`, `booking_change_confirmed`
- Decision scenarios: If eligibility passes but confirmation is low, PO reviews fee communication and confirmation friction before expanding rules.

- Metric: Support fallback rate
- Type: guardrail
- Why PO cares: the business goal is not met if customers still need support after trying online change.
- How to calculate: support fallback events divided by modification flows started.
- How to read: high fallback can be acceptable for ineligible cases, but unhealthy for eligible or fee-ready cases.
- Related tracking events: `booking_change_support_fallback_shown`, `booking_change_failed`
- Decision scenarios: If fallback is high for eligible bookings, prioritize missing online handling over marketing the feature.

- Metric: Fee transparency view rate
- Type: behavior
- Why PO cares: customers should see fee information before deciding whether to continue.
- How to calculate: fee viewed events divided by eligible modification flows.
- How to read: low fee visibility means the first slice is not meeting the transparency goal.
- Related tracking events: `booking_change_fee_viewed`
- Decision scenarios: If fee view rate is low, fix fee retrieval, placement, or copy before optimizing confirmation.

## 4. Tracking Events And Actions

- Event/action name: `booking_change_started`
- Trigger: customer starts changing an existing booking.
- Source: FE screen
- Actor: customer
- Required properties: `booking_id_present`, `source_view`
- Optional properties: `channel`
- Related metric: Online modification funnel completion rate
- Expected timing: immediately after customer enters the change flow.
- Verification: QA starts the change flow and confirms one event fires.
- Notes for dev: do not include passenger name or payment details.
- Privacy note: use booking ID presence or hashed reference only if approved.

- Event/action name: `booking_change_eligibility_returned`
- Trigger: backend returns online-change eligibility.
- Source: BE endpoint
- Actor: system
- Required properties: `eligibility_status`, `rejection_reason`, `response_status`
- Optional properties: `fare_rule_category`
- Related metric: Online modification funnel completion rate; Support fallback rate
- Expected timing: after eligibility evaluation completes.
- Verification: QA covers eligible and ineligible bookings.
- Notes for dev: rejection_reason must use stable categories.
- Privacy note: do not send passenger identity or raw fare rule text.

- Event/action name: `booking_change_fee_viewed`
- Trigger: customer sees fee or fare difference before confirmation.
- Source: FE screen
- Actor: customer
- Required properties: `fee_available`, `fee_bucket`, `currency`
- Optional properties: `fare_difference_bucket`
- Related metric: Fee transparency view rate
- Expected timing: when fee section is rendered to the customer.
- Verification: QA confirms event fires only after fee information is visible.
- Notes for dev: bucket fee values if analytics policy does not allow exact amounts.
- Privacy note: avoid full payment or card data.

- Event/action name: `booking_change_confirmed`
- Trigger: backend confirms the booking change.
- Source: BE endpoint
- Actor: customer
- Required properties: `confirmation_status`, `response_status`
- Optional properties: `fee_bucket`
- Related metric: Online modification funnel completion rate
- Expected timing: after final confirmation succeeds.
- Verification: QA confirms event follows successful confirmation response.
- Notes for dev: confirmation_status should reflect final backend result, not button click intent.
- Privacy note: do not include passenger or payment details.

- Event/action name: `booking_change_support_fallback_shown`
- Trigger: customer is directed to support because online change cannot continue.
- Source: FE screen
- Actor: customer
- Required properties: `fallback_reason`, `eligibility_status`
- Optional properties: `source_step`
- Related metric: Support fallback rate
- Expected timing: when support guidance is visible.
- Verification: QA triggers ineligible and dependency-failure paths.
- Notes for dev: separate policy fallback from technical failure.
- Privacy note: do not include customer contact details.

## 5. Reading Metrics Together

- signal combination: eligibility pass high, fee view high, confirmation low.
- likely interpretation: customers understand eligibility and fees but hesitate at final confirmation.
- PO action to consider: review fee copy, confidence messaging, and confirmation UX.

- signal combination: eligibility pass low, support fallback high.
- likely interpretation: policy constraints limit online value more than UX does.
- PO action to consider: review rules for which booking changes should be enabled online.

- signal combination: confirmation rate high, support fallback high.
- likely interpretation: eligible users succeed, but many customers are still outside supported scope.
- PO action to consider: expand eligibility or improve pre-entry guidance.

## 6. Visual Tracking Summary

### Event Tracking Matrix

| Event/action | Trigger | Source | Actor | Required properties | Related metric | Verification | Privacy note |
|---|---|---|---|---|---|---|---|
| `booking_change_started` | Customer starts changing an existing booking | FE screen | customer | `booking_id_present`, `source_view` | Online modification funnel completion rate | QA starts the change flow and confirms one event fires | Do not include passenger name or payment details |
| `booking_change_eligibility_returned` | Backend returns online-change eligibility | BE endpoint | system | `eligibility_status`, `rejection_reason`, `response_status` | Online modification funnel completion rate; Support fallback rate | QA covers eligible and ineligible bookings | Do not send passenger identity or raw fare rule text |
| `booking_change_fee_viewed` | Customer sees fee or fare difference before confirmation | FE screen | customer | `fee_available`, `fee_bucket`, `currency` | Fee transparency view rate | QA confirms event fires only after fee information is visible | Avoid full payment or card data |
| `booking_change_confirmed` | Backend confirms the booking change | BE endpoint | customer | `confirmation_status`, `response_status` | Online modification funnel completion rate | QA confirms event follows successful confirmation response | Do not include passenger or payment details |
| `booking_change_support_fallback_shown` | Customer is directed to support because online change cannot continue | FE screen | customer | `fallback_reason`, `eligibility_status` | Support fallback rate | QA triggers ineligible and dependency-failure paths | Do not include customer contact details |

### Metric To Event Map

| Metric | Events needed | What this proves | Risk if missing |
|---|---|---|---|
| Online modification funnel completion rate | `booking_change_started`, `booking_change_eligibility_returned`, `booking_change_fee_viewed`, `booking_change_confirmed` | Customers can move through the online change journey | PO cannot locate funnel drop-off or prove online completion |
| Support fallback rate | `booking_change_support_fallback_shown`, `booking_change_eligibility_returned` | Customers still need support or policy fallback after trying online change | PO may overstate feature success and miss unsupported customer groups |
| Fee transparency view rate | `booking_change_fee_viewed`, `booking_change_eligibility_returned` | Eligible customers saw fee information before deciding | PO cannot prove the transparency goal is being met |

### Reading And Decision Matrix

| Signal combination | Likely interpretation | PO action to consider | Agent to involve |
|---|---|---|---|
| Eligibility pass high + fee view high + confirmation low | Customers understand eligibility and fees but hesitate at final confirmation | Review fee copy, confidence messaging, and confirmation UX | PO, UIUX, FE |
| Eligibility pass low + support fallback high | Policy constraints limit online value more than UX does | Review which booking changes should be enabled online | PO, BA, BE |
| Confirmation rate high + support fallback high | Eligible users succeed, but many customers are still outside supported scope | Expand eligibility or improve pre-entry guidance | PO, BA |

## 7. Gaps And Assumptions

- gap or assumption: reduction target for avoidable support contact is still missing.
- impact: first release can establish baseline but cannot prove target achievement.
- owner to clarify: PO.

- gap or assumption: analytics SDK and dashboard are out of scope for this template output.
- impact: this artifact guides tracking implementation but does not prove events are live.
- owner to clarify: Data/FE/BE before production rollout.
