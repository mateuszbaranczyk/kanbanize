from unittest.mock import patch

from kanbanize.data_structures.schemas import TASK_PREFIX, TaskResponse


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


@patch("kanbanize.tasks.crud.get_task")
def test_get_task(mock_crud, client, task):
    db_task = TaskResponse(**task.model_dump())
    mock_crud.return_value = db_task

    response = client.get(f"/task/get/{db_task.uuid}")
    task_response = TaskResponse(**response.json())
    assert response.status_code == 200
    assert task_response.uuid == db_task.uuid


@patch("kanbanize.tasks.crud.get_task")
def test_get_task_returns_404(
    mock_crud,
    client,
):
    mock_crud.side_effect = NameError()

    response = client.get("/task/get/uuid")
    assert response.status_code == 404
