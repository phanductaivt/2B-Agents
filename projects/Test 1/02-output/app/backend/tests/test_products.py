from __future__ import annotations

import os
import tempfile
from pathlib import Path

os.environ["INVENTORY_DB_PATH"] = str(Path(tempfile.gettempdir()) / "inventory_test.db")

from fastapi.testclient import TestClient

from app.main import app, DB_PATH, init_db


def reset_db() -> None:
    if DB_PATH.exists():
        DB_PATH.unlink()
    init_db()


def client() -> TestClient:
    reset_db()
    return TestClient(app)


def test_health_and_seeded_products() -> None:
    api = client()
    assert api.get("/health").json() == {"status": "ok"}
    products = api.get("/api/products").json()
    assert len(products) == 3
    assert {item["status"] for item in products} == {"ACTIVE", "LOW_STOCK", "OUT_OF_STOCK"}


def test_create_product_and_duplicate_code_rejected() -> None:
    api = client()
    payload = {
        "product_code": "SP100",
        "product_name": "Kệ kho nhỏ",
        "description": "Kệ mini",
        "unit": "bộ",
        "quantity": 7,
        "minimum_stock": 2,
    }
    created = api.post("/api/products", json=payload)
    assert created.status_code == 201
    assert created.json()["status"] == "ACTIVE"

    duplicate = api.post("/api/products", json=payload)
    assert duplicate.status_code == 409
    assert duplicate.json()["detail"]["message"] == "Mã sản phẩm đã tồn tại"


def test_validation_and_status_transitions() -> None:
    api = client()
    product = api.get("/api/products/search", params={"keyword": "SP001"}).json()[0]

    invalid = api.patch(f"/api/products/{product['id']}/quantity", json={"quantity": -1})
    assert invalid.status_code == 400
    assert invalid.json()["detail"]["message"] == "Số lượng tồn kho không hợp lệ"

    out = api.patch(f"/api/products/{product['id']}/quantity", json={"quantity": 0}).json()
    assert out["status"] == "OUT_OF_STOCK"

    low = api.patch(f"/api/products/{product['id']}/quantity", json={"quantity": 3}).json()
    assert low["status"] == "LOW_STOCK"


def test_search_is_case_insensitive_and_delete_hides_product() -> None:
    api = client()
    found = api.get("/api/products/search", params={"keyword": "keychron"}).json()
    assert len(found) == 1
    product_id = found[0]["id"]

    deleted = api.delete(f"/api/products/{product_id}")
    assert deleted.status_code == 200
    assert deleted.json()["deleted"] is True

    after_delete = api.get("/api/products/search", params={"keyword": "keychron"}).json()
    assert after_delete == []
    missing = api.get(f"/api/products/{product_id}")
    assert missing.status_code == 404
