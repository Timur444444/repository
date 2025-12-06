from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

begin_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Комедия", callback_data="Комедия"),
            InlineKeyboardButton(text="Ужасы", callback_data="Ужасы"),
            InlineKeyboardButton(text="Романтика", callback_data="Романтика")
        ],
        [
            InlineKeyboardButton(text="Фантастика", callback_data="Фантастика"),
            InlineKeyboardButton(text="Приключения", callback_data="Приключения")
        ]
    ]
)