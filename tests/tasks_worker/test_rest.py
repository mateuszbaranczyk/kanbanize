from fastapi.testclient import TestClient

from kanbanize.data_structures.schemas import TASK_PREFIX, TaskResponse
from kanbanize.tasks.rest import app

client = TestClient(app)


def test_create_task(task):
    task_dump = task.model_dump_json()
    response = client.post("/task/create", json=task_dump)
    task = TaskResponse(**response.json())

    assert response.status_code == 200
    assert task.title == task.title
    assert task.status == task.status
    assert task.notes == task.notes
    assert task.table_uuid == ""
    assert task.uuid.startswith(TASK_PREFIX)
