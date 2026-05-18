---
file_type: "BA Artifact"
primary_agents: ["BA"]
supporting_agents: ["PO", "UIUX", "FE", "BE", "QA"]
activation_mode: "Generated Output"
lifecycle_stage: "Project Output"
purpose: "Functional requirement specification for req-001."
---
# req-001 FRS

## Functional Summary

The system lets a warehouse staff user manage a simple product inventory list. The user can create, browse, search, view detail, update product information, update quantity, and delete products. The system validates input and calculates stock status automatically.

## Actor

- ACT-001: Warehouse staff.

## Functional Requirements

- FR-001: User can create a product with product code, name, description, unit, quantity, and minimum stock.
- FR-002: User can view active products in a list.
- FR-003: User can search active products by product code or product name, case-insensitively.
- FR-004: User can view product detail.
- FR-005: User can update product name, description, unit, and minimum stock.
- FR-006: User can update current quantity.
- FR-007: User can delete a product after confirmation.
- FR-008: System calculates status as ACTIVE, LOW_STOCK, or OUT_OF_STOCK.

## Main Flow

1. User opens inventory management screen.
2. System loads active products.
3. User creates or selects a product.
4. System validates the request.
5. System saves data and recalculates stock status.
6. System refreshes list/detail with updated data.

## Alternative Flows

- Duplicate product code: reject create with "Mã sản phẩm đã tồn tại".
- Missing product name: reject create/update with "Tên sản phẩm không được để trống".
- Missing product code: reject create with "Mã sản phẩm không được để trống".
- Missing unit: reject create/update with "Đơn vị tính không được để trống".
- Negative quantity: reject create/quantity update with "Số lượng tồn kho không hợp lệ".
- Negative minimum stock: reject create/update with "Tồn kho tối thiểu không hợp lệ".
- Product not found or deleted: return "Sản phẩm không tồn tại".

## Business Rules

- BR-001: Product code is unique.
- BR-002: Product name is required.
- BR-003: Quantity must be greater than or equal to 0.
- BR-004: Quantity 0 means OUT_OF_STOCK.
- BR-005: Quantity greater than 0 and less than or equal to minimum stock means LOW_STOCK.
- BR-006: Quantity greater than minimum stock, or no minimum stock, means ACTIVE.
- BR-007: Deletion requires user confirmation in UI.
- BR-008: Deleted products do not appear in list or search.
- BR-009: Update operations refresh updated_at.
- BR-010: Search is case-insensitive.

## Dependencies

- Backend CRUD API.
- SQLite persistence.
- React frontend connected to the API.
- QA verification for status and validation branches.
