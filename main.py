import os
import random
import datetime
from telegram import Bot
from telegram.ext import Updater, CommandHandler

TOKEN = os.getenv("TOKEN")

phrases = [
    "🌞 Лето всё ближе. Терпи, воин.",
    "🔥 Минус ещё один день до жары!",
    "😎 Лето подкрадывается...",
    "🌴 Скоро будем жить на чиле.",
    "🍉 Лето почти на районе.",
    "☀️ Тепло уже в пути!",
    "🏖 Песочек ждёт.",
    "🌊 Море скоро увидимся.",
    "🍹 Готовь очки и вайб.",
    "💛 Ещё чуть-чуть до счастья.",
    "🚀 Лето не за горами!",
    "🌺 Врываемся в летний режим.",
    "😏 Лето уже пакует чемоданы.",
    "🍦 Скоро сезон мороженки.",
    "🎧 Летний плейлист уже готов?",
    "🌅 Закаты станут красивее.",
    "🏝 Вайб будет 100/10.",
    "🌻 Время тепла приближается.",
    "🔥 Солнце заряжается.",
    "😌 Потерпи, скоро июнь."
]

def days_until_summer():
    today = datetime.date.today()
    year = today.year
    summer = datetime.date(year, 6, 1)
    if today > summer:
        summer = datetime.date(year + 1, 6, 1)
    return (summer - today).days

def send_daily_message(context):
    chat_id = os.getenv("CHAT_ID")
    days = days_until_summer()
    phrase = random.choice(phrases)
    text = f"🌴 До лета осталось: {days} дней\n\n{phrase}"
    context.bot.send_message(chat_id=chat_id, text=text)

def start(update, context):
    days = days_until_summer()
    phrase = random.choice(phrases)
    update.message.reply_text(f"🌴 До лета осталось: {days} дней\n\n{phrase}")

def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))

    job_queue = updater.job_queue
    job_queue.run_daily(send_daily_message, time=datetime.time(hour=9, minute=0))

    updater.start_polling()
    updater.idle()

if name == "__main__":
    main()
    
