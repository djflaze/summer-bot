import asyncio
import random
from datetime import date
from db import get_users, get_meta, set_meta
from phrases import PHRASES

def days_to_summer():
    today = date.today()
    summer = date(today.year, 6, 1)
    if today > summer:
        summer = date(today.year + 1, 6, 1)
    return (summer - today).days

async def daily_sender(bot):
    while True:
        today = str(date.today())
        last = get_meta("last_send")

        if last != today:
            for user in get_users():
                try:
                    await bot.send_message(
                        user,
                        f"🌴 До лета осталось: {days_to_summer()} дней\n\n{random.choice(PHRASES)}"
                    )
                except:
                    pass
            set_meta("last_send", today)

        await asyncio.sleep(600)