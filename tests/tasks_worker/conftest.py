from fastapi.testclient import TestClient
from mockfirestore import MockFirestore
from pytest import fixture

from kanbanize.data_structures.schemas import Task, TaskResponse
from kanbanize.tasks.database import get_db
from kanbanize.tasks.rest import app


class FakeFirestore(MockFirestore):
    _instance = None

    @staticmethod
    def get_instance():
        if FakeFirestore._instance is None:
            FakeFirestore()
        return FakeFirestore._instance

    def __init__(self):
        if FakeFirestore._instance is not None:
            raise Exception(
                "Instance already created. Use get_instance method."
            )
        else:
            super().__init__()
            FakeFirestore._instance = self


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


@fixture(autouse=True)
def override_get_db() -> None:
    app.dependency_overrides[get_db] = FakeFirestore.get_instance
    return None


@fixture
def mock_db():
    db = FakeFirestore.get_instance()
    return db


@fixture(autouse=True)
def setup_teardown(mock_db):
    try:
        mock_db
    finally:
        mock_db.reset()


def create_new_task(mock_db, task) -> TaskResponse:
    new_task = TaskResponse(**task.model_dump())
    mock_db.collection("tasks").document(new_task.uuid).set(
        new_task.model_dump()
    )
    return new_task
