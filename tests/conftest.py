from mockfirestore import MockFirestore
from pytest import fixture


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
def mock_db():
    db = FakeFirestore.get_instance()
    return db


@fixture(autouse=True)
def setup_teardown(mock_db):
    try:
        mock_db
    finally:
        mock_db.reset()
