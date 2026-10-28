from decimal import Decimal

def test_create_transaction(client):
    category = client.post("/categories",json={"name": "Hrana", "color": "#27AE60"}).json()

    response = client.post("/transactions", json={"type": "expense", "amount": 2.50, "date": "2026-08-16", "description": "Kafa", "category_id": category["id"]})
    print(response.json())
    assert response.status_code == 201
    assert response.json()["type"] == "expense"
    assert Decimal(response.json()["amount"]) == Decimal(2.50)
    assert response.json()["date"] == "2026-08-16"
    assert response.json()["description"] == "Kafa"
    assert response.json()["category_id"] == category["id"]


def test_create_transaction_with_negative_amount(client):
    category = client.post("/categories", json={"name": "Hrana", "color": "#27AE60"}).json()

    response = client.post("/transactions",json={
            "type": "expense",
            "amount": -10,
            "date": "2026-08-16",
            "description": "Kafa",
            "category_id": category["id"],
        }
    )

    assert response.status_code == 422


def test_create_transaction_with_invalid_category(client):
    response = client.post( "/transactions", json={
            "type": "expense",
            "amount": 10,
            "date": "2026-08-16",
            "description": "Kafa",
            "category_id": 999999,
        }
    )

    assert response.status_code == 404


def test_transaction_invalid_type(client):
    category = client.post("/categories", json={"name": "Hrana", "color": "#27AE60"}).json()

    response = client.post("/transactions",json={
            "type": "something_invalid",
            "amount": 10,
            "date": "2026-08-16",
            "description": "Kafa",
            "category_id": category["id"],
        }
    )

    assert response.status_code == 422


def test_update_transaction(client):
    category = client.post("/categories", json={"name": "Hrana", "color": "#27AE60"}).json()

    transaction = client.post("/transactions", json={"type": "expense", "amount": 2.50, "date": "2026-08-16", "description": "Kafa", "category_id": category["id"],}).json()

    response = client.patch(f"/transactions/{transaction['id']}", json={"amount": 5.00, "description": "Ručak",})

    assert response.status_code == 200

    data = response.json()

    assert Decimal(data["amount"]) == Decimal("5.00")
    assert data["description"] == "Ručak"
    assert data["type"] == "expense"
    assert data["date"] == "2026-08-16"
    assert data["category_id"] == category["id"]


def test_list_transactions(client):
    category = client.post("/categories", json={"name": "Hrana", "color": "#27AE60"}).json()

    client.post("/transactions", json={"type": "expense", "amount": 2.50, "date": "2026-08-16", "description": "Kafa", "category_id": category["id"],})

    response = client.get("/transactions")

    assert response.status_code == 200
    assert len(response.json()["items"]) == 1
    assert response.json()["total"] == 1


def test_transaction_maximum_amount(client):
    category = client.post("/categories", json={"name": "Hrana", "color": "#27AE60"}).json()

    response = client.post("/transactions", json={
            "type": "expense",
            "amount": "1000000.00",
            "date": "2026-08-16",
            "description": "Test",
            "category_id": category["id"],
        }
    )

    assert response.status_code == 201


def test_transaction_above_maximum_amount(client):
    category = client.post("/categories", json={"name": "Hrana", "color": "#27AE60"}).json()

    response = client.post("/transactions", json={
            "type": "expense",
            "amount": "1000000.01",
            "date": "2026-08-16",
            "description": "Test",
            "category_id": category["id"],
        }
    )

    assert response.status_code == 422


def test_transaction_zero_amount(client):
    category = client.post("/categories", json={"name": "Hrana", "color": "#27AE60"},).json()

    response = client.post("/transactions", json={
            "type": "expense",
            "amount": 0,
            "date": "2026-08-16",
            "description": "Kafa",
            "category_id": category["id"],
        },
    )

    assert response.status_code == 422