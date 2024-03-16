from fastapi.testclient import TestClient

from kanbanize.main_api.run import rest

client = TestClient(rest)


def test_create_group():
    response = client.post(
        "/group/create", json={"name": "test group", "project": "test project"}
    )
    assert response.status_code == 200
    assert response.json()["name"] == "test group"
    assert response.json()["project"] == "test project"


def test_get_group():
    response = client.get("/group/get/1")
    assert response.status_code == 200


def test_edit_group():
    response = client.put(
        "/group/edit/1",
        json={"name": "edited group", "project": "edited project"},
    )
    assert response.status_code == 200
    assert response.json()["name"] == "edited group"
    assert response.json()["project"] == "edited project"
