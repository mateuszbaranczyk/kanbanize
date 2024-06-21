import pika

cred = pika.credentials.PlainCredentials(
    username="listener", password="listener"
)  # TODO


class RmqSender:
    host: str
    queue: str
    exchange: str
    routing_key: str

    def __init__(self) -> None:
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host="raspberry", port=5672, credentials=cred
            )
        )
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=self.queue, durable=True)

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
