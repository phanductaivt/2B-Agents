from __future__ import annotations

import sqlite3
from contextlib import asynccontextmanager
from datetime import date, datetime
from pathlib import Path
from typing import Any

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

DB_PATH = Path(__file__).resolve().parent / "ticket_change.db"


class QuoteRequest(BaseModel):
    new_travel_date: date = Field(..., description="Requested new travel date")


class ConfirmRequest(BaseModel):
    new_travel_date: date
    payment_confirmed: bool = False


def connect() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    with connect() as conn:
        conn.execute(
            """
            create table if not exists tickets (
                id text primary key,
                passenger_name text not null,
                route text not null,
                travel_date text not null,
                departure_date text not null,
                fare_amount integer not null,
                status text not null
            )
            """
        )
        count = conn.execute("select count(*) as total from tickets").fetchone()["total"]
        if count == 0:
            conn.executemany(
                """
                insert into tickets (
                    id, passenger_name, route, travel_date, departure_date, fare_amount, status
                ) values (?, ?, ?, ?, ?, ?, ?)
                """,
                [
                    ("TCK-1001", "Linh Nguyen", "SGN -> HAN", "2026-06-10", "2026-06-10", 120, "confirmed"),
                    ("TCK-1002", "Minh Tran", "HAN -> DAD", "2026-06-15", "2026-06-15", 95, "confirmed"),
                ],
            )


@asynccontextmanager
async def lifespan(_: FastAPI):
    init_db()
    yield


app = FastAPI(title="Ticket Change API", lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def parse_date(value: str) -> date:
    return datetime.strptime(value, "%Y-%m-%d").date()


def ticket_to_dict(row: sqlite3.Row) -> dict[str, Any]:
    return {
        "id": row["id"],
        "passengerName": row["passenger_name"],
        "route": row["route"],
        "travelDate": row["travel_date"],
        "departureDate": row["departure_date"],
        "fareAmount": row["fare_amount"],
        "status": row["status"],
    }


def load_ticket(ticket_id: str) -> sqlite3.Row:
    init_db()
    with connect() as conn:
        row = conn.execute("select * from tickets where id = ?", (ticket_id,)).fetchone()
    if row is None:
        raise HTTPException(status_code=404, detail={"code": "ticket_not_found", "message": "Ticket was not found."})
    return row


def calculate_quote(row: sqlite3.Row, new_travel_date: date) -> dict[str, Any]:
    departure_date = parse_date(row["departure_date"])
    if new_travel_date >= departure_date:
        raise HTTPException(
            status_code=400,
            detail={"code": "change_after_departure", "message": "Date change is only allowed before departure."},
        )

    day_gap = (departure_date - new_travel_date).days
    fare_difference = 25 if day_gap <= 3 else 10
    change_fee = 15
    total_due = fare_difference + change_fee
    return {
        "ticketId": row["id"],
        "newTravelDate": new_travel_date.isoformat(),
        "fareDifference": fare_difference,
        "changeFee": change_fee,
        "totalDue": total_due,
        "paymentRequired": total_due > 0,
    }


@app.get("/health")
def health() -> dict[str, str]:
    init_db()
    return {"status": "ok"}


@app.get("/tickets")
def list_tickets() -> list[dict[str, Any]]:
    init_db()
    with connect() as conn:
        rows = conn.execute("select * from tickets order by id").fetchall()
    return [ticket_to_dict(row) for row in rows]


@app.get("/tickets/{ticket_id}")
def get_ticket(ticket_id: str) -> dict[str, Any]:
    return ticket_to_dict(load_ticket(ticket_id))


@app.post("/tickets/{ticket_id}/change-quote")
def quote_change(ticket_id: str, request: QuoteRequest) -> dict[str, Any]:
    row = load_ticket(ticket_id)
    return calculate_quote(row, request.new_travel_date)


@app.post("/tickets/{ticket_id}/confirm-change")
def confirm_change(ticket_id: str, request: ConfirmRequest) -> dict[str, Any]:
    row = load_ticket(ticket_id)
    quote = calculate_quote(row, request.new_travel_date)
    if quote["paymentRequired"] and not request.payment_confirmed:
        raise HTTPException(
            status_code=402,
            detail={"code": "payment_required", "message": "Payment is required before confirming this change."},
        )

    with connect() as conn:
        conn.execute(
            "update tickets set travel_date = ?, status = ? where id = ?",
            (request.new_travel_date.isoformat(), "changed", ticket_id),
        )

    return {
        "ticketId": ticket_id,
        "status": "changed",
        "newTravelDate": request.new_travel_date.isoformat(),
        "confirmationSent": True,
        "totalPaid": quote["totalDue"],
    }
