import pika


class RmqSender:
    host: str
    queue: str
    exchange: str
    routing_key: str
    user: str
    password: str

    def __init__(self) -> None:
        connection = self.create_connection()
        self.channel = connection.channel()
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

    def create_connection(self) -> pika.BlockingConnection:
        cred = pika.credentials.PlainCredentials(
            username=self.user, password=self.password
        )
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host=self.host, port=self.port, credentials=cred
            )
        )
        return connection
