from fastapi.testclient import TestClient

from kanbanize.main_api.rest import task

client = TestClient(task)


def test_create_task():
    response = client.post(
        "/create", json={"name": "test task", "status": "todo"}
    )
    assert response.status_code == 200
    assert response.json()["name"] == "test task"
    assert response.json()["status"] == "todo"


def test_get_task():
    response = client.get("/get/1")
    assert response.status_code == 200


def test_edit_task():
    response = client.put(
        "/edit/1", json={"name": "edited task", "status": "done"}
    )
    assert response.status_code == 200
    assert response.json()["name"] == "edited task"
    assert response.json()["status"] == "done"
