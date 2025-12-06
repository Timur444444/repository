from aiogram import Bot, Dispatcher, types, F
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from fsm import Form
from inkb import game_kb
from inkb3 import question1_kb, question2_kb, question3_kb, question4_kb, question5_kb
from kb import kb
import asyncio
import db3
import sqlite3


bot = Bot(
    token='8326922803:AAErPSMCIxsxHR5BfthRLOJ_moeQqIkJBsM',
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)
dp = Dispatcher()


@dp.message(Command("start"))
async def start_command(message: Message):
    name = message.from_user.first_name or message.from_user.username or "друг"
    await message.answer(f"Привет, {name}! Рад тебя видеть.")

@dp.message(Command("start2"))
async def echo(message: Message):
    await message.answer("Привет вот тебе кнопочки) ", reply_markup=kb)

@dp.message(F.text == "Меню")
async def echo(message: Message):
    await message.answer("Вот ваше меню)")

@dp.message(F.text == "О нас")
async def echo(message: Message):
    await message.answer("Наш бот помогает пользователям быстро получать актуальную информацию. Мы стремися сделать взаимодействие простым, быстрым и безопасным.")

@dp.message(F.text == "Контакты")
async def echo(message: Message):
    await message.answer("Телефон: +37368956269")

@dp.message(F.text == "Новости")
async def echo(message: Message):
    await message.answer("Информация о последних изменениях и учучшениях нашего сервиса чтобы вы были всегда в курсе.")

@dp.message(F.text == "Ресурсы")
async def echo(message: Message):
    await message.answer("Здесь вы найдёте полезные материалы и инструкции для удобного использвания бота.")

@dp.message(F.text == "Советы")
async def echo(message: Message):
    await message.answer("Полезные советы для использования сервиса, чтобы было с ним работать проще.")

@dp.message(F.text == "Поддержка")
async def echo(message: Message):
    await message.answer("Если нужна помощь, вы можете связаться по номеру телефона в разделе (Контакты).")

@dp.callback_query(F.data == "add_to_cart")
async def menu_callback(callback: Message):
    await callback.message.answer("Вот ваше меню)")
    await callback.answer()

@dp.message(Command("about"))
async def echo(message: Message):
    await message.answer("Этот бот создан для работы и тестирования функций Telegram ботов.")

@dp.message(Command("end"))
async def echo(message: Message):
    name = message.from_user.first_name or message.from_user.username or "друг"
    await message.answer(f"Прощай, {name}! Ещё увидимся!")

@dp.message(Command("help"))
async def echo(message: Message):
    text = (
        "<b> Доступные команды:</b>\n"
        "<b>/start</b> - начать работу\n"
        "<b>/about</b> - о боте\n"
        "<b>/help</b> - список команд\n"
        "<b>/end</b> - завершить работу\n"
        "<b>start2</b> - reply кнопки\n"
        "<b>admin</b> - Админ\n"
        "<b>quiz</b> - Игра\n"
    )
    await message.answer(text)

@dp.message(Command("admin"))
async def admin_command(message: Message):
    await message.answer("Введи пароль.")

@dp.message(F.text=="4444")
async def admin__(message: Message):
    await message.answer("Ты теперь админ")

@dp.message(Command("quiz"))
async def quiz_command(message: Message):
    await message.answer("Какое из животных не умеет прыгать?", reply_markup=game_kb)

@dp.callback_query(F.data=="right")
async def menu_callback(callback: Message):
    await callback.message.answer("Да! Это же кит.")
    await callback.answer()

@dp.callback_query(F.data=="wrong")
async def menu_callback(callback: Message):
    await callback.message.answer("Нет, попробуй ещё раз.")
    await callback.message.answer("Какое из животных не умеет прыгать", reply_markup=game_kb)
    await callback.answer()

@dp.message(Command("form"))
async def from_FSM(message: Message, state: FSMContext):
    await message.answer("Привет введи своё имя")
    await state.set_state(Form.name)

@dp.message(Form.name)
async def name_FSM(message: Message, state: FSMContext):
    await message.answer("Супер! Теперь введи свой возраст")
    await state.update_data(name=message.text)
    await state.set_state(Form.age)

@dp.message(Form.age)
async def age_FSM(message: Message, state: FSMContext):
    await message.answer("Отлично! Но какой твой любимый фильм?")
    await state.update_data(age=message.text)
    await state.set_state(Form.movie)

@dp.message(Form.movie)
async def  movie_FSM(message: Message, state: FSMContext):
    await message.answer("Отлично! Ты выполнил форму")
    await state.update_data(movie=message.text)
    data = state.get_data()
    await state.clear()

@dp.message(Command("cancel"))
async def cancel(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Анкета отменена.")

@dp.message(Command("game"))
async def cancel(message: Message, state: FSMContext):
    await message.answer("Напиши свою любимую игру")
    await state.set_state(Form.game)

@dp.message(Form.game)
async def game_FSM(message: Message, state: FSMContext):
    await message.answer("Отлично! Ты выполнил форму.")
    await state.update_data(game=message.text)
    data = await state.get_data()
    print(data)
    await state.clear()

@dp.message(Command("quiz2"))
async def quiz2_command(message: Message):
    await message.answer("Какая самая близкая планета к солнцу?", reply_markup=question1_kb)

@dp.callback_query(F.data=="right1")
async def right1(callback: Message):
    await callback.message.answer("Правильно! Меркурий ")
    await callback.message.answer("В каком году началась вторая мировая война?", reply_markup=question2_kb)
    await callback.answer()

@dp.callback_query(F.data=="wrong1")
async def wrong1(callback: Message):
    await callback.message.answer("Нет, попробуй ещё раз ")
    await callback.message.answer("Какая самая близкая планета к солнцу?", reply_markup=question1_kb)
    await callback.answer()

@dp.callback_query(F.data=="right2")
async def right2(callback: Message):
    await callback.message.answer("Да! 1939 ")
    await callback.message.answer("Самое быстрое наземное животное?", reply_markup=question3_kb)
    await callback.answer()

@dp.callback_query(F.data=="wrong2")
async def wrong2(callback: Message):
    await callback.message.answer("Нет, попробуй ещё раз ")
    await callback.message.answer("В каком году началась вторая мировая война?", reply_markup=question2_kb)
    await callback.answer()

@dp.callback_query(F.data=="right3")
async def right3(callback: Message):
    await callback.message.answer("Правильно! Гепард ")
    await callback.message.answer("Какая столица Китая?", reply_markup=question4_kb)
    await callback.answer()

@dp.callback_query(F.data=="wrong3")
async def wrong3(callback: Message):
    await callback.message.answer("Нет, попробуй ещё раз ")
    await callback.message.answer("Самое быстрое наземное животное?", reply_markup=question3_kb)
    await callback.answer()

@dp.callback_query(F.data=="right4")
async def right4(callback: Message):
    await callback.message.answer("Да! Пекин ")
    await callback.message.answer("Какая ягода синяя?", reply_markup=question5_kb)
    await callback.answer()

@dp.callback_query(F.data=="wrong4")
async def wrong4(callback: Message):
    await callback.message.answer("Нет, попробуй ещё раз ")
    await callback.message.answer("Какая столица Китая?", reply_markup=question4_kb)
    await callback.answer()

@dp.callback_query(F.data=="right5")
async def right5(callback: Message):
    await callback.message.answer("Правильно! Голубика ")
    await callback.message.answer("Поздравляю! Вы прошли викторину ")
    await callback.answer()

@dp.callback_query(F.data=="wrong5")
async def wrong5(callback: Message):
    await callback.message.answer("Нет, попробуй ещё раз ")
    await callback.message.answer("Какая ягода синяя?", reply_markup=question5_kb)
    await callback.answer()

def food_insert(name, price):
    conn_f = sqlite3.connect("food.db")
    cursor_f = conn_f.cursor()
    cursor_f.execute("INSERT INTO food(name, price) VALUES (?, ?)", (name, price))
    conn_f.commit()
    conn_f.close()

@dp.message()
async def echo(message: Message):
    await message.answer(message.text)

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())


