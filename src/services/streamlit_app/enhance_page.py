import io
import logging
import os
from time import sleep

import requests
import streamlit as st
from PIL import Image
from streamlit_image_comparison import image_comparison

site = "http://fastapp:8000"


@st.cache_data(show_spinner=False, max_entries=10)
def upscale(img, scale_value):
    response = requests.request(
        "POST",
        f"{site}/enhance/upscale",
        files={"image": img.getvalue()},
        params={"scale": scale_value},
    )
    if response.status_code != 200:
        return response.status_code, ""
    inference_id = response.json()["inference_id"]
    while True:
        response = requests.request(
            "GET", f"{site}/enhance/result", params={"inference_id": inference_id}
        )
        if response.status_code == 200 or response.status_code == 500:
            break
        sleep(int(os.getenv("POLLING_INTERVAL", "1")))
    return response.status_code, response.content


@st.cache_data(show_spinner=False, max_entries=10)
def deblur(img):
    response = requests.request(
        "POST", f"{site}/enhance/deblur", files={"image": img.getvalue()}
    )
    if response.status_code != 200:
        return response.status_code, ""
    inference_id = response.json()["inference_id"]
    while True:
        response = requests.request(
            "GET", f"{site}/enhance/result", params={"inference_id": inference_id}
        )
        if response.status_code == 200 or response.status_code == 500:
            break
        sleep(int(os.getenv("POLLING_INTERVAL", "1")))
    return response.status_code, response.content


@st.cache_data(show_spinner=False, max_entries=10)
def denoise(img):
    response = requests.request(
        "POST", f"{site}/enhance/denoise", files={"image": img.getvalue()}
    )
    if response.status_code != 200:
        return response.status_code, ""
    inference_id = response.json()["inference_id"]
    while True:
        response = requests.request(
            "GET", f"{site}/enhance/result", params={"inference_id": inference_id}
        )
        if response.status_code == 200 or response.status_code == 500:
            break
        sleep(int(os.getenv("POLLING_INTERVAL", "1")))
    return response.status_code, response.content


if "disabled" not in st.session_state:
    st.session_state.disabled = False


def callback(value):
    st.session_state.disabled = value


st.title("Обработка изображений")
c = st.container(border=True)
enhance_type = c.pills(
    "Выберите тип улучшения",
    options=["Повышение разрешения", "Удаление смазов", "Удаление шумов"],
    selection_mode="single",
    disabled=st.session_state.disabled,
)

if enhance_type == "Повышение разрешения":
    scale = c.segmented_control(
        label="Выберите степень повышения разрешения",
        options=["x2", "x4"],
        default="x2",
        selection_mode="single",
        disabled=st.session_state.disabled,
    )

input_img_bytes = c.file_uploader(
    "Загрузите изображение",
    type=["jpg", "jpeg", "png"],
    accept_multiple_files=False,
    disabled=st.session_state.disabled,
)

start_button = c.button(
    "Обработать изображение",
    disabled=st.session_state.disabled,
    on_click=callback,
    args=(True,),
)

if start_button and input_img_bytes is not None:
    with st.spinner("В процессе..."):
        if enhance_type == "Повышение разрешения":
            if scale == "x2":
                logging.info("Upscaling x2")
                status_code, output_img_bytes = upscale(input_img_bytes, 2)
            elif scale == "x4":
                logging.info("Upscaling x4")
                status_code, output_img_bytes = upscale(input_img_bytes, 4)
        elif enhance_type == "Удаление смазов":
            logging.info("Deblurring")
            status_code, output_img_bytes = deblur(input_img_bytes)
        elif enhance_type == "Удаление шумов":
            logging.info("Denoise")
            status_code, output_img_bytes = denoise(input_img_bytes)

        if status_code == 200:
            input_img = Image.open(input_img_bytes)
            output_img_bytes = io.BytesIO(output_img_bytes)
            output_img = Image.open(output_img_bytes)
            image_comparison(
                img1=input_img, img2=output_img, label1="До", label2="После"
            )
            st.button("Попробовать ещё", on_click=callback, args=(False,))
            st.download_button(
                "Скачать обработанное изображение",
                data=output_img_bytes,
                mime="image/png",
                on_click=callback,
                args=(False,),
            )
        else:
            st.error("Упс! Что-то пошло не так")
            st.button("Попробовать ещё", on_click=callback, args=(False,))
            logging.error("Image processing error", exc_info=True)
