from mockfirestore import MockFirestore
from pytest import fixture

from kanbanize.data_structures.schemas import TASK_PREFIX, TaskResponse
from kanbanize.tasks.crud import create_task


@fixture
def get_mock_db():
    db = MockFirestore()
    yield db
    db.reset()


def test_create_task(get_mock_db, task):
    result = create_task(get_mock_db, task)
    assert isinstance(result, TaskResponse)
    assert result.uuid.startswith(TASK_PREFIX)
