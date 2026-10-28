def test_create_category(client):
    response = client.post("/categories", json={"name": "Hrana", "color": "#27AE60"})
    assert response.status_code == 201
    assert response.json()["name"] == "Hrana"
    assert response.json()["color"] == "#27AE60"

def test_category_name_cannot_be_empty(client):
    response = client.post("/categories",json={"name": "   ", "color": "#27AE60"})
    assert response.status_code == 422


def test_duplicate_name(client):
    client.post("/categories", json={"name": "Hrana", "color": "#27AE60"})
    response = client.post("/categories", json={"name": "hrana", "color": "#27AE60"})
    assert response.status_code == 409


def test_long_name(client):
    response = client.post("/categories", json={"name": "Ovo je dugacak naziv za kategoriju za potrebe testiranja pravila", "color": "#27AE60"})
    assert response.status_code == 422


def test_categories_sorted_by_name(client):
    for name in ["Prevoz", "bioskop", "Kupovina"]:
        client.post("/categories", json={"name": name, "color": "#000000"})
    
    names = [c["name"] for c in client.get("/categories").json()]
    assert names == ["bioskop", "Kupovina", "Prevoz"]


def test_category_invalid_color(client):
    response = client.post("/categories", json={"name": "Hrana", "color": "red"})
    assert response.status_code == 422


def test_category_with_transaction_cant_delete(client):
    category = client.post("/categories", json={"name": "Hrana", "color": "#2ECC71"}).json()
    client.post("/transactions", json={
        "type": "expense", "amount": 10, "date": "2026-10-01",
        "description": "Kafa", "category_id": category["id"],
    })
    response = client.delete(f"/categories/{category['id']}")
    assert response.status_code == 409


def test_delete_category(client):
    category = client.post("/categories",json={"name": "Prevoz", "color": "#000000"}).json()

    response = client.delete(f"/categories/{category['id']}")
    assert response.status_code == 204

def test_category_name_strips_whitespace(client):
    response = client.post("/categories", json={"name": "  Hrana  ", "color": "#27AE60"},)
    assert response.status_code == 201
    assert response.json()["name"] == "Hrana"

def test_delete_category_also_deletes_its_budgets(client):
    c = client.post("/categories", json={"name": "Zabava", "color": "#9B59B6"}).json()
    client.post("/budgets", json={"month": "2026-10-01", "amount": "50.00", "category_id": c["id"]})

    assert client.delete(f"/categories/{c['id']}").status_code == 204
    assert client.get("/budgets?month=2026-10-01").json() == []