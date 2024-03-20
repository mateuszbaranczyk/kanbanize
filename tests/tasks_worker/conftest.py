from fastapi.testclient import TestClient
from mockfirestore import MockFirestore
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
def client() -> TestClient:
    client = TestClient(app)
    return client


# @fixture
def mocked_db() -> MockFirestore:
    mock_db = MockFirestore()
    try:
        yield mock_db
    finally:
        mock_db.reset()


@fixture(autouse=True)
def override_get_db() -> None:
    app.dependency_overrides[get_db] = mocked_db
    return None
