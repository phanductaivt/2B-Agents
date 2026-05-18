---
file_type: "QA Artifact"
primary_agents: ["QA"]
supporting_agents: ["BE", "FE", "Release"]
activation_mode: "Generated Output"
lifecycle_stage: "Project Output"
purpose: "Test cases for req-001."
---
# req-001 Test Cases

- Test Case Set ID: `TC-REQ-001`
- Parent Scenario Set: `req-001-test-scenarios.md`
- Source Requirement: `01-input/requirements/Requirement 0805.md`
- Evidence Standard: every case states preconditions, steps, expected result, evidence or execution record, and automation candidate.

## TC-001: Backend Health And Seeded Product List

- Area: List / Release smoke
- Priority: High

### Preconditions

- Backend dependencies are installed from `02-output/app/backend/requirements.txt`.
- SQLite database can be initialized by backend startup or test setup.

### Steps

1. Run `.venv/bin/pytest`.
2. Call `GET /health`.
3. Call `GET /api/products`.

### Expected Result

- Health response is `{"status":"ok"}`.
- Seeded active products are returned.
- Returned product statuses include `ACTIVE`, `LOW_STOCK`, and `OUT_OF_STOCK`.

### Evidence / Execution Record

- Evidence to capture: pytest output and `/api/products` response sample.
- Actual result: backend pytest passed, `4 passed in 0.41s`.
- Status: `pass`

### Automation Candidate

- Automation level: `api-test`
- Automation priority: High
- Automation notes: already covered by `test_health_and_seeded_products`.

## TC-002: Create Product With Valid Data

- Area: Create
- Priority: High

### Preconditions

- Backend database is reset to known seed data.
- Product code `SP100` does not already exist.

### Steps

1. Submit `POST /api/products` with valid product code, product name, unit, quantity, and minimum stock.
2. Read the response status and body.
3. Call `GET /api/products` or search for the new product code.

### Expected Result

- API returns `201`.
- Product is created with a generated ID.
- Status is calculated from quantity and minimum stock.
- Product appears in active list or search results.

### Evidence / Execution Record

- Evidence to capture: POST response body and product list/search response.
- Actual result: backend pytest passed, `4 passed in 0.41s`.
- Status: `pass`

### Automation Candidate

- Automation level: `api-test`
- Automation priority: High
- Automation notes: already covered by `test_create_product_and_duplicate_code_rejected`.

## TC-003: Reject Duplicate Product Code

- Area: Create / Validation
- Priority: High

### Preconditions

- Backend database is reset to known seed data.
- A product with code `SP100` has already been created.

### Steps

1. Submit `POST /api/products` with the same `product_code`.
2. Read the response status and error body.

### Expected Result

- API returns `409`.
- Error code is `duplicate_product_code`.
- Error message is `Mã sản phẩm đã tồn tại`.

### Evidence / Execution Record

- Evidence to capture: duplicate POST response body.
- Actual result: backend pytest passed, `4 passed in 0.41s`.
- Status: `pass`

### Automation Candidate

- Automation level: `api-test`
- Automation priority: High
- Automation notes: already covered by `test_create_product_and_duplicate_code_rejected`.

## TC-004: Reject Blank Required Product Fields

- Area: Create / Validation
- Priority: High

### Preconditions

- Backend database is reset to known seed data.
- Create or update payload can be submitted with blank field values.

### Steps

1. Submit create or update data with blank `product_name`.
2. Submit create or update data with blank `unit`.
3. Read the response status and error body for each request.

### Expected Result

- Blank product name is rejected with `Tên sản phẩm không được để trống`.
- Blank unit is rejected with `Đơn vị tính không được để trống`.
- No invalid product is persisted.

### Evidence / Execution Record

- Evidence to capture: API error responses and follow-up list/search proving no invalid record exists.
- Actual result: blank product name/unit should be added to automated coverage; related validation logic exists in backend.
- Status: `not-run`

### Automation Candidate

- Automation level: `api-test`
- Automation priority: High
- Automation notes: add pytest assertions for blank name and blank unit before production hardening.

## TC-005: Reject Negative Quantity

- Area: Quantity / Validation
- Priority: High

### Preconditions

- Backend database is reset to known seed data.
- At least one active product exists.

### Steps

1. Find an active product by `GET /api/products/search?keyword=SP001`.
2. Submit `PATCH /api/products/{id}/quantity` with `quantity = -1`.
3. Read the response status and error body.

### Expected Result

- API returns `400`.
- Error code is `validation_error`.
- Error message is `Số lượng tồn kho không hợp lệ`.
- Product quantity remains unchanged.

### Evidence / Execution Record

- Evidence to capture: PATCH error response and follow-up product detail response.
- Actual result: backend pytest passed, `4 passed in 0.41s`.
- Status: `pass`

### Automation Candidate

- Automation level: `api-test`
- Automation priority: High
- Automation notes: already covered by `test_validation_and_status_transitions`.

## TC-006: Search Is Case-Insensitive

- Area: Search
- Priority: High

### Preconditions

- Backend database is reset to known seed data.
- Seed product name contains `Keychron`.

### Steps

1. Call `GET /api/products/search?keyword=keychron`.
2. Inspect returned products.

### Expected Result

- Matching product is returned even though the search keyword uses lowercase.
- Deleted products are not returned.

### Evidence / Execution Record

- Evidence to capture: search request and response.
- Actual result: backend pytest passed, `4 passed in 0.41s`.
- Status: `pass`

### Automation Candidate

- Automation level: `api-test`
- Automation priority: High
- Automation notes: already covered by `test_search_is_case_insensitive_and_delete_hides_product`.

## TC-007: View Missing Or Deleted Product

- Area: Detail / Soft delete
- Priority: High

### Preconditions

- Backend database is reset to known seed data.
- A product is deleted through `DELETE /api/products/{id}`.

### Steps

1. Delete an active product.
2. Call `GET /api/products/{id}` for the deleted product.
3. Read the response status and error body.

### Expected Result

- API returns `404`.
- Error code is `product_not_found`.
- Error message is `Sản phẩm không tồn tại`.

### Evidence / Execution Record

- Evidence to capture: DELETE response and subsequent GET error response.
- Actual result: backend pytest passed, `4 passed in 0.41s`.
- Status: `pass`

### Automation Candidate

- Automation level: `api-test`
- Automation priority: High
- Automation notes: already covered by `test_search_is_case_insensitive_and_delete_hides_product`.

## TC-008: Update Product Information

- Area: Update
- Priority: High

### Preconditions

- Backend database is reset to known seed data.
- At least one active product exists.

### Steps

1. Call `PUT /api/products/{id}` with updated product name, description, unit, and minimum stock.
2. Read the response body.
3. Fetch the product detail again.

### Expected Result

- Product fields are updated.
- `updated_at` changes.
- Product code remains unchanged.
- Status is recalculated if minimum stock changes the status rule.

### Evidence / Execution Record

- Evidence to capture: PUT response, before/after product detail, and timestamp comparison.
- Actual result: not covered by current backend pytest.
- Status: `not-run`

### Automation Candidate

- Automation level: `api-test`
- Automation priority: High
- Automation notes: add pytest coverage for update and `updated_at` before production hardening.

## TC-009: Quantity Status Transitions

- Area: Quantity / Status
- Priority: High

### Preconditions

- Backend database is reset to known seed data.
- Selected product has `minimum_stock = 5`.

### Steps

1. Set quantity to `0`.
2. Set quantity to `3`.
3. Set quantity to a value above minimum stock.
4. Read product status after each update.

### Expected Result

- Quantity `0` sets status to `OUT_OF_STOCK`.
- Quantity greater than `0` and less than or equal to minimum stock sets status to `LOW_STOCK`.
- Quantity greater than minimum stock sets status to `ACTIVE`.

### Evidence / Execution Record

- Evidence to capture: PATCH responses for each transition.
- Actual result: current backend pytest covers `OUT_OF_STOCK` and `LOW_STOCK`; `ACTIVE` transition should be added.
- Status: `partially-covered`

### Automation Candidate

- Automation level: `api-test`
- Automation priority: High
- Automation notes: extend `test_validation_and_status_transitions` to assert the `ACTIVE` branch.

## TC-010: Confirm Delete Hides Product From List And Search

- Area: Delete / Soft delete
- Priority: High

### Preconditions

- Backend database is reset to known seed data.
- Product selected for deletion is active and visible in search.

### Steps

1. Call `DELETE /api/products/{id}`.
2. Search for the deleted product by name or code.
3. Call `GET /api/products`.

### Expected Result

- Delete response confirms `deleted = true`.
- Deleted product no longer appears in search.
- Deleted product no longer appears in active list.

### Evidence / Execution Record

- Evidence to capture: DELETE response, search response, and list response.
- Actual result: backend pytest passed, `4 passed in 0.41s`.
- Status: `pass`

### Automation Candidate

- Automation level: `api-test`
- Automation priority: High
- Automation notes: already covered by `test_search_is_case_insensitive_and_delete_hides_product`; list exclusion can be asserted more explicitly.

## TC-011: Cancel Delete In UI

- Area: Delete / UI behavior
- Priority: Medium

### Preconditions

- Frontend app is running against the backend.
- A visible active product exists.

### Steps

1. Click the delete action for an active product.
2. Cancel the confirmation dialog or modal.
3. Return to the product list.

### Expected Result

- Product remains visible.
- No `DELETE /api/products/{id}` request is sent after cancel.
- No success deletion message is shown.

### Evidence / Execution Record

- Evidence to capture: screenshot or browser devtools/network log showing cancel behavior.
- Actual result: not automated in current repo.
- Status: `not-run`

### Automation Candidate

- Automation level: `ui-e2e`
- Automation priority: Medium
- Automation notes: add Playwright after the repo adopts browser automation.

## TC-012: Local Release Verification Commands

- Area: Release
- Priority: High

### Preconditions

- Backend and frontend dependency setup can run locally.
- `02-output/release/req-001-run-instructions.md` is available.

### Steps

1. Run backend tests with `.venv/bin/pytest`.
2. Run frontend build with `npm run build`.
3. Review `02-output/release/req-001-runnable-system-verification.md`.

### Expected Result

- Backend tests pass.
- Frontend build succeeds.
- Release verification separates local runnable status from production readiness.

### Evidence / Execution Record

- Evidence to capture: pytest output, Vite build output, and release verification artifact.
- Actual result: backend pytest passed, `4 passed in 0.41s`; frontend build passed.
- Status: `pass`

### Automation Candidate

- Automation level: `smoke-test`
- Automation priority: High
- Automation notes: move to CI after `.github/workflows` is introduced.
