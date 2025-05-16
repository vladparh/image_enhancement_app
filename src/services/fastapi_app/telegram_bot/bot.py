from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message

from .config_reader import settings
from .handlers.predict_router import router as predict_router

bot = Bot(token=settings.BOT_TOKEN.get_secret_value())
dp = Dispatcher()
dp.include_router(predict_router)


@dp.message(Command("start"))
async def cmd_start(message: Message):
    """
    Start message
    """
    await message.answer("Привет! Чтобы узнать доступные команды, введи /help")


@dp.message(Command("help"))
async def help_info(message: Message):
    """
    Help
    """
    await message.answer(
        "/enhance или Улучшить- улучшение изображения \n"
        "/cancel или Отмена - выйти из процесса улучшения"
    )
