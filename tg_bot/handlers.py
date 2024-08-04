import psycopg2
import re
from aiogram import Router, types
from aiogram.fsm.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.filters import CommandStart, Command, StateFilter
from config import DATABASE


router = Router()


class Registration(StatesGroup):
    name = State()
    email = State()


class NoteAdding(StatesGroup):
    text = State()
    reminder_time = State()


def setup_handlers(dp):
    dp.include_router(router)


@router.message(CommandStart())
async def start(message: types.Message, state: FSMContext):
    try:
        conn = psycopg2.connect(**DATABASE)
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE telegram_id = %s", (message.from_user.id,))
        user = cur.fetchone()
        conn.close()

        if user:
            await message.reply("Вы уже зарегистрированы!")
        else:
            await message.reply("Привет! Пожалуйста, введите ваше имя.")
            await state.set_state(Registration.name)
            current_state = await state.get_state()
            print(f"Текущее состояние после установки name: {current_state}")
    except Exception as e:
        print(f"Ошибка подключения к базе данных: {e}")


@router.message(StateFilter(Registration.name))
async def process_name(message: types.Message, state: FSMContext):
    try:
        await state.update_data(name=message.text)
        await message.reply("Спасибо! Теперь введите ваш email.")
        await state.set_state(Registration.email)
        current_state = await state.get_state()
        print(f"Текущее состояние после установки email: {current_state}")
    except Exception as e:
        print(f"Ошибка при обработке имени: {e}")


def is_valid_email(email):
    pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(pattern, email)


@router.message(StateFilter(Registration.email))
async def process_email(message: types.Message, state: FSMContext):
    try:
        email = message.text
        if not is_valid_email(email):
            await message.reply("Неверный формат email. Пожалуйста, введите корректный email.")
            return

        user_data = await state.get_data()
        name = user_data['name']
        telegram_id = message.from_user.id
        print("Данные для записи в БД:", name, email, telegram_id)

        # Сохранение пользователя в базе данных
        conn = psycopg2.connect(**DATABASE)
        cur = conn.cursor()
        cur.execute("INSERT INTO users (name, email, telegram_id) VALUES (%s, %s, %s)",
                    (name, email, telegram_id))
        conn.commit()
        conn.close()

        await message.reply("Вы успешно зарегистрированы!")
        await state.clear()
        print("Пользователь зарегистрирован и данные сохранены в БД")
    except Exception as e:
        print(f"Ошибка при обработке email: {e}")


@router.message(Command(commands=['addnote']))
async def add_note_start(message: types.Message, state: FSMContext):
    await message.reply("Пожалуйста, введите текст заметки.")
    await state.set_state(NoteAdding.text)


@router.message(StateFilter(NoteAdding.text))
async def process_note_text(message: types.Message, state: FSMContext):
    await state.update_data(note_text=message.text)
    await message.reply("Спасибо! Теперь введите время напоминания (в формате ГГГГ-ММ-ДД ЧЧ:ММ).")
    await state.set_state(NoteAdding.reminder_time)


@router.message(StateFilter(NoteAdding.reminder_time))
async def process_note_time(message: types.Message, state: FSMContext):
    try:
        user_data = await state.get_data()
        note_text = user_data['note_text']
        reminder_time = message.text
        telegram_id = message.from_user.id

        # Получение user_id из базы данных
        conn = psycopg2.connect(**DATABASE)
        cur = conn.cursor()
        cur.execute("SELECT id FROM users WHERE telegram_id = %s", (telegram_id,))
        user = cur.fetchone()
        user_id = user[0]

        # Сохранение заметки в базе данных
        cur.execute("INSERT INTO notes (user_id, text, reminder_time) VALUES (%s, %s, %s)",
                    (user_id, note_text, reminder_time))
        conn.commit()
        conn.close()

        await message.reply("Заметка успешно добавлена!")
        await state.clear()
    except Exception as e:
        print(f"Ошибка при обработке заметки: {e}")


@router.message(Command(commands=['mynotes']))
async def my_notes(message: types.Message):
    try:
        telegram_id = message.from_user.id
        # Получение заметок пользователя из базы данных
        conn = psycopg2.connect(**DATABASE)
        cur = conn.cursor()
        cur.execute("""
            SELECT text, reminder_time FROM notes
            JOIN users ON notes.user_id = users.id
            WHERE users.telegram_id = %s
            ORDER BY reminder_time ASC
        """, (telegram_id,))
        notes = cur.fetchall()
        conn.close()

        if notes:
            response = "Ваши заметки:\n"
            for note in notes:
                response += f"{note[1]}: {note[0]}\n"
        else:
            response = "У вас нет заметок."

        await message.reply(response)
    except Exception as e:
        print(f"Ошибка при получении заметок: {e}")



