import asyncio
import random
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from config import TOKEN, ADMIN_ID
from db import add_user, get_users
from phrases import PHRASES
from scheduler import daily_sender, days_to_summer

bot = Bot(TOKEN)
dp = Dispatcher()

kb_user = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="🌴 До лета")]],
    resize_keyboard=True
)

kb_admin = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🌴 До лета")],
        [KeyboardButton(text="📊 Статистика")]
    ],
    resize_keyboard=True
)

@dp.message(F.text == "/start")
async def start(msg: Message):
    add_user(msg.from_user.id)
    kb = kb_admin if msg.from_user.id == ADMIN_ID else kb_user
    await msg.answer(
        f"🌴 До лета осталось: {days_to_summer()} дней\n\n{random.choice(PHRASES)}",
        reply_markup=kb
    )
    await msg.delete()

@dp.message(F.text == "🌴 До лета")
async def summer(msg: Message):
    await msg.answer(
        f"🌴 До лета осталось: {days_to_summer()} дней\n\n{random.choice(PHRASES)}"
    )

@dp.message(F.text == "📊 Статистика")
async def stats(msg: Message):
    if msg.from_user.id != ADMIN_ID:
        return
    await msg.answer(f"👥 Всего пользователей: {len(get_users())}")

async def main():
    asyncio.create_task(daily_sender(bot))
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())