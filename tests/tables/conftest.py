from fastapi.testclient import TestClient
from mockfirestore import MockFirestore
from pytest import fixture

from kanbanize.schemas import Table
from kanbanize.tables.crud import TablesAdapter
from kanbanize.tables.database import get_db
from kanbanize.tables.rest import app


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
def client() -> TestClient:
    client = TestClient(app)
    return client


@fixture
def mock_db():
    db = FakeFirestore.get_instance()
    return db


@fixture(autouse=True)
def override_get_db() -> None:
    app.dependency_overrides[get_db] = FakeFirestore.get_instance
    return None


@fixture(autouse=True)
def setup_teardown(mock_db):
    try:
        mock_db
    finally:
        mock_db.reset()


@fixture
def table():
    table = Table(name="test_table", tasks=[])
    return table


@fixture
def table_adapter(mock_db):
    adapter = TablesAdapter(mock_db)
    return adapter
