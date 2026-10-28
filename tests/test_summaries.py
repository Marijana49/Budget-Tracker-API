from decimal import Decimal

def test_month_summary(client):
    category = client.post("/categories", json={"name": "Hrana", "color": "#27AE60"},).json()

    client.post("/transactions", json={
        "type": "income",
        "amount": "100.00",
        "date": "2026-10-05",
        "description": "Plata",
        "category_id": category["id"],
    })

    for amount, description in [
        ("20.00", "Ručak"),
        ("10.00", "Kafa"),
    ]:
        client.post("/transactions", json={
            "type": "expense",
            "amount": amount,
            "date": "2026-10-10",
            "description": description,
            "category_id": category["id"],
        })

    client.post("/budgets", json={
        "month": "2026-10-01",
        "amount": "50.00",
        "category_id": category["id"],
    })

    response = client.get("/summaries?month=2026-10-01")

    assert response.status_code == 200

    data = response.json()

    assert data["month"] == "2026-10-01"
    assert Decimal(data["total_income"]) == Decimal("100.00")
    assert Decimal(data["total_expense"]) == Decimal("30.00")
    assert Decimal(data["balance"]) == Decimal("70.00")

    assert len(data["categories"]) == 1

    food = data["categories"][0]

    assert food["category"] == "Hrana"
    assert Decimal(food["spent"]) == Decimal("30.00")
    assert Decimal(food["budget"]) == Decimal("50.00")
    assert Decimal(food["left"]) == Decimal("20.00")

def test_over_budget_has_negative_left(client):
    category = client.post("/categories", json={"name": "Prevoz", "color": "#3498DB"}).json()
    client.post("/transactions", json={
        "type": "expense", "amount": "80.00", "date": "2026-10-10",
        "description": "Gorivo", "category_id": category["id"],
    })
    client.post("/budgets", json={"month": "2026-10-01", "amount": "50.00", "category_id": category["id"]})

    food = client.get("/summaries?month=2026-10-01").json()["categories"][0]
    assert Decimal(food["left"]) == Decimal("-30.00")


def test_category_without_budget_and_left(client):
    category = client.post("/categories", json={"name": "Zabava", "color": "#9B59B6"}).json()
    client.post("/transactions", json={
        "type": "expense", "amount": "15.00", "date": "2026-10-10",
        "description": "Bioskop", "category_id": category["id"],
    })
    item = client.get("/summaries?month=2026-10-01").json()["categories"][0]
    assert item["budget"] is None
    assert item["left"] is None


def test_empty_month_returns_zeros_and_no_categories(client):
    data = client.get("/summaries?month=2026-02-01").json()
    assert Decimal(data["total_income"]) == 0
    assert Decimal(data["total_expense"]) == 0
    assert Decimal(data["balance"]) == 0
    assert data["categories"] == []