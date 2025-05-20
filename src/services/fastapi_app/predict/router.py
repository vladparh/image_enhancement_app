import asyncio
import io
import logging
import os
import pickle
import uuid

import pika
import redis
from fastapi import APIRouter, HTTPException, UploadFile
from fastapi.responses import Response
from pika import BasicProperties, PlainCredentials
from PIL import Image

router = APIRouter(prefix="/enhance", tags=["enhance image"])

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


@router.post("/upscale")
async def upscale(scale: int = 2, image: UploadFile = None):
    """
    Image upscaling

    Args:
        scale: scale for upscaling
        image: image for upscaling

    Returns:
        status code 200 and inference_id - if all is ok
        status code 400 - if something wrong with file or invalid scale
        status code 500 - if something wrong while sending task
    """
    try:
        content = image.file.read()
        buffer = io.BytesIO(content)
        img = Image.open(buffer)
    except Exception:
        logging.error("Files read error", exc_info=True)
        raise HTTPException(status_code=400, detail="Something wrong with file")

    if scale == 2:
        logging.info("Upscale x2")
        model_name = "real_esrgan_x2"
    elif scale == 4:
        logging.info("Upscale x4")
        model_name = "real_esrgan_x4"
    else:
        raise HTTPException(status_code=400, detail="Invalid scale")

    try:
        inference_id = str(uuid.uuid4())

        rabbitmq_client.basic_publish(
            exchange="",  # default exchange
            routing_key="inference_queue",
            body=pickle.dumps(img),
            properties=BasicProperties(
                headers={"inference_id": inference_id, "model": model_name}
            ),
        )
    except Exception:
        logging.error("Image upscale error", exc_info=True)
        raise HTTPException(status_code=500, detail="Something wrong send task")

    return {"inference_id": inference_id}


@router.post("/deblur")
async def deblur(image: UploadFile = None):
    """
    Image deblurring

    Args:
        image: image for debluring

    Returns:
        status code 200 and inference_id - if all is ok
        status code 400 - if something wrong with file
        status code 500 - if something wrong while sending task
    """
    try:
        content = image.file.read()
        buffer = io.BytesIO(content)
        img = Image.open(buffer)
    except Exception:
        logging.error("Files read error", exc_info=True)
        raise HTTPException(status_code=400, detail="Something wrong with file")

    try:
        logging.info("Deblur image")
        inference_id = str(uuid.uuid4())

        rabbitmq_client.basic_publish(
            exchange="",  # default exchange
            routing_key="inference_queue",
            body=pickle.dumps(img),
            properties=BasicProperties(
                headers={"inference_id": inference_id, "model": "mlwnet"}
            ),
        )
    except Exception:
        logging.error("Image deblur error", exc_info=True)
        raise HTTPException(status_code=500, detail="Something wrong send task")

    return {"inference_id": inference_id}


@router.post("/denoise")
async def denoise(image: UploadFile = None):
    """
    Image denoising

    Args:
        image: image for denoising

    Returns:
        status code 200 and inference_id - if all is ok
        status code 400 - if something wrong with file
        status code 500 - if something wrong while sending task
    """
    try:
        img = Image.open(image.file)
    except Exception:
        logging.error("Files read error", exc_info=True)
        raise HTTPException(status_code=400, detail="Something wrong with file")

    try:
        logging.info("Denoise image")
        inference_id = str(uuid.uuid4())

        rabbitmq_client.basic_publish(
            exchange="",  # default exchange
            routing_key="inference_queue",
            body=pickle.dumps(img),
            properties=BasicProperties(
                headers={"inference_id": inference_id, "model": "scunet"}
            ),
        )
    except Exception:
        logging.error("Image denoise error", exc_info=True)
        raise HTTPException(status_code=500, detail="Something wrong while send task")

    return {"inference_id": inference_id}


@router.get("/result")
async def classification_result(inference_id) -> Response:
    """
    Get result

    Args:
        inference_id: id for get result

    Returns:
        status code 200 and image - if image processed
        status code 502 - if inference_id not found yet
        status code 500 - if error while processing image was occurred
    """
    for _ in range(int(os.getenv("API_TIMEOUT"))):
        if redis_client.exists(inference_id):
            result = redis_client.get(inference_id)
            redis_client.delete(inference_id)
            if result == b"error":
                raise HTTPException(
                    status_code=500, detail="Something wrong while image processing"
                )
            img = pickle.loads(result)
            img_bytes = io.BytesIO()
            img.save(img_bytes, format="png")
            img_bytes = img_bytes.getvalue()
            return Response(content=img_bytes, media_type="image/png")
        await asyncio.sleep(1)
    if not redis_client.exists(inference_id):
        raise HTTPException(status_code=502, detail="inference_id not found")
