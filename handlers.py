import random
from datetime import datetime
from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from keyboards import get_main_keyboard
from config import ADMIN_ID

router = Router()

# ========= ВСЕ ТВОИ ФРАЗЫ =========

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

# ========= ФУНКЦИЯ ПОДСЧЁТА ДНЕЙ =========

def days_until_summer():
    today = datetime.now()
    summer = datetime(today.year, 6, 1)

    if today > summer:
        summer = datetime(today.year + 1, 6, 1)

    return (summer - today).days

# ========= START =========

@router.message(CommandStart())
async def start(message: Message):
    days = days_until_summer()

    await message.answer(
        f"🌴 До лета осталось: {days} дней\n\n{random.choice(phrases)}",
        reply_markup=get_main_keyboard(message.from_user.id)
    )

# ========= КНОПКА "До лета" =========

@router.message(lambda message: message.text == "До лета")
async def send_phrase(message: Message):
    days = days_until_summer()
    phrase = random.choice(phrases)

    await message.answer(
        f"🌴 До лета осталось: {days} дней\n\n{phrase}"
    )

# ========= СТАТИСТИКА (ТОЛЬКО АДМИН) =========

@router.message(lambda message: message.text == "Статистика")
async def stats(message: Message):
    if message.from_user.id != ADMIN_ID:
        return

    await message.answer("📊 Статистика пока в разработке.")

# ========= ОБНОВИТЬ (ТОЛЬКО АДМИН) =========

@router.message(lambda message: message.text == "Обновить")
async def update(message: Message):
    if message.from_user.id != ADMIN_ID:
        return

    await message.answer("🔄 Бот обновлён.")