def _make_category(client, name="Hrana"):
    return client.post("/categories", json={"name": name, "color": "#27AE60"}).json()


def _upload(client, content: str):
    return client.post(
        "/transactions/import",
        files={"file": ("transactions.csv", content.encode("utf-8"), "text/csv")},
    )


HEADER = "type,amount,date,description,category\n"


def test_import_valid_rows(client):
    _make_category(client, "Hrana")
    _make_category(client, "Plata")
    content = HEADER + (
        "expense,12.50,2026-10-08,Lunch,Hrana\n"
        "income,300.00,2026-10-09,,Plata\n"
    )

    response = _upload(client, content)

    assert response.status_code == 200
    assert response.json() == {"imported": 2, "failed": []}
    assert client.get("/transactions").json()["total"] == 2


def test_import_category_ignores_case(client):
    _make_category(client, "Hrana")
    response = _upload(client, HEADER + "expense,5.00,2026-10-08,Kafa,HRANA\n")

    assert response.json()["imported"] == 1


def test_import_empty_description_becomes_null(client):
    _make_category(client, "Plata")
    _upload(client, HEADER + "income,300.00,2026-10-09,,Plata\n")

    item = client.get("/transactions").json()["items"][0]
    assert item["description"] is None


def test_import_reports_failed_rows_with_reason(client):
    _make_category(client, "Hrana")
    content = HEADER + (
        "expense,10.00,2026-10-08,Ok,Hrana\n"            
        "expense,abc,2026-10-09,Los iznos,Hrana\n"      
        "expense,10.00,2026-13-45,Los datum,Hrana\n"     
        "expense,10.00,2026-10-10,Nema,Nepostojeca\n"  
        "profit,10.00,2026-10-11,Los tip,Hrana\n"        
    )

    data = _upload(client, content).json()

    assert data["imported"] == 1
    failed = {item["row"]: item["reason"] for item in data["failed"]}
    assert sorted(failed) == [3, 4, 5, 6]
    assert failed[3].startswith("amount")
    assert failed[4].startswith("date")
    assert failed[5].startswith("category")
    assert failed[6].startswith("type")


def test_import_rejects_amount_rules(client):
    _make_category(client, "Hrana")
    content = HEADER + (
        "expense,0,2026-10-08,Nula,Hrana\n"
        "expense,-5,2026-10-08,Negativan,Hrana\n"
        "expense,10.123,2026-10-08,Tri decimale,Hrana\n"
        "expense,1000000.01,2026-10-08,Previse,Hrana\n"
        "expense,1000000.00,2026-10-08,Granica,Hrana\n"
    )

    data = _upload(client, content).json()

    assert data["imported"] == 1
    assert len(data["failed"]) == 4


def test_import_trims_spaces_and_uppercase_type(client):
    _make_category(client, "Prevoz")
    content = HEADER + "EXPENSE,  20.00  ,  2026-10-14  ,  Taksi  ,  Prevoz  \n"

    data = _upload(client, content).json()

    assert data["imported"] == 1
    assert client.get("/transactions").json()["items"][0]["description"] == "Taksi"


def test_import_missing_columns_returns_422(client):
    response = _upload(client, "type,amount\nexpense,10\n")

    assert response.status_code == 422
    assert "Missing columns" in response.json()["detail"]


def test_import_invalid_encoding_returns_422(client):
    response = client.post(
        "/transactions/import",
        files={"file": ("bad.csv", b"\xff\xfe\x00\x01\x02", "text/csv")},
    )

    assert response.status_code == 422


def test_import_failed_rows_are_not_saved(client):
    _make_category(client, "Hrana")
    _upload(client, HEADER + "expense,abc,2026-10-08,Los,Hrana\n")

    assert client.get("/transactions").json()["total"] == 0