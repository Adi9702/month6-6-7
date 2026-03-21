import asyncio
from aiogram import Bot, Dispatcher
import os
from dotenv import load_dotenv
from app.bottg import router

load_dotenv()

TOKEN = os.environ.get("TOKEN")

async def main():
    bot = Bot(token=TOKEN)
    dp = Dispatcher()
    dp.include_router(router)

    await dp.start_polling(bot)

asyncio.run(main())