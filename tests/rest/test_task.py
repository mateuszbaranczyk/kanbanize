from unittest.mock import patch

from fastapi.testclient import TestClient

from kanbanize.main_api.run import rest
from kanbanize.schemas import TaskResponse

client = TestClient(rest)


@patch("kanbanize.main_api.adapters.TaskAdapter.create")
def test_create_task(request):
    task, expected = _prepare_adapter_data(request)
    response = client.post("/task/create", json=expected)
    assert response.status_code == 200
    assert response.json()["name"] == task.name


@patch("kanbanize.main_api.adapters.TaskAdapter.get")
def test_get_task(request):
    task, _ = _prepare_adapter_data(request)
    response = client.get(f"/task/get/{task.uuid}")
    assert response.status_code == 200
    assert response.json()["name"] == task.name


@patch("kanbanize.main_api.adapters.TaskAdapter.create")
def test_edit_task(request):
    task = _prepare_adapter_data(request)
    response = client.put(
        f"/task/edit/{task.uuid}",
        json={"name": "edited task", "status": "done"},
    )
    assert response.status_code == 200
    assert response.json()["name"] == "edited task"
    assert response.json()["status"] == "done"


def _prepare_adapter_data(request):
    expected = {"name": "test task", "status": "todo"}
    task = TaskResponse(**expected)
    request.return_value = task
    return task, expected
