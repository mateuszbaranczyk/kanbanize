from fastapi.testclient import TestClient
from mockfirestore import MockFirestore
from pytest import fixture

from kanbanize.data_structures.schemas import Task, TaskResponse
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


@fixture
def mock_db():
    db = MockFirestore()
    yield db
    db.reset()


def create_new_task(mock_db, task) -> TaskResponse:
    new_task = TaskResponse(**task.model_dump())
    mock_db.collection("tasks").document(new_task.uuid).set(
        new_task.model_dump()
    )
    return new_task
