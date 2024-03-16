from fastapi.testclient import TestClient

from kanbanize.main_api.run import app

client = TestClient(app)


def test_create_task():
    response = client.post(
        "/task/create", json={"name": "test task", "status": "todo"}
    )
    assert response.status_code == 200
    assert response.json()["name"] == "test task"
    assert response.json()["status"] == "todo"


def test_get_task():
    response = client.get("/task/get/1")
    assert response.status_code == 200


def test_edit_task():
    response = client.put(
        "/task/edit/1", json={"name": "edited task", "status": "done"}
    )
    assert response.status_code == 200
    assert response.json()["name"] == "edited task"
    assert response.json()["status"] == "done"
