import os
from abc import ABC, abstractmethod

import pika

from kanbanize.data_structures import Task


class RmqSender:
    host = os.getenv("RMQ_HOST", "localhost")
    queue = os.getenv("QUEUE", "tasks")
    exchange = os.getenv("EXCHANGE", "")
    routing_key = os.getenv("ROUTING_KEY", "tasks")

    def __init__(self) -> None:
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=self.host)
        )
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=self.queue)

    def send_message(self, body: str, close_connection: bool = True) -> None:
        self.channel.basic_publish(
            exchange=self.exchange,
            routing_key=self.routing_key,
            body=body,
            properties=pika.BasicProperties(
                delivery_mode=pika.DeliveryMode.Persistent
            ),
        )
        if close_connection:
            self.connection.close()


class TaskEvent(RmqSender, ABC):
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
