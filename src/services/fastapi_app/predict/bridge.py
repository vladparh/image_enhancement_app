import pika
import redis
from pika import PlainCredentials

connection = pika.BlockingConnection(
    pika.ConnectionParameters(
        heartbeat=0,
        host="rabbit",
        port=5672,
        credentials=PlainCredentials("my_user", "my_password"),
    )
)
rabbitmq_client = connection.channel()
rabbitmq_client.queue_declare(queue="inference_queue")

redis_client = redis.Redis(host="redis", port=6379)
