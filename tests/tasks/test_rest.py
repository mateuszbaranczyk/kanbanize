from unittest.mock import patch

import pytest
from conftest import create_new_task

from kanbanize.schemas import TASK_PREFIX, TaskResponse


def test_create_task(client, task):
    task_dump = task.model_dump_json()
    response = client.post("/task/create/", data=task_dump)
    task_response = TaskResponse(**response.json())

    assert response.status_code == 200
    assert task_response.name == task.name
    assert task_response.status == task.status
    assert task_response.notes == task.notes
    assert task_response.table_uuid == ""
    assert task_response.uuid.startswith(TASK_PREFIX)


@pytest.fixture
def creation_event():
    with patch("kanbanize.tasks.rest.TaskConnectedEvent") as connected_event:
        yield connected_event


def test_create_task_with_connected_table(client, task, creation_event):
    task.table_uuid = "tb-test"
    task_dump = task.model_dump_json()

    response = client.post("/task/create/", data=task_dump)

    creation_event.assert_called_once()
    assert response.status_code == 200


def test_get_task(mock_db, client, task):
    new_task = create_new_task(mock_db, task)

    response = client.get(f"/task/get/{new_task.uuid}")
    task_response = TaskResponse(**response.json())

    assert response.status_code == 200
    assert task_response.uuid == new_task.uuid


def test_get_task_returns_404(client):
    response = client.get("/task/get/uuid")
    assert response.status_code == 404


def test_edit_task(mock_db, client, task):
    new_task = create_new_task(mock_db, task)
    new_name = "test name 2"
    data = {"name": new_name}

    result = client.put(f"/task/edit/{new_task.uuid}", json=data)
    task_response = TaskResponse(**result.json())

    assert result.status_code == 200
    assert task_response.name == new_name


@pytest.mark.parametrize(
    "error_code, json", [(404, {}), (422, {"test": "test"})]
)
def test_edit_task_error_codes(client, error_code, json):
    result = client.put("/task/edit/uuid", json=json)

    assert result.status_code == error_code


@pytest.mark.parametrize(
    "table_uuid, task_event",
    [
        ("tb-test", "task_connected"),
        ("", "task_disconnected"),
    ],
)
def test_edit_with_events(
    mock_db, client, task, table_uuid, task_event, request
):
    new_task = create_new_task(mock_db, task)
    data = {"table_uuid": table_uuid}

    result = client.put(f"/task/edit/{new_task.uuid}", json=data)
    task_response = TaskResponse(**result.json())

    assert result.status_code == 200
    assert task_response.table_uuid == table_uuid

    event_mock = request.getfixturevalue(task_event)
    event_mock.assert_called_once()
