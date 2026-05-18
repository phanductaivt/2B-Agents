from __future__ import annotations

import os
import sqlite3
import uuid
from contextlib import asynccontextmanager
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Optional

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field


DB_PATH = Path(os.getenv("INVENTORY_DB_PATH", Path(__file__).resolve().parent / "inventory.db"))


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def connect() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def calculate_status(quantity: int, minimum_stock: Optional[int]) -> str:
    if quantity == 0:
        return "OUT_OF_STOCK"
    if minimum_stock is not None and quantity <= minimum_stock:
        return "LOW_STOCK"
    return "ACTIVE"


def validate_non_negative(value: Optional[int], message: str) -> None:
    if value is not None and value < 0:
        raise HTTPException(status_code=400, detail={"code": "validation_error", "message": message})


def clean_text(value: Optional[str]) -> str:
    return (value or "").strip()


class ProductCreate(BaseModel):
    product_code: str = Field(..., max_length=50)
    product_name: str = Field(..., max_length=255)
    description: Optional[str] = Field(default="", max_length=1000)
    unit: str
    quantity: int
    minimum_stock: Optional[int] = None


class ProductUpdate(BaseModel):
    product_name: str = Field(..., max_length=255)
    description: Optional[str] = Field(default="", max_length=1000)
    unit: str
    minimum_stock: Optional[int] = None


class QuantityUpdate(BaseModel):
    quantity: int


def init_db() -> None:
    with connect() as conn:
        conn.execute(
            """
            create table if not exists products (
                id text primary key,
                product_code text not null unique,
                product_name text not null,
                description text,
                unit text not null,
                quantity integer not null,
                minimum_stock integer,
                status text not null,
                is_deleted integer not null default 0,
                created_at text not null,
                updated_at text not null
            )
            """
        )
        conn.execute("create index if not exists idx_products_code on products(product_code)")
        conn.execute("create index if not exists idx_products_name on products(product_name)")
        conn.execute("create index if not exists idx_products_deleted on products(is_deleted)")
        count = conn.execute("select count(*) as total from products").fetchone()["total"]
        if count == 0:
            timestamp = now_iso()
            seed_rows = [
                ("SP001", "Bàn phím cơ Keychron K2", "Bàn phím cơ không dây", "cái", 15, 5),
                ("SP002", "Chuột Logitech MX Master 3S", "Chuột không dây văn phòng", "cái", 3, 5),
                ("SP003", "Màn hình Dell 24 inch", "Màn hình văn phòng", "cái", 0, 2),
            ]
            conn.executemany(
                """
                insert into products (
                    id, product_code, product_name, description, unit, quantity,
                    minimum_stock, status, is_deleted, created_at, updated_at
                ) values (?, ?, ?, ?, ?, ?, ?, ?, 0, ?, ?)
                """,
                [
                    (
                        str(uuid.uuid4()),
                        code,
                        name,
                        description,
                        unit,
                        quantity,
                        minimum_stock,
                        calculate_status(quantity, minimum_stock),
                        timestamp,
                        timestamp,
                    )
                    for code, name, description, unit, quantity, minimum_stock in seed_rows
                ],
            )


@asynccontextmanager
async def lifespan(_: FastAPI):
    init_db()
    yield


app = FastAPI(title="Basic Inventory Management API", lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def product_to_dict(row: sqlite3.Row) -> dict[str, Any]:
    return {
        "id": row["id"],
        "productCode": row["product_code"],
        "productName": row["product_name"],
        "description": row["description"] or "",
        "unit": row["unit"],
        "quantity": row["quantity"],
        "minimumStock": row["minimum_stock"],
        "status": row["status"],
        "createdAt": row["created_at"],
        "updatedAt": row["updated_at"],
    }


def validate_product_create(payload: ProductCreate) -> None:
    if not clean_text(payload.product_code):
        raise HTTPException(status_code=400, detail={"code": "validation_error", "message": "Mã sản phẩm không được để trống"})
    validate_product_fields(payload.product_name, payload.unit, payload.quantity, payload.minimum_stock)


def validate_product_fields(product_name: str, unit: str, quantity: Optional[int], minimum_stock: Optional[int]) -> None:
    if not clean_text(product_name):
        raise HTTPException(status_code=400, detail={"code": "validation_error", "message": "Tên sản phẩm không được để trống"})
    if not clean_text(unit):
        raise HTTPException(status_code=400, detail={"code": "validation_error", "message": "Đơn vị tính không được để trống"})
    if quantity is not None:
        validate_non_negative(quantity, "Số lượng tồn kho không hợp lệ")
    validate_non_negative(minimum_stock, "Tồn kho tối thiểu không hợp lệ")


def load_active_product(product_id: str) -> sqlite3.Row:
    init_db()
    with connect() as conn:
        row = conn.execute("select * from products where id = ? and is_deleted = 0", (product_id,)).fetchone()
    if row is None:
        raise HTTPException(status_code=404, detail={"code": "product_not_found", "message": "Sản phẩm không tồn tại"})
    return row


@app.get("/health")
def health() -> dict[str, str]:
    init_db()
    return {"status": "ok"}


@app.get("/api/products")
def list_products() -> list[dict[str, Any]]:
    init_db()
    with connect() as conn:
        rows = conn.execute("select * from products where is_deleted = 0 order by product_code").fetchall()
    return [product_to_dict(row) for row in rows]


@app.get("/api/products/search")
def search_products(keyword: str = Query(default="")) -> list[dict[str, Any]]:
    init_db()
    term = f"%{keyword.strip().lower()}%"
    with connect() as conn:
        rows = conn.execute(
            """
            select * from products
            where is_deleted = 0
            and (lower(product_code) like ? or lower(product_name) like ?)
            order by product_code
            """,
            (term, term),
        ).fetchall()
    return [product_to_dict(row) for row in rows]


@app.get("/api/products/{product_id}")
def get_product(product_id: str) -> dict[str, Any]:
    return product_to_dict(load_active_product(product_id))


@app.post("/api/products", status_code=201)
def create_product(payload: ProductCreate) -> dict[str, Any]:
    init_db()
    validate_product_create(payload)
    timestamp = now_iso()
    product_id = str(uuid.uuid4())
    status = calculate_status(payload.quantity, payload.minimum_stock)
    try:
        with connect() as conn:
            conn.execute(
                """
                insert into products (
                    id, product_code, product_name, description, unit, quantity,
                    minimum_stock, status, is_deleted, created_at, updated_at
                ) values (?, ?, ?, ?, ?, ?, ?, ?, 0, ?, ?)
                """,
                (
                    product_id,
                    clean_text(payload.product_code),
                    clean_text(payload.product_name),
                    clean_text(payload.description),
                    clean_text(payload.unit),
                    payload.quantity,
                    payload.minimum_stock,
                    status,
                    timestamp,
                    timestamp,
                ),
            )
    except sqlite3.IntegrityError as exc:
        raise HTTPException(status_code=409, detail={"code": "duplicate_product_code", "message": "Mã sản phẩm đã tồn tại"}) from exc
    return get_product(product_id)


@app.put("/api/products/{product_id}")
def update_product(product_id: str, payload: ProductUpdate) -> dict[str, Any]:
    row = load_active_product(product_id)
    validate_product_fields(payload.product_name, payload.unit, row["quantity"], payload.minimum_stock)
    timestamp = now_iso()
    status = calculate_status(row["quantity"], payload.minimum_stock)
    with connect() as conn:
        conn.execute(
            """
            update products
            set product_name = ?, description = ?, unit = ?, minimum_stock = ?,
                status = ?, updated_at = ?
            where id = ? and is_deleted = 0
            """,
            (
                clean_text(payload.product_name),
                clean_text(payload.description),
                clean_text(payload.unit),
                payload.minimum_stock,
                status,
                timestamp,
                product_id,
            ),
        )
    return get_product(product_id)


@app.patch("/api/products/{product_id}/quantity")
def update_quantity(product_id: str, payload: QuantityUpdate) -> dict[str, Any]:
    row = load_active_product(product_id)
    validate_non_negative(payload.quantity, "Số lượng tồn kho không hợp lệ")
    timestamp = now_iso()
    status = calculate_status(payload.quantity, row["minimum_stock"])
    with connect() as conn:
        conn.execute(
            "update products set quantity = ?, status = ?, updated_at = ? where id = ? and is_deleted = 0",
            (payload.quantity, status, timestamp, product_id),
        )
    return get_product(product_id)


@app.delete("/api/products/{product_id}")
def delete_product(product_id: str) -> dict[str, Any]:
    load_active_product(product_id)
    with connect() as conn:
        conn.execute(
            "update products set is_deleted = 1, updated_at = ? where id = ? and is_deleted = 0",
            (now_iso(), product_id),
        )
    return {"id": product_id, "deleted": True, "message": "Xoá sản phẩm thành công"}
