# python -m src.services.fastapi.main
import logging
from contextlib import asynccontextmanager

import uvicorn
from aiogram.types import Update
from fastapi import FastAPI, Request

from src.services.bot.bot import bot, dp
from src.services.bot.config_reader import settings
from src.services.fastapi.predict.router import router as predict_router

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Код, выполняющийся при запуске приложения
    webhook_url = settings.get_webhook_url()  # Получаем URL вебхука
    await bot.set_webhook(
        url=settings.get_webhook_url(),
        allowed_updates=dp.resolve_used_update_types(),
        drop_pending_updates=True,
    )
    logging.info(f"Webhook set to {webhook_url}")
    yield  # Приложение работает
    # Код, выполняющийся при завершении работы приложения
    await bot.delete_webhook()
    logging.info("Webhook removed")


app = FastAPI(title="Image enhancement", lifespan=lifespan)


app.include_router(predict_router)


@app.post("/webhook")
async def webhook(request: Request) -> None:
    logging.info("Received webhook request")
    update = Update.model_validate(await request.json(), context={"bot": bot})
    # Обрабатываем обновление через диспетчер (dp) и передаем в бот
    await dp.feed_update(bot, update)
    logging.info("Update processed")


if __name__ == "__main__":
    uvicorn.run(app="src.services.fastapi.main:app", reload=True, port=8000)
