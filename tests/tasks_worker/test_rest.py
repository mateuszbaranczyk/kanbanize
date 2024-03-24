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


def test_nonexisted_edit_task(client):
    result = client.put("/task/edit/uuid", json={})

    assert result.status_code == 404


def test_send_edit_task_with_invalid_data(client):
    result = client.put("/task/edit/uuid", json={"test": "test"})

    assert result.status_code == 422
