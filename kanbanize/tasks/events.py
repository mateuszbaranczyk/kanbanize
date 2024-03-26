import os
from abc import ABC, abstractmethod

from kanbanize.rabbit_sender import RmqSender
from kanbanize.schemas import TABLE_PREFIX, Task


class TaskEvent(RmqSender, ABC):
    host = os.getenv("RMQ_HOST", "localhost")
    queue = os.getenv("QUEUE", "tasks")
    exchange = os.getenv("EXCHANGE", "")
    routing_key = os.getenv("ROUTING_KEY", "tasks")

    def __init__(self, task: Task) -> None:
        super().__init__()
        self.task = task

    def send(self) -> None:
        body = self.create_body_message(self.task)
        self.send_message(body)

    @abstractmethod
    def create_body_message(self, task: Task) -> str:
        raise NotImplementedError


class TaskConnectedEvent(TaskEvent):
    def __init__(self, task: Task) -> None:
        super().__init__(task)

    def create_body_message(self, task: Task) -> str:
        return f"::TASK connected to TABLE:: {task.uuid} -> {task.table_uuid}"


class TaskDisconnectedEvent(TaskEvent):
    def __init__(self, task: Task) -> None:
        super().__init__(task)

    def create_body_message(self, task: Task) -> str:
        return (
            f"::TASK disconnected from TABLE:: {task.uuid} "
            f"from {task.table_uuid}"
        )


def handle_events(data: dict, task: Task) -> None:
    table_uuid = data.get("table_uuid", "No table uuid")
    if table_uuid.startswith(TABLE_PREFIX):
        TaskConnectedEvent(task).send()
    elif table_uuid == "":
        TaskDisconnectedEvent(task).send()
    return None
