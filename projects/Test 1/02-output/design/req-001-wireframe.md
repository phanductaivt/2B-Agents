---
file_type: "Design Artifact"
primary_agents: ["UIUX"]
supporting_agents: ["BA", "FE", "QA"]
activation_mode: "Generated Output"
lifecycle_stage: "Project Output"
purpose: "Wireframe for req-001."
---
# req-001 Wireframe

## Screen: Inventory Management

```text
┌────────────────────────────────────────────────────────────┐
│ Quản lý kho                         [Tạo / Lưu sản phẩm]   │
│ Tìm kiếm: [ mã hoặc tên sản phẩm                         ] │
├────────────────────────────────────────────────────────────┤
│ Product Code | Name | Unit | Quantity | Status | Actions   │
│ SP001        | ...  | cái  | 15       | ACTIVE | View Edit Del│
├────────────────────────────────────────────────────────────┤
│ Product Form                                                │
│ Code [readonly when editing]   Name                         │
│ Unit                         Quantity                       │
│ Minimum Stock                 Description                   │
│ [Save] [Cancel]                                              │
├────────────────────────────────────────────────────────────┤
│ Product Detail / Messages / Validation Errors               │
└────────────────────────────────────────────────────────────┘
```

## UI States

- Empty list.
- Search no result.
- Validation error.
- Save success.
- Delete confirmation.
- Status badges: ACTIVE, LOW_STOCK, OUT_OF_STOCK.
