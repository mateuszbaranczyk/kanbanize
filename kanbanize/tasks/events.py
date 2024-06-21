import os
from abc import ABC, abstractmethod

from rabbit_sender import RmqSender

from kanbanize.schemas import TABLE_PREFIX, TaskResponse


class TaskEvent(RmqSender, ABC):
    host = os.getenv("RMQ_HOST", "listener:listener@raspberry:5672")  # TODO
    queue = os.getenv("QUEUE", "tasks")
    exchange = os.getenv("EXCHANGE", "")
    routing_key = os.getenv("ROUTING_KEY", "tasks")

    def __init__(self, task: TaskResponse) -> None:
        super().__init__()
        self.task = task

    def send(self) -> None:
        body = self.create_body_message()
        self.send_message(body)

    @abstractmethod
    def create_body_message(self) -> str:
        raise NotImplementedError


class TaskConnectedEvent(TaskEvent):
    def __init__(self, task: TaskResponse) -> None:
        super().__init__(task)

    def create_body_message(self) -> str:
        return (
            f"::TASK connected to TABLE:: "
            f"{self.task.uuid} -> {self.task.table_uuid}"
        )


class TaskDisconnectedEvent(TaskEvent):
    def __init__(self, task: TaskResponse) -> None:
        super().__init__(task)

    def create_body_message(self) -> str:
        return (
            f"::TASK disconnected from TABLE:: {self.task.uuid} "
            f"from {self.task.table_uuid}"
        )


def handle_events(data: dict, task: TaskResponse) -> None:
    table_uuid = data.get("table_uuid", "No table uuid")
    if table_uuid.startswith(TABLE_PREFIX):
        TaskConnectedEvent(task).send()
    elif table_uuid == "":
        TaskDisconnectedEvent(task).send()
    return None
