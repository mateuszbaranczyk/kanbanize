from fastapi.testclient import TestClient

from kanbanize.main_api.run import rest

client = TestClient(rest)


def test_create_table():
    response = client.post("/table/create", json={"name": "test table"})
    assert response.status_code == 200
    assert response.json()["name"] == "test table"


def test_get_table():
    response = client.get("/table/get/1")
    assert response.status_code == 200


def test_edit_table():
    response = client.put("/table/edit/1", json={"name": "edited table"})
    assert response.status_code == 200
    assert response.json()["name"] == "edited table"
