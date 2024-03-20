from unittest.mock import patch

from kanbanize.data_structures.schemas import TASK_PREFIX, TaskResponse
from kanbanize.tasks.crud import create_task


@patch("kanbanize.tasks.database.get_db")
def test_create_task(db, task):
    result = create_task(db, task)
    assert isinstance(result, TaskResponse)
    assert result.uuid.startswith(TASK_PREFIX)
