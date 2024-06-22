import logging
import os

import pika

logger = logging.getLogger()

cred = pika.credentials.PlainCredentials(
    username="listener", password="listener"
)

HOST = os.getenv("RMQ_HOST", "localhost")
QUEUE = os.getenv("QUEUE", "tasks")
EXCHANGE = os.getenv("EXCHANGE", "")
ROUTING_KEY = os.getenv("ROUTING_KEY", "tasks")

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host=HOST, port=5672, credentials=cred)
)
channel = connection.channel()

channel.queue_declare(queue=QUEUE, durable=True)


def parse_message(msg: str):
    table_uuid_pos = msg.find(" tb-")
    task_uuid_pos = msg.find(" ta-")
    table_uuid = msg[table_uuid_pos : table_uuid_pos + 39]  # noqa: E203
    task_uuid = msg[task_uuid_pos : task_uuid_pos + 39]  # noqa: E203
    return table_uuid, task_uuid


def callback(ch, method, properties, body: bytes):
    msg = str(body)
    logger.info(msg)
    table_uuid, task_uuid = parse_message(msg)
    ch.basic_ack(delivery_tag=method.delivery_tag)
    logger.info("Consumed", table_uuid, task_uuid)


channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue=QUEUE, on_message_callback=callback)

channel.start_consuming()


class RabbitWorker:
    def __init__(self):
        pass
