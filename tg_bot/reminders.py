import asyncio
from database import fetch_query
from telethon import TelegramClient


async def check_reminders(telethon_client: TelegramClient):
    while True:
        try:
            query = """
                SELECT users.telegram_id, notes.text, notes.reminder_time
                FROM notes
                JOIN users ON notes.user_id = users.id
                WHERE notes.reminder_time <= NOW() + INTERVAL '10 minutes'
                AND notes.reminder_time > NOW()
            """
            reminders = fetch_query(query)

            if reminders:
                for reminder in reminders:
                    telegram_id, text, reminder_time = reminder
                    await telethon_client.send_message(telegram_id, f"Напоминание: {text} в {reminder_time}")

            await asyncio.sleep(60)
        except Exception as e:
            print(f"Ошибка при проверке напоминаний: {e}")
            await asyncio.sleep(60)
