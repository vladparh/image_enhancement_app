import io
import logging

from fastapi import APIRouter, HTTPException, UploadFile
from fastapi.responses import Response
from PIL import Image

from src.models.image_enhance import Enhancer

router = APIRouter(prefix="/enhance", tags=["enhance image"])


@router.post("/upscale")
async def upscale(scale: int = 2, image: UploadFile = None) -> Response:
    """
    Image upscaling

    :param scale: scale for upscaling
    :param image: image for upscaling
    :return: upscaled image
    """
    try:
        content = image.file.read()
        buffer = io.BytesIO(content)
        img = Image.open(buffer)
    except Exception:
        logging.error("Files read error", exc_info=True)
        raise HTTPException(status_code=400, detail="Something wrong with file")

    if scale == 2:
        enhancer = Enhancer(model_name="real_esrgan_x2", tile_size=1000)
        logging.info("Upscale x2")
    elif scale == 4:
        enhancer = Enhancer(model_name="real_esrgan_x4", tile_size=500)
        logging.info("Upscale x4")
    else:
        raise HTTPException(status_code=400, detail="Invalid scale")

    try:
        img = enhancer.enhance(img)
    except Exception:
        logging.error("Image upscale error", exc_info=True)
        raise HTTPException(status_code=500, detail="Something wrong while processing")

    img_bytes = io.BytesIO()
    img.save(img_bytes, format="png")
    img_bytes = img_bytes.getvalue()
    return Response(content=img_bytes, media_type="image/png")


@router.post("/deblur")
async def deblur(image: UploadFile = None) -> Response:
    """
    Image deblurring

    :param image: image for deblurring
    :return: deblured image
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
        enhancer = Enhancer(model_name="mlwnet", tile_size=1000)
        img = enhancer.enhance(img)
    except Exception:
        logging.error("Image deblur error", exc_info=True)
        raise HTTPException(status_code=500, detail="Something wrong while processing")

    img_bytes = io.BytesIO()
    img.save(img_bytes, format="png")
    img_bytes = img_bytes.getvalue()
    return Response(content=img_bytes, media_type="image/png")


@router.post("/denoise")
async def denoise(image: UploadFile = None) -> Response:
    """
    Image denoising

    :param image: image for denoising
    :return: denoised image
    """
    try:
        content = image.file.read()
        buffer = io.BytesIO(content)
        img = Image.open(buffer)
    except Exception:
        logging.error("Files read error", exc_info=True)
        raise HTTPException(status_code=400, detail="Something wrong with file")

    try:
        logging.info("Denoise image")
        enhancer = Enhancer(model_name="nafnet_sidd", tile_size=1000)
        img = enhancer.enhance(img)
    except Exception:
        logging.error("Image denoise error", exc_info=True)
        raise HTTPException(status_code=500, detail="Something wrong while processing")

    img_bytes = io.BytesIO()
    img.save(img_bytes, format="png")
    img_bytes = img_bytes.getvalue()
    return Response(content=img_bytes, media_type="image/png")
