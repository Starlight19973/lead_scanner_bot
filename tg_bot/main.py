import asyncio
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from config import TELEGRAM_TOKEN, TELETHON_API_ID, TELETHON_API_HASH, TELETHON_SESSION_STRING
from telethon import TelegramClient
from telethon.sessions import StringSession
from handlers import setup_handlers
from reminders import check_reminders


bot = Bot(token=TELEGRAM_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)
telethon_client = TelegramClient(StringSession(TELETHON_SESSION_STRING), TELETHON_API_ID, TELETHON_API_HASH)

setup_handlers(dp)


async def main():
    await telethon_client.start()
    asyncio.create_task(check_reminders(telethon_client))
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
