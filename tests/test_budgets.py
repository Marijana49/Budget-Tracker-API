from decimal import Decimal

def test_create_budget(client):
    category = client.post("/categories", json={"name": "Hrana", "color": "#27AE60"},).json()

    response = client.post("/budgets", json={"month": "2026-10-01", "amount": "500.00", "category_id": category["id"],},)

    assert response.status_code == 201

    data = response.json()
    assert data["month"] == "2026-10-01"
    assert Decimal(data["amount"]) == Decimal("500.00")
    assert data["category_id"] == category["id"]


def test_create_budget_with_negative_amount(client):
    category = client.post("/categories", json={"name": "Hrana", "color": "#27AE60"},).json()

    response = client.post("/budgets", json={"month": "2026-10-01", "amount": "-100.00", "category_id": category["id"],},)

    assert response.status_code == 422


def test_create_budget_with_zero_amount(client):
    category = client.post("/categories", json={"name": "Hrana", "color": "#27AE60"},).json()

    response = client.post("/budgets", json={"month": "2026-10-01", "amount": "0", "category_id": category["id"],},)

    assert response.status_code == 422


def test_create_budget_with_invalid_category(client):
    response = client.post("/budgets", json={
            "month": "2026-10-01",
            "amount": "500.00",
            "category_id": 999999,
        },
    )

    assert response.status_code == 404


def test_duplicate_budget_for_same_month(client):
    category = client.post("/categories", json={"name": "Hrana", "color": "#27AE60"},).json()

    payload = {"month": "2026-10-01", "amount": "500.00", "category_id": category["id"],}

    first_response = client.post("/budgets", json=payload)
    assert first_response.status_code == 201

    second_response = client.post("/budgets", json=payload)
    assert second_response.status_code == 409