from aiogram import Bot, Dispatcher, types, F
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from inkb2 import begin_kb
from kb import kb
import asyncio


bot = Bot(
    token='8221121524:AAH_CZT-IEeLIduTQPm_Xw9YRlaflAEtYJw',
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)
dp = Dispatcher()


movies = {
    "Комедия": ["Суперсемейка", "Мальчишник в Вегасе", "День сурка", "Клик", "Отпетые мошенники"],
    "Ужасы": ["Оно", "Заклятие", "Пила", "Астрал", "Хэллоуин"],
    "Романтика": ["Титаник", "Дневник памяти", "Ла-Ла Ленд", "50 первых поцелуев", "Виноваты звезды"],
    "Фантастика": ["Интерстеллар", "Начало", "Матрица", "Марсианин", "Аватар"],
    "Приключения": ["Индиана Джонс", "Пираты Карибского моря", "Джуманджи", "Властелин колец", "Хоббит"]
}

@dp.message(Command("start"))
async def start_command(message: Message):
    await message.answer("Привет! Какой жанр фильмов больше нравится?", reply_markup=begin_kb)

@dp.callback_query()
async def genre_callback(callback: CallbackQuery):
    genre = callback.data
    await callback.message.answer(f"Вот список фильмов жанра {genre}: {', '.join(movies[genre])}")
    await callback.answer()

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())