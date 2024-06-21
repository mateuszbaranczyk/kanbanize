import os

import pika

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


def callback(ch, method, properties, body: bytes):
    print(f" [x] Received {body}")
    msg = str(body)
    table_uuid_pos = msg.find(" tb-")
    task_uuid_pos = msg.find(" ta-")
    table_uuid = msg[table_uuid_pos : table_uuid_pos + 39]  # noqa: E203
    task_uuid = msg[task_uuid_pos : task_uuid_pos + 39]  # noqa: E203
    ch.basic_ack(delivery_tag=method.delivery_tag)
    print("Consumed", table_uuid, task_uuid)


channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue=QUEUE, on_message_callback=callback)

channel.start_consuming()
