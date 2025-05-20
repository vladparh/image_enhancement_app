import logging
import os
import pickle

import pika
import redis
from pika import BasicProperties, PlainCredentials

from src.models.image_enhance import Enhancer


def callback(ch, method, properties: BasicProperties, body):
    """Function for image processing"""
    image_data = pickle.loads(body)
    try:
        result = Enhancer(model_name=properties.headers["model"]).enhance(image_data)
        redis_client.set(properties.headers["inference_id"], pickle.dumps(result))
    except Exception:
        redis_client.set(properties.headers["inference_id"], "error")

    ch.basic_ack(delivery_tag=method.delivery_tag)


logging.basicConfig(level=logging.INFO)

# define rabbitmq and redis client
connection = pika.BlockingConnection(
    pika.ConnectionParameters(
        heartbeat=0,
        host="rabbit",
        port=5672,
        credentials=PlainCredentials(
            os.getenv("RABBITMQ_DEFAULT_USER"), os.getenv("RABBITMQ_DEFAULT_PASS")
        ),
    )
)
rabbitmq_client = connection.channel()
rabbitmq_client.queue_declare(queue="inference_queue")

redis_client = redis.Redis(host="redis", port=6379)

# start rabbitmq
rabbitmq_client.basic_qos(prefetch_count=1)
rabbitmq_client.basic_consume(queue="inference_queue", on_message_callback=callback)

rabbitmq_client.start_consuming()
