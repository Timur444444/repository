import asyncio
import sqlite3
from datetime import datetime, date, timedelta
from zoneinfo import ZoneInfo

from aiogram import Bot, Dispatcher, types
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

# --------- Настройки ----------
BOT_TOKEN = "8341181963:AAGWvI0bU2BwCQXl1NgBBKH4XsKnNQfYB84"
TZ = ZoneInfo("Europe/Chisinau")  

DB_PATH = "habits.db"

class AddHabitStates(StatesGroup):
    waiting_for_name = State()
    waiting_for_times = State()

# Инициализация бота и диспетчера
bot = Bot(token=BOT_TOKEN, parse_mode="HTML")
dp = Dispatcher(storage=MemoryStorage())

# Создание/подключение к БД
def init_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS habits (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            name TEXT NOT NULL,
            times_per_day INTEGER NOT NULL
        )
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS habit_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            habit_id INTEGER NOT NULL,
            date TEXT NOT NULL,
            times_done INTEGER NOT NULL,
            UNIQUE(user_id, habit_id, date)
        )
    """)
    conn.commit()
    conn.close()

def get_today_str():
    return datetime.now(TZ).date().isoformat()

# DB helpers
def add_habit_to_db(user_id: int, name: str, times_per_day: int):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("INSERT INTO habits (user_id, name, times_per_day) VALUES (?, ?, ?)",
                (user_id, name, times_per_day))
    conn.commit()
    conn.close()

def get_user_habits(user_id: int):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT id, name, times_per_day FROM habits WHERE user_id = ?", (user_id,))
    rows = cur.fetchall()
    conn.close()
    return rows

def get_habit(user_id: int, habit_id: int):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT id, name, times_per_day FROM habits WHERE user_id = ? AND id = ?", (user_id, habit_id))
    row = cur.fetchone()
    conn.close()
    return row

def increment_habit_log(user_id: int, habit_id: int, when: str):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    # Попробуем обновить строку; если нет — вставим
    cur.execute("SELECT id, times_done FROM habit_logs WHERE user_id = ? AND habit_id = ? AND date = ?",
                (user_id, habit_id, when))
    row = cur.fetchone()
    if row:
        log_id, times_done = row
        times_done += 1
        cur.execute("UPDATE habit_logs SET times_done = ? WHERE id = ?", (times_done, log_id))
    else:
        times_done = 1
        cur.execute("INSERT INTO habit_logs (user_id, habit_id, date, times_done) VALUES (?, ?, ?, ?)",
                    (user_id, habit_id, when, times_done))
    conn.commit()
    conn.close()
    return times_done

def get_today_times_done(user_id: int, habit_id: int, when: str):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT times_done FROM habit_logs WHERE user_id = ? AND habit_id = ? AND date = ?",
                (user_id, habit_id, when))
    row = cur.fetchone()
    conn.close()
    return row[0] if row else 0

def get_week_stats(user_id: int, habit_id: int, end_date: date):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    start = end_date - timedelta(days=6)  # 7 дней включая end_date
    cur.execute("""
        SELECT SUM(times_done) FROM habit_logs
        WHERE user_id = ? AND habit_id = ? AND date BETWEEN ? AND ?
    """, (user_id, habit_id, start.isoformat(), end_date.isoformat()))
    row = cur.fetchone()
    conn.close()
    return row[0] if row and row[0] is not None else 0

# UI: Главное меню (reply keyboard)
def main_menu_keyboard():
    kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
    kb.add(KeyboardButton("➕ Добавить привычку"))
    kb.add(KeyboardButton("✅ Отметить выполнение"))
    kb.add(KeyboardButton("📊 Статистика"))
    kb.add(KeyboardButton("❌ Выход"))
    return kb

# Inline клавиатура со списком привычек (для отметки)
def habits_inline_keyboard(habits):
    kb = InlineKeyboardMarkup(row_width=1)
    for hid, name, times in habits:
        kb.add(InlineKeyboardButton(text=f"{name} ({times}×/день)", callback_data=f"mark:{hid}"))
    return kb

# Inline клавиатура для статистики
def stats_inline_keyboard():
    kb = InlineKeyboardMarkup(row_width=2)
    kb.add(InlineKeyboardButton(text="Статистика за сегодня", callback_data="stat:today"))
    kb.add(InlineKeyboardButton(text="Статистика за неделю", callback_data="stat:week"))
    return kb

# /start
@dp.message(Command(commands=["start"]))
async def cmd_start(message: types.Message):
    await message.answer(
        "Привет! Я — Трекер привычек.\n\nВыбирай действие в меню.",
        reply_markup=main_menu_keyboard()
    )

# Обработка кнопок главного меню (reply)
@dp.message()
async def main_menu_handler(message: types.Message, state: FSMContext):
    text = message.text.strip()
    user_id = message.from_user.id

    if text == "➕ Добавить привычку":
        await message.answer("Введите название привычки (например, «Пить воду»). Для отмены напишите /cancel")
        await state.set_state(AddHabitStates.waiting_for_name)
        return

    if text == "✅ Отметить выполнение":
        habits = get_user_habits(user_id)
        if not habits:
            await message.answer("У вас пока нет привычек. Добавьте через ➕ Добавить привычку.", reply_markup=main_menu_keyboard())
            return
        kb = habits_inline_keyboard(habits)
        await message.answer("Выберите привычку, чтобы отметить выполнение:", reply_markup=kb)
        return

    if text == "📊 Статистика":
        await message.answer("Выберите период статистики:", reply_markup=stats_inline_keyboard())
        return

    if text == "❌ Выход":
        await message.answer("До встречи! Если нужно — снова нажмите /start", reply_markup=types.ReplyKeyboardRemove())
        return

    # Если бот в состоянии ожидания ввода — переключим его на FSM обработчики (см. ниже).
    # Для остальных случаев — покажем подсказку.
    await message.answer("Неизвестная команда. Используйте главное меню.", reply_markup=main_menu_keyboard())

# Отмена (для FSM)
@dp.message(Command(commands=["cancel"]))
async def cancel_handler(message: types.Message, state: FSMContext):
    if await state.get_state():
        await state.clear()
        await message.answer("Операция отменена.", reply_markup=main_menu_keyboard())
    else:
        await message.answer("Нечего отменять.", reply_markup=main_menu_keyboard())

# FSM: получаем название привычки
@dp.message(AddHabitStates.waiting_for_name)
async def process_habit_name(message: types.Message, state: FSMContext):
    name = message.text.strip()
    if not name:
        await message.answer("Название не может быть пустым. Введите название привычки.")
        return
    await state.update_data(name=name)
    await message.answer("Сколько раз в день нужно выполнять эту привычку? Введите целое число (например, 3).")
    await state.set_state(AddHabitStates.waiting_for_times)

# FSM: получаем times_per_day
@dp.message(AddHabitStates.waiting_for_times)
async def process_habit_times(message: types.Message, state: FSMContext):
    text = message.text.strip()
    try:
        times = int(text)
        if times <= 0:
            raise ValueError()
    except ValueError:
        await message.answer("Пожалуйста, введите положительное целое число (например, 3).")
        return

    data = await state.get_data()
    name = data.get("name")
    add_habit_to_db(message.from_user.id, name, times)
    await state.clear()
    await message.answer(f"Привычка «{name}» добавлена — нужно {times}× в день.", reply_markup=main_menu_keyboard())

# Обработка inline callbacks (отметка и статистика)
@dp.callback_query()
async def callback_handler(call: types.CallbackQuery):
    user_id = call.from_user.id
    data = call.data

    if data.startswith("mark:"):
        habit_id = int(data.split(":", 1)[1])
        habit = get_habit(user_id, habit_id)
        if not habit:
            await call.answer("Привычка не найдена.", show_alert=True)
            return
        _, name, times_per_day = habit
        today = get_today_str()
        times_done = increment_habit_log(user_id, habit_id, today)
        # Check if reached or exceeded
        if times_done >= times_per_day:
            await call.message.answer(f'Отлично! Норма по привычке "{name}" на сегодня выполнена! ({times_done}/{times_per_day})')
        else:
            await call.message.answer(f'Отметка сохранена: "{name}" — {times_done}/{times_per_day} сегодня.')
        await call.answer()  # закрыть "крутилку" на кнопке
        return

    if data == "stat:today":
        habits = get_user_habits(user_id)
        if not habits:
            await call.message.answer("У вас нет привычек для статистики.")
            await call.answer()
            return
        today = get_today_str()
        lines = ["📅 Статистика за сегодня:"]
        for hid, name, times in habits:
            done = get_today_times_done(user_id, hid, today)
            lines.append(f'• {name}: {done}/{times} (выполнено/цель)')
        await call.message.answer("\n".join(lines))
        await call.answer()
        return

    if data == "stat:week":
        habits = get_user_habits(user_id)
        if not habits:
            await call.message.answer("У вас нет привычек для статистики.")
            await call.answer()
            return
        end = datetime.now(TZ).date()
        lines = [f"📅 Статистика за неделю ({(end - timedelta(days=6)).isoformat()} — {end.isoformat()}):"]
        for hid, name, times_per_day in habits:
            total = get_week_stats(user_id, hid, end)
            goal = times_per_day * 7
            lines.append(f'• {name}: {total}/{goal} (за 7 дней)')
        await call.message.answer("\n".join(lines))
        await call.answer()
        return

    # неизвестный callback
    await call.answer()

# Обработчик ошибок и логирование простое
@dp.errors()
async def global_error_handler(update, exception):
    # здесь можно добавить логирование
    print("Ошибка:", exception)

# Запуск
async def main():
    print("Инициализация БД...")
    init_db()
    print("Бот запущен...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())