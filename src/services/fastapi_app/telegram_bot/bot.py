import os

from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message

from .handlers.predict_router import router as predict_router

bot = Bot(token=os.getenv("TELEGRAM_BOT_TOKEN"))
dp = Dispatcher()
dp.include_router(predict_router)


@dp.message(Command("start"))
async def cmd_start(message: Message):
    """
    Start message
    """
    await message.answer(
        "Привет! Данный бот позволяет улучшить качество изображения с помощью AI: "
        "повысить разрешение изображения, убрать смазы или шумы на изображении. \n\n"
        "Доступные команды: \n"
        "/enhance или Улучшить - улучшение изображения \n"
        "/cancel или Отмена - выйти из процесса улучшения"
    )
