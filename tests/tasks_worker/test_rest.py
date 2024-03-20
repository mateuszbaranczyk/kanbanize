from unittest.mock import patch

from fastapi.testclient import TestClient

from kanbanize.data_structures.schemas import TASK_PREFIX, TaskResponse
from kanbanize.tasks.rest import app

client = TestClient(app)


@patch("kanbanize.tasks.rest.get_db")
def test_create_task(db, task):
    db.return_value = None
    task_dump = task.model_dump_json()
    response = client.post("/task/create/", data=task_dump)
    task_response = TaskResponse(**response.json())

    assert response.status_code == 200
    assert task_response.name == task.name
    assert task_response.status == task.status
    assert task_response.notes == task.notes
    assert task_response.table_uuid == ""
    assert task_response.uuid.startswith(TASK_PREFIX)
