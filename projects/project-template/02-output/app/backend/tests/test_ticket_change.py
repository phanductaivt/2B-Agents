from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_quote_change_returns_fee_breakdown():
    response = client.post(
        "/tickets/TCK-1001/change-quote",
        json={"new_travel_date": "2026-06-07"},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["fareDifference"] == 25
    assert body["changeFee"] == 15
    assert body["totalDue"] == 40
    assert body["paymentRequired"] is True


def test_confirm_change_requires_payment_when_total_due_positive():
    response = client.post(
        "/tickets/TCK-1001/confirm-change",
        json={"new_travel_date": "2026-06-07", "payment_confirmed": False},
    )

    assert response.status_code == 402
    assert response.json()["detail"]["code"] == "payment_required"


def test_confirm_change_updates_ticket_and_sends_confirmation():
    response = client.post(
        "/tickets/TCK-1002/confirm-change",
        json={"new_travel_date": "2026-06-12", "payment_confirmed": True},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "changed"
    assert body["confirmationSent"] is True
