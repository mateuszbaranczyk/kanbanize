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


@patch("kanbanize.main_api.adapters.TaskAdapter.edit")
def test_edit_task(request):
    task, expected = _prepare_adapter_data(
        request, {"name": "edited task", "status": "done"}
    )
    response = client.put(
        f"/task/edit/{task.uuid}",
        json=expected,
    )
    assert response.status_code == 200
    assert response.json()["name"] == expected["name"]
    assert response.json()["status"] == expected["status"]


def _prepare_adapter_data(
    request, expected={"name": "test task", "status": "todo"}
):
    expected = expected
    task = TaskResponse(**expected)
    request.return_value = task
    return task, expected
