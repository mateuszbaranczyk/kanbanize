from pytest import fixture, raises

from kanbanize.schemas import TASK_PREFIX, TaskResponse
from kanbanize.tasks.crud import TasksAdapter


@fixture
def task_adapter(mock_db):
    return TasksAdapter(mock_db)


def test_create_task(task_adapter, task):
    result = task_adapter.create(task)
    assert isinstance(result, TaskResponse)
    assert result.uuid.startswith(TASK_PREFIX)


def test_get_task(task_adapter, task):
    new_task = task_adapter.create(task)
    result = task_adapter.get(new_task.uuid)
    assert isinstance(result, TaskResponse)
    assert result.uuid == new_task.uuid


def test_get_task_name_error(task_adapter):
    uuid = "ta-test"
    with raises(NameError, match=f"No such document! {uuid}"):
        task_adapter.get(uuid)


def test_edit_task(task_adapter, task):
    task = task_adapter.create(task)
    new_name = "new name"
    data = {"name": new_name}

    result = task_adapter.edit(task.uuid, data)
    assert result.name == new_name
    assert result.notes == task.notes
