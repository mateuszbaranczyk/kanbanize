from unittest.mock import patch

import pytest

from kanbanize.schemas import TaskResponse
from kanbanize.tasks.events import TaskConnectedEvent, TaskDisconnectedEvent

disconnected_message = "::TASK disconnected from TABLE:: ta-test from tb-test"
connected_message = "::TASK connected to TABLE:: ta-test -> tb-test"


@pytest.mark.parametrize(
    "event_class, expected_result",
    [
        (TaskConnectedEvent, connected_message),
        (TaskDisconnectedEvent, disconnected_message),
    ],
)
@patch("kanbanize.tasks.events.RmqSender.__init__")
def test_task_event_messages__(_, event_class, expected_result, task):
    task.table_uuid = "tb-test"
    task_response = TaskResponse(**task.model_dump())
    task_response.uuid = "ta-test"
    event = event_class(task_response)
    result = event.create_body_message()

    assert result == expected_result
