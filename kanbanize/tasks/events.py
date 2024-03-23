import os

import pika
from pika.adapters.blocking_connection import BlockingChannel

from kanbanize.data_structures import Task

HOST = os.getenv("RMQ_HOST", "localhost")
QUEUE = "tasks"
EXCHANGE = ""


def create_chanel() -> BlockingChannel:
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=HOST))
    channel = connection.channel()
    channel.queue_declare(queue=QUEUE)


def create_body_message(task: Task) -> str:
    return f"::TASK connected to TABLE:: {task.uuid} -> {task.table_uuid}"


def send_message(task: Task, table_uuid: str | None) -> None:
    if table_uuid:
        channel = create_chanel()
        body = create_body_message(task)
        channel.basic_publish(
            exchange=EXCHANGE, routing_key="hello", body=body
        )
