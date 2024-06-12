from unittest.mock import patch

from fastapi.testclient import TestClient
from pytest import fixture

from kanbanize.schemas import Task, TaskResponse
from kanbanize.tasks.database import get_db
from kanbanize.tasks.rest import app


@fixture(autouse=True)
def override_get_db(mock_db) -> None:
    app.dependency_overrides[get_db] = mock_db
    return None


@fixture
def task() -> Task:
    task = Task(name="task_name", status="done", notes="test notes")
    return task


@fixture
def dumped_task(task) -> dict:
    return task.model_dump()


@fixture
def client() -> TestClient:
    client = TestClient(app)
    return client


def create_new_task(mock_db, task) -> TaskResponse:
    new_task = TaskResponse(**task.model_dump())
    mock_db.collection("tasks").document(new_task.uuid).set(
        new_task.model_dump()
    )
    return new_task


@fixture(autouse=True)
def task_connected():
    with patch("kanbanize.tasks.events.TaskConnectedEvent") as connected_event:
        yield connected_event


@fixture(autouse=True)
def task_disconnected():
    with patch(
        "kanbanize.tasks.events.TaskDisconnectedEvent"
    ) as disconnected_event:
        yield disconnected_event
