import time

import pika

HOST = ""
QUEUE = ""

connection = pika.BlockingConnection(pika.ConnectionParameters(host=HOST))
channel = connection.channel()

channel.queue_declare(queue=QUEUE, durable=True)


def callback(ch, method, properties, body):
    time.sleep(body.count(b"."))
    ch.basic_ack(delivery_tag=method.delivery_tag)


channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue=QUEUE, on_message_callback=callback)

channel.start_consuming()
