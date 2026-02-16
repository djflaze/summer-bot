import random
from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from keyboards import get_main_keyboard
from config import ADMIN_ID

router = Router()

phrases = [
    "Лето уже крашится в твою жизнь.",
    "Солнце такое: «ну приветик».",
    "Зима словила делулу.",
    "Чилл на вайбе сигма.",
    "Лето уже в твоём ДНК."
]

@router.message(CommandStart())
async def start(message: Message):
    await message.answer(
        "Ну что, запускаем лето?",
        reply_markup=get_main_keyboard(message.from_user.id)
    )

@router.message(lambda message: message.text == "До лета")
async def send_phrase(message: Message):
    await message.answer(random.choice(phrases))

@router.message(lambda message: message.text == "Статистика")
async def stats(message: Message):
    if message.from_user.id != ADMIN_ID:
        return
    await message.answer("Статистика пока в разработке.")

@router.message(lambda message: message.text == "Обновить")
async def update(message: Message):
    if message.from_user.id != ADMIN_ID:
        return
    await message.answer("Бот обновлён 🔥")