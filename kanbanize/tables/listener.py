import logging
import os

import pika
from crud import TablesAdapter
from schemas import TableUuid, TaskUuid


class RabbitWorker:
    HOST = os.getenv("RMQ_HOST", "localhost")
    PORT = os.getenv("RMQ_PORT", 5672)
    QUEUE = os.getenv("QUEUE", "tasks")
    EXCHANGE = os.getenv("EXCHANGE", "")
    ROUTING_KEY = os.getenv("ROUTING_KEY", "tasks")
    USERNAME = os.getenv("USERNAME", "listener")
    PASSWORD = os.getenv("PASSWORD", "listener")

    def __init__(self) -> None:
        self.logger = logging.getLogger("RabbitMQ")
        connection = self.prepare_connection()
        channel = connection.channel()
        channel.queue_declare(queue=self.QUEUE, durable=True)
        channel.basic_qos(prefetch_count=1)
        channel.basic_consume(
            queue=self.QUEUE, on_message_callback=self.callback
        )
        channel.start_consuming()
        return None

    def callback(self, ch, method, properties, body: bytes) -> None:
        msg = str(body)
        self.logger.info(msg)
        table_uuid, task_uuid, event = self._parse_message(msg)
        self.handle_event(event)
        ch.basic_ack(delivery_tag=method.delivery_tag)
        self.logger.info("Consumed", table_uuid, task_uuid)
        return None

    def handle_event(
        self, table_uuid: TableUuid, task_uuid: TaskUuid, event: str
    ) -> None:
        adapter = TablesAdapter()
        table = adapter.get(table_uuid)
        match event:
            case "connected":
                data = {"tasks": table.tasks.append(task_uuid)}
                adapter.edit(table_uuid, data)
            case "disconnected":
                data = {"tasks": table.tasks.remove(task_uuid)}
                adapter.edit(table_uuid)
        return None

    def prepare_connection(self) -> None:
        credensials = pika.credentials.PlainCredentials(
            username=self.USERNAME, password=self.PASSWORD
        )
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host=self.HOST, port=self.PORT, credentials=credensials
            )
        )
        return connection

    def _parse_message(self, msg: str) -> tuple[TableUuid, TaskUuid, str]:
        table_uuid_pos = msg.find(" tb-")
        task_uuid_pos = msg.find(" ta-")
        uuid_len = 39
        table_uuid = msg[
            table_uuid_pos : table_uuid_pos + uuid_len  # noqa: E203
        ]
        task_uuid = msg[task_uuid_pos : task_uuid_pos + uuid_len]  # noqa: E203
        event = "connected" if "connected" in msg else "disconnected"
        return table_uuid, task_uuid, event
