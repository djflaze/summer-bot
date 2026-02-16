import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from config import TOKEN, ADMIN_ID
from db import add_user, get_users
from scheduler import daily_sender, days_to_summer
from phrases import PHRASES
import random

bot = Bot(TOKEN)
dp = Dispatcher()

kb_user = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="🌴 До лета")]],
    resize_keyboard=True
)

kb_admin = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📊 Статистика")],
        [KeyboardButton(text="🔄 Обновить")]
    ],
    resize_keyboard=True
)

@dp.message(F.text == "/start")
async def start(msg: Message):
    add_user(msg.from_user.id)
    await msg.answer(
        f"🌴 До лета осталось: {days_to_summer()} дней\n{random.choice(PHRASES)}",
        reply_markup=kb_user
    )
    await msg.delete()

@dp.message(F.text == "🌴 До лета")
async def summer(msg: Message):
    await msg.answer(
        f"🌴 До лета осталось: {days_to_summer()} дней\n{random.choice(PHRASES)}"
    )

@dp.message(F.text == "📊 Статистика")
async def stats(msg: Message):
    if msg.from_user.id != ADMIN_ID:
        return
    await msg.answer(f"👥 Пользователей: {len(get_users())}")

@dp.message(F.text == "🔄 Обновить")
async def refresh(msg: Message):
    if msg.from_user.id != ADMIN_ID:
        return
    await msg.answer("Обновлено. Лето всё ближе 😈")

async def main():
    asyncio.create_task(daily_sender(bot))
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())