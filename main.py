import os
import random
import logging
import sqlite3
from datetime import datetime, time
from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)

TOKEN = os.getenv("TOKEN")
ADMIN_ID = None  # можешь позже вставить свой id

DB_NAME = "users.db"

logging.basicConfig(level=logging.INFO)

# ========= ФРАЗЫ =========

phrases = [
"Лето уже крашится в твою жизнь.",
"Солнце такое: «ну приветик».",
"Зима словила делулу.",
"Чилл на вайбе сигма.",
"Лето уже в твоём ДНК.",
"Солнце апает тебе настроение.",
"Зима в тильте.",
"Лето: «я в пути, зай».",
"Терпи, это лор.",
"Чилл грузится через 5G.",
"Солнце уже в твоих реках.",
"Зима получила бан.",
"Лето фармит позитив.",
"Настроение скоро будет slay.",
"Тепло идёт без спроса.",
"Лето врывается как сигма-патруль.",
"Зима кричит «я устала».",
"Солнце делает flex.",
"Чилл выходит из подвала.",
"Лето уже написало «го гулять».",
"Зима поймала cringe-комбо.",
"Лето апает твой skin.",
"Солнце делает soft launch.",
"Чилл на максимальном rizz.",
"Зима потеряла вайб.",
"Лето в статусе «онлайн».",
"Солнце такой: «чё спим?»",
"Зима больше не канон.",
"Лето зашло в чат.",
"Чилл в апдейте 2.0.",
"Солнце уже делает POV.",
"Зима вне сюжета.",
"Лето — главный персонаж арки.",
"Чилл включён по умолчанию.",
"Солнце делает main character moment.",
"Зима удаляется без сохранения.",
"Лето на low start.",
"Чилл активирует ульту.",
"Солнце прожимает кнопку «сиять».",
"Зима больше не meta.",
"Лето в режиме slay era.",
"Чилл качает харизму.",
"Солнце флексит лучами.",
"Зима словила hard reset.",
"Лето на эстетике «вау».",
"Чилл пишет «ты где?».",
"Солнце уже на подлёте, bestie.",
"Зима оффнулась.",
"Лето запускает summer core.",
"Чилл с premium подпиской.",
"Солнце такое: «ну всё, выхожу».",
"Зима больше не сигма.",
"Лето апает твой ментал.",
"Чилл делает comeback.",
"Солнце в статусе «готово сиять».",
"Зима ушла в архив.",
"Лето в режиме «без багов».",
"Чилл словил glow up.",
"Солнце прожимает ультра-вайб.",
"Summer arc almost unlocked."
]

# ========= DB =========

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            chat_id INTEGER PRIMARY KEY,
            joined_at TEXT
        )
    """)
    conn.commit()
    conn.close()

def add_user(chat_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT OR IGNORE INTO users (chat_id, joined_at) VALUES (?, ?)",
        (chat_id, datetime.now().isoformat())
    )
    conn.commit()
    conn.close()

def remove_user(chat_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM users WHERE chat_id=?", (chat_id,))
    conn.commit()
    conn.close()

def get_users():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT chat_id FROM users")
    rows = cursor.fetchall()
    conn.close()
    return [r[0] for r in rows]

# ========= ЛОГИКА =========

def days_until_summer():
    today = datetime.now()
    summer = datetime(today.year, 6, 1)
    if today > summer:
        summer = datetime(today.year + 1, 6, 1)
    return (summer - today).days

def build_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("📊 Статистика", callback_data="stats")],
        [InlineKeyboardButton("🌴 Обновить", callback_data="refresh")]
    ])

# ========= КОМАНДЫ =========

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    add_user(chat_id)

    try:
        await update.message.delete()
    except:
        pass

    days = days_until_summer()
    phrase = random.choice(phrases)

    await context.bot.send_message(
        chat_id=chat_id,
        text=f"<b>🌴 До лета осталось:</b> {days} дней\n\n<i>{phrase}</i>",
        parse_mode="HTML",
        reply_markup=build_keyboard()
    )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "stats":
        count = len(get_users())
        await query.edit_message_text(
            f"👥 <b>Пользователей:</b> {count}",
            parse_mode="HTML",
            reply_markup=build_keyboard()
        )

    elif query.data == "refresh":
        days = days_until_summer()
        phrase = random.choice(phrases)
        await query.edit_message_text(
            f"<b>🌴 До лета осталось:</b> {days} дней\n\n<i>{phrase}</i>",
            parse_mode="HTML",
            reply_markup=build_keyboard()
        )

# ========= РАССЫЛКА =========

async def daily(context: ContextTypes.DEFAULT_TYPE):
    users = get_users()
    days = days_until_summer()
    phrase = random.choice(phrases)

    for chat_id in users:
        try:
            await context.bot.send_message(
                chat_id=chat_id,
                text=f"<b>🌴 До лета осталось:</b> {days} дней\n\n<i>{phrase}</i>",
                parse_mode="HTML",
            )
        except:
            remove_user(chat_id)

# ========= MAIN =========

def main():
    init_db()

    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))

    app.job_queue.run_daily(
        daily,
        time=time(hour=9, minute=0)
    )

    print("ULTRA BOT STARTED")
    app.run_polling()

if __name__ == "__main__":
    main()