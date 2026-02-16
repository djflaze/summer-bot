from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from config import ADMIN_ID

def get_main_keyboard(user_id: int):
    buttons = [
        [KeyboardButton(text="До лета")]
    ]

    if user_id == ADMIN_ID:
        buttons.append([KeyboardButton(text="Статистика")])
        buttons.append([KeyboardButton(text="Обновить")])

    return ReplyKeyboardMarkup(
        keyboard=buttons,
        resize_keyboard=True
    )