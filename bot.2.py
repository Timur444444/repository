from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.filters import Command
from db import init_db, add_favorite, get_favorites
import json
import requests
import os
import asyncio

JSON_FILE = "currencies.json"

bot = Bot(token='8473814638:AAG8PD9XVrsvFe9yLTcj52DSouK1yHmSJAI')
dp = Dispatcher(storage=MemoryStorage())


if not os.path.exists(JSON_FILE):
    raise FileNotFoundError(f"❌ Не найден файл {JSON_FILE}! Положи его рядом с этим скриптом.")

try:
    with open(JSON_FILE, "r", encoding="utf-8") as f:
        currency_data = json.load(f)
        currencies = [item["code"].upper() for item in currency_data]

    currency_lookup = {}
    for item in currency_data:
        code = item["code"].upper()
        currency_lookup[code.lower()] = code

        if "symbol" in item and item["symbol"]:
            currency_lookup[item["symbol"].lower()] = code

        if "rusname" in item and item["rusname"]:
            currency_lookup[item["rusname"].lower()] = code

        for name in item.get("names", []):
            currency_lookup[name.lower()] = code

except json.JSONDecodeError:
    raise ValueError("⚠️ Ошибка в формате currencies.json. Проверь синтаксис JSON.")


def parse_currency(text: str):
    """Определение валюты по коду, символу или названию."""
    if not text:
        return None
    return currency_lookup.get(text.strip().lower())


class ConvertStates(StatesGroup):
    waiting_for_amount = State()
    waiting_for_base = State()
    waiting_for_target = State()


def get_result_keyboard(base, target, amount):
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(
                text="🔄 Поменять валюты",
                callback_data=f"swap:{base}:{target}:{amount}"
            )
        ],
        [
            InlineKeyboardButton(
                text="🔁 Повторить",
                callback_data="repeat"
            )
        ],
        [
            InlineKeyboardButton(
                text="⭐ Сохранить",
                callback_data=f"save:{base}:{target}"
            )
        ]
    ])


@dp.message(Command("start"))
async def start(message: types.Message, state: FSMContext):
    await message.answer("💱 Введи сумму для конвертации:")
    await state.set_state(ConvertStates.waiting_for_amount)


@dp.message(ConvertStates.waiting_for_amount)
async def get_amount(message: types.Message, state: FSMContext):
    try:
        amount = float(message.text.strip())
        await state.update_data(amount=amount)
    except ValueError:
        await message.answer("Пожалуйста, введи только число, например 10 или 10.5.")
        return

    keyboard = []
    row = []
    for i, cur in enumerate(currencies, start=1):
        row.append(KeyboardButton(text=cur))
        if i % 3 == 0:
            keyboard.append(row)
            row = []
    if row:
        keyboard.append(row)

    markup = ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)
    await message.answer("Из какой валюты перевести?", reply_markup=markup)
    await state.set_state(ConvertStates.waiting_for_base)

@dp.message(ConvertStates.waiting_for_base)
async def get_base_currency(message: types.Message, state: FSMContext):
    base = parse_currency(message.text)
    if not base:
        await message.answer("❌ Не удалось распознать валюту. Введи код (USD), символ ($) или название.")
        return

    await state.update_data(base=base)

    keyboard = []
    row = []
    for i, cur in enumerate(currencies, start=1):
        row.append(KeyboardButton(text=cur))
        if i % 3 == 0:
            keyboard.append(row)
            row = []
    if row:
        keyboard.append(row)

    markup = ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)
    await message.answer("В какую валюту перевести?", reply_markup=markup)
    await state.set_state(ConvertStates.waiting_for_target)


@dp.message(ConvertStates.waiting_for_target)
async def get_target_currency(message: types.Message, state: FSMContext):
    target = parse_currency(message.text)
    if not target:
        await message.answer("❌ Не удалось распознать валюту. Введи код (EUR), символ (€) или название.")
        return

    data = await state.get_data()
    amount = data["amount"]
    base = data["base"]

    try:
        url = f"https://open.er-api.com/v6/latest/{base}"
        response = requests.get(url, timeout=10)
        data_json = response.json()

        if data_json.get("result") != "success":
            await message.answer("❌ Не удалось загрузить курсы валют. Попробуй позже.")
            await state.clear()
            return

        rates = data_json["rates"]
        if target not in rates:
            await message.answer("❌ Такой валюты нет в списке.")
            return

        converted = amount * rates[target]
        await message.answer(
            f"💹 {amount} {base} = {converted:.2f} {target}",
            reply_markup=get_result_keyboard(base, target, amount)
        )

    except Exception as e:
        await message.answer(f"⚠️ Ошибка при конвертации: {e}")

    await state.clear()


@dp.callback_query(lambda c: c.data == "repeat")
async def repeat_conversion(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer("💱 Введи новую сумму:")
    await state.set_state(ConvertStates.waiting_for_amount)
    await callback.answer()


@dp.callback_query(lambda c: c.data.startswith("swap"))
async def swap_currencies(callback: types.CallbackQuery, state: FSMContext):
    _, base, target, amount = callback.data.split(":")
    amount = float(amount)

    new_base, new_target = target, base

    url = f"https://open.er-api.com/v6/latest/{new_base}"
    resp = requests.get(url).json()
    rate = resp["rates"][new_target]
    converted = amount * rate

    await callback.message.answer(
        f"🔄 Обновлено!\n\n💹 {amount} {new_base} = {converted:.2f} {new_target}",
        reply_markup=get_result_keyboard(new_base, new_target, amount)
    )
    await callback.answer()


@dp.callback_query(lambda c: c.data.startswith("save"))
async def save_rate(callback: types.CallbackQuery):
    _, base, target = callback.data.split(":")
    user_id = callback.from_user.id

    add_favorite(user_id, base, target)

    await callback.message.answer(f"⭐ Сохранено: {base} → {target}")
    await callback.answer()

    
@dp.message(Command("favorites"))
async def show_favorites(message: types.Message):
    user_id = message.from_user.id
    favs = get_favorites(user_id)

    if not favs:
        await message.answer("⭐ У тебя пока нет сохранённых валют.")
        return

    text = "⭐ Твои сохранённые пары:\n\n"
    for base, target in favs:
        text += f"• {base} → {target}\n"

    await message.answer(text)


async def main():
    print("✅ Бот запущен...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    init_db() 
    asyncio.run(main())
