from mockfirestore import MockFirestore
from pytest import fixture, raises

from kanbanize.data_structures.schemas import TASK_PREFIX, TaskResponse
from kanbanize.tasks.crud import create_task, get_task


@fixture
def mock_db():
    db = MockFirestore()
    yield db
    db.reset()


def test_create_task(mock_db, task):
    result = create_task(mock_db, task)
    assert isinstance(result, TaskResponse)
    assert result.uuid.startswith(TASK_PREFIX)


def test_get_task(mock_db, task):
    new_task = _create_new_task(mock_db, task)
    result = get_task(mock_db, new_task.uuid)

    assert isinstance(result, TaskResponse)
    assert result.uuid == new_task.uuid


def _create_new_task(mock_db, task) -> TaskResponse:
    new_task = TaskResponse(**task.model_dump())
    mock_db.collection("tasks").document(new_task.uuid).set(
        new_task.model_dump()
    )
    return new_task


def test_get_task_name_error(mock_db):
    uuid = "ta-test"
    with raises(NameError, match=f"No such document! {uuid}"):
        get_task(mock_db, uuid)
