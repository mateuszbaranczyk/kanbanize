from conftest import create_new_task

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


def test_get_task(client, mock_db, task):
    task = create_new_task(mock_db, task)
    response = client.get(f"/task/get/{task.uuid}")
    task_response = TaskResponse(**response.json())

    assert response.status_code == 200
    assert task_response.uuid == task.uuid
