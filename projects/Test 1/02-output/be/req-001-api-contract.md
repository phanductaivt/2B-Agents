---
file_type: "BE Artifact"
primary_agents: ["BE"]
supporting_agents: ["FE", "QA"]
activation_mode: "Generated Output"
lifecycle_stage: "Project Output"
purpose: "API contract for req-001."
---
# req-001 API Contract

## Endpoints

- `GET /health`
- `GET /api/products`
- `GET /api/products/search?keyword=<keyword>`
- `GET /api/products/{id}`
- `POST /api/products`
- `PUT /api/products/{id}`
- `PATCH /api/products/{id}/quantity`
- `DELETE /api/products/{id}`

## Product Response

```json
{
  "id": "uuid",
  "productCode": "SP001",
  "productName": "Bàn phím cơ Keychron K2",
  "description": "Bàn phím cơ không dây",
  "unit": "cái",
  "quantity": 15,
  "minimumStock": 5,
  "status": "ACTIVE",
  "createdAt": "2026-05-09T00:00:00Z",
  "updatedAt": "2026-05-09T00:00:00Z"
}
```

## Error Response

```json
{
  "detail": {
    "code": "validation_error",
    "message": "Tên sản phẩm không được để trống"
  }
}
```
