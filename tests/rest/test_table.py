from fastapi.testclient import TestClient

from kanbanize.main_api.rest import table

client_table = TestClient(table)


def test_create_table():
    response = client_table.post("/create", json={"name": "test table"})
    assert response.status_code == 200
    assert response.json()["name"] == "test table"


def test_get_table():
    response = client_table.get("/get/1")
    assert response.status_code == 200


def test_edit_table():
    response = client_table.put("/edit/1", json={"name": "edited table"})
    assert response.status_code == 200
    assert response.json()["name"] == "edited table"
