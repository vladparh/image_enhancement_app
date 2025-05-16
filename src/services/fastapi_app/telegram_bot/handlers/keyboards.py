from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def enhance_kb() -> ReplyKeyboardMarkup:
    """
    Клавиатура для выбора типа улучшения
    """
    kb = ReplyKeyboardBuilder()
    kb.button(text="Повысить разрешение")
    kb.button(text="Убрать смазы")
    kb.button(text="Убрать шумы")
    kb.adjust(1)
    return kb.as_markup(resize_keyboard=True)


def upscale_kb() -> ReplyKeyboardMarkup:
    """
    Клавиатура для выбора стапени увеличения разрешения
    """
    kb = ReplyKeyboardBuilder()
    kb.button(text="x2")
    kb.button(text="x4")
    kb.adjust(2)
    return kb.as_markup(resize_keyboard=True)


def yes_no_kb() -> ReplyKeyboardMarkup:
    """
    Да/Нет клавиатура
    """
    kb = ReplyKeyboardBuilder()
    kb.button(text="Да")
    kb.button(text="Нет")
    kb.adjust(2)
    return kb.as_markup(resize_keyboard=True)
