# Telegram Bot

Этот проект представляет собой Telegram-бота, который позволяет пользователям регистрироваться, добавлять заметки и получать уведомления о предстоящих событиях.

## Установка и настройка

### 1. Установка окружения

1. **Создайте виртуальное окружение (рекомендуется):**
   ```bash
   python -m venv venv

Активируйте виртуальное окружение:

На Windows:
bash
Копировать код
venv\Scripts\activate
На macOS и Linux:
bash
Копировать код
source venv/bin/activate
Установите необходимые зависимости:

bash
Копировать код
pip install -r requirements.txt
2. Настройка бота
Получение токена Telegram Bot API:

Создайте нового бота в Telegram, обратившись к BotFather.
Следуйте инструкциям, чтобы создать бота и получить токен API.
Получение API ID и API Hash для Telethon:

Перейдите на my.telegram.org и войдите в свою учетную запись Telegram.
Перейдите в раздел "API Development Tools" и создайте новое приложение.
Получите API_ID и API_HASH.
Создание сессии для Telethon:

Создайте файл generate_session.py с следующим содержимым:
python
Копировать код
from telethon.sync import TelegramClient
from telethon.sessions import StringSession

api_id = 'YOUR_API_ID'
api_hash = 'YOUR_API_HASH'

with TelegramClient(StringSession(), api_id, api_hash) as client:
    print(client.session.save())
Замените YOUR_API_ID и YOUR_API_HASH на ваши значения.
Запустите скрипт:
bash
Копировать код
python generate_session.py
Сохраните строку сессии (TELETHON_SESSION_STRING), которую вы получите.
Создание и настройка файла .env:

Создайте файл .env в корневом каталоге проекта и добавьте следующие строки, заменяя значения на ваши:
makefile
Копировать код
TELEGRAM_TOKEN=your_telegram_bot_token
TELETHON_API_ID=your_telethon_api_id
TELETHON_API_HASH=your_telethon_api_hash
TELETHON_SESSION_STRING=your_telethon_session_string
DATABASE_NAME=your_db_name
DATABASE_USER=your_db_user
DATABASE_PASSWORD=your_db_password
DATABASE_HOST=your_db_host
DATABASE_PORT=your_db_port
Создание файла config.py:

Создайте файл config.py в корневом каталоге проекта и добавьте следующие строки:
python
Копировать код
from dotenv import load_dotenv
import os

load_dotenv()

DATABASE = {
    'dbname': os.getenv('DATABASE_NAME'),
    'user': os.getenv('DATABASE_USER'),
    'password': os.getenv('DATABASE_PASSWORD'),
    'host': os.getenv('DATABASE_HOST'),
    'port': os.getenv('DATABASE_PORT'),
}

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
TELETHON_API_ID = os.getenv('TELETHON_API_ID')
TELETHON_API_HASH = os.getenv('TELETHON_API_HASH')
TELETHON_SESSION_STRING = os.getenv('TELETHON_SESSION_STRING')
3. Запуск бота
Запустите бота:
bash
Копировать код
python main.py
Тестирование
Для тестирования основных функций бота используйте pytest.

Установите необходимые зависимости (если еще не установлены):

bash
Копировать код
pip install pytest
Запустите тесты:

bash
Копировать код
pytest tests
Структура проекта
main.py: Главный файл для запуска бота и настройки основных функций.
handlers.py: Обработчики команд и состояний.
database.py: Функции для работы с базой данных.
reminders.py: Функции для проверки и отправки напоминаний.
keyboards.py: Функции для создания клавиатур.
config.py: Настройки и конфигурации.
tests/test_bot.py: Тесты для проверки основных функций бота.
Лицензия
Этот проект лицензирован под лицензией MIT.

makefile
Копировать код

### Дополнительные файлы

**requirements.txt:**
```plaintext
aiogram
asyncpg
telethon
psycopg2-binary
python-dotenv
pytest
generate_session.py:

python
Копировать код
from telethon.sync import TelegramClient
from telethon.sessions import StringSession

api_id = 'YOUR_API_ID'
api_hash = 'YOUR_API_HASH'

with TelegramClient(StringSession(), api_id, api_hash) as client:
    print(client.session.save())
Этот README.md файл предоставляет все необходимые инструкции для установки, настройки и запуска вашего бота, а также для выполнения тестов. Не забудьте заменить все YOUR_* значения на реальные данные.
