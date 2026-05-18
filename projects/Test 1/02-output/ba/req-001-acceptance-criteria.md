---
file_type: "BA Artifact"
primary_agents: ["BA"]
supporting_agents: ["QA", "FE", "BE"]
activation_mode: "Generated Output"
lifecycle_stage: "Project Output"
purpose: "Acceptance criteria for req-001."
---
# req-001 Acceptance Criteria

## Create Product

- AC-001: Given valid product data, when the user saves, then the system creates the product and shows it in the list.
- AC-002: Given duplicate product code, when the user saves, then the system shows "Mã sản phẩm đã tồn tại".
- AC-003: Given blank product name, when the user saves, then the system shows "Tên sản phẩm không được để trống".
- AC-004: Given negative quantity, when the user saves, then the system shows "Số lượng tồn kho không hợp lệ".

## View And Search

- AC-005: Given active products exist, when the user opens the list, then active products are shown.
- AC-006: Given no active products exist, when the user opens the list, then the UI shows "Chưa có sản phẩm trong kho".
- AC-007: Given a keyword matches code or name regardless of case, when the user searches, then matching active products are shown.
- AC-008: Given no match exists, when the user searches, then the UI shows "Không tìm thấy sản phẩm phù hợp".

## Detail And Update

- AC-009: Given an active product, when the user selects it, then full product detail is shown.
- AC-010: Given valid update data, when the user saves, then the product is updated and updated_at changes.
- AC-011: Given invalid minimum stock, when the user saves, then the system shows "Tồn kho tối thiểu không hợp lệ".

## Quantity And Status

- AC-012: Given quantity is updated to 0, then status becomes OUT_OF_STOCK.
- AC-013: Given quantity is greater than 0 and less than or equal to minimum stock, then status becomes LOW_STOCK.
- AC-014: Given quantity is greater than minimum stock or minimum stock is empty, then status becomes ACTIVE.

## Delete

- AC-015: Given the user confirms delete, when the system deletes the product, then it no longer appears in list or search.
- AC-016: Given the user cancels delete, then the product remains visible.
- AC-017: Given a deleted or missing product is requested, then the system shows "Sản phẩm không tồn tại".
