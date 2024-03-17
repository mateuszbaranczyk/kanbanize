from fastapi.testclient import TestClient

from kanbanize.data_structures.schemas import TaskResponse
from kanbanize.tasks.rest import app

client = TestClient(app)


def test_create_task():
    notes = "Test User"
    status = "To Do"
    title = "Test Task"
    response = client.post(
        "/task/create",
        json={
            "title": title,
            "status": status,
            "notes": notes,
        },
    )
    assert response.status_code == 200
    task = TaskResponse(**response.json())
    assert task.title == title
    assert task.status == status
    assert task.notes == notes
    assert task.table_uuid == ""
