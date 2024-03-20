from unittest.mock import MagicMock

from fastapi.testclient import TestClient
from pytest import fixture

from kanbanize.data_structures.schemas import Task
from kanbanize.tasks.database import get_db
from kanbanize.tasks.rest import app


@fixture
def task() -> Task:
    task = Task(name="task_name", status="done", notes="test notes")
    return task


@fixture
def dumped_task(task) -> dict:
    return task.model_dump()


@fixture
def client():
    client = TestClient(app)
    return client


def mocked_db():
    return MagicMock()


@fixture(autouse=True)
def get_db_override():
    app.dependency_overrides[get_db] = mocked_db
