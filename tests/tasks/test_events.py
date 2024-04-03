from unittest.mock import patch

from kanbanize.schemas import TaskResponse
from kanbanize.tasks.events import TaskConnectedEvent


@patch("kanbanize.tasks.events.RmqSender.__init__")
def test_task_event_messages(mock, task):
    task.table_uuid = "tb-test"
    task_response = TaskResponse(**task.model_dump())
    expected_result = (
        f"::TASK connected to TABLE:: "
        f"{task_response.uuid} -> {task_response.table_uuid}"
    )
    event = TaskConnectedEvent(task_response)
    result = event.create_body_message()

    assert result == expected_result
