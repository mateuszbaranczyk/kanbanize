from conftest import create_new_task
from pytest import raises

from kanbanize.data_structures.schemas import TASK_PREFIX, TaskResponse
from kanbanize.tasks.crud import create_task, get_task


def test_create_task(mock_db, task):
    result = create_task(mock_db, task)
    assert isinstance(result, TaskResponse)
    assert result.uuid.startswith(TASK_PREFIX)


def test_get_task(mock_db, task):
    new_task = create_new_task(mock_db, task)
    result = get_task(mock_db, new_task.uuid)

    assert isinstance(result, TaskResponse)
    assert result.uuid == new_task.uuid


def test_get_task_name_error(mock_db):
    uuid = "ta-test"
    with raises(NameError, match=f"No such document! {uuid}"):
        get_task(mock_db, uuid)
