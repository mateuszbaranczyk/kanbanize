from conftest import create_new_task
from pytest import raises

from kanbanize.data_structures.schemas import TASK_PREFIX, TaskResponse
from kanbanize.tasks.crud import create, edit, get


def test_create_task(mock_db, task):
    result = create(mock_db, task)
    assert isinstance(result, TaskResponse)
    assert result.uuid.startswith(TASK_PREFIX)


def test_get_task(mock_db, task):
    new_task = create_new_task(mock_db, task)
    result = get(mock_db, new_task.uuid)

    assert isinstance(result, TaskResponse)
    assert result.uuid == new_task.uuid


def test_get_task_name_error(mock_db):
    uuid = "ta-test"
    with raises(NameError, match=f"No such document! {uuid}"):
        get(mock_db, uuid)


def test_edit_task(mock_db, task):
    task = create_new_task(mock_db, task)
    new_name = "new name"
    data = {"name": new_name}

    result = edit(mock_db, task.uuid, data)

    assert result.name == new_name
    assert result.notes == task.notes
