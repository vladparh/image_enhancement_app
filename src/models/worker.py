import logging
import pickle

from pika import BasicProperties

from src.models.image_enhance import Enhancer
from src.services.fastapi_app.predict.bridge import rabbitmq_client, redis_client


def callback(ch, method, properties: BasicProperties, body):
    image_data = pickle.loads(body)
    try:
        result = Enhancer(model_name=properties.headers["model"]).enhance(image_data)
        redis_client.set(properties.headers["inference_id"], pickle.dumps(result))
    except Exception:
        redis_client.set(properties.headers["inference_id"], "error")

    ch.basic_ack(delivery_tag=method.delivery_tag)


logging.basicConfig(level=logging.INFO)
rabbitmq_client.basic_qos(prefetch_count=1)
rabbitmq_client.basic_consume(queue="inference_queue", on_message_callback=callback)

rabbitmq_client.start_consuming()
