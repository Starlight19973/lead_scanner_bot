import pytest
from aiogram import Bot, Dispatcher, types
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Message, Update
from unittest.mock import AsyncMock
from config import TELEGRAM_TOKEN
from handlers import setup_handlers


@pytest.fixture
def bot():
    return Bot(token=TELEGRAM_TOKEN)


@pytest.fixture
def dispatcher(bot):
    storage = MemoryStorage()
    dp = Dispatcher(bot, storage=storage)
    setup_handlers(dp)
    return dp


@pytest.fixture
def message():
    return AsyncMock(spec=Message)


@pytest.mark.asyncio
async def test_start_command(dispatcher, message):
    message.text = '/start'
    message.from_user.id = 12345
    message.reply = AsyncMock()

    update = Update(update_id=1, message=message)
    await dispatcher.feed_update(bot=dispatcher.bot, update=update)

    message.reply.assert_called_once_with("Привет! Пожалуйста, введите ваше имя.")


@pytest.mark.asyncio
async def test_addnote_command(dispatcher, message):
    message.text = '/addnote'
    message.from_user.id = 12345
    message.reply = AsyncMock()

    update = Update(update_id=1, message=message)
    await dispatcher.feed_update(bot=dispatcher.bot, update=update)

    message.reply.assert_called_once_with("Пожалуйста, введите текст заметки.")


@pytest.mark.asyncio
async def test_mynotes_command(dispatcher, message):
    message.text = '/mynotes'
    message.from_user.id = 12345
    message.reply = AsyncMock()

    update = Update(update_id=1, message=message)
    await dispatcher.feed_update(bot=dispatcher.bot, update=update)

    message.reply.assert_called_once_with("У вас нет заметок.")
