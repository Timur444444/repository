from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Меню"),
            KeyboardButton(text="О нас"),
            KeyboardButton(text="Контакты")
        ],
        [
            KeyboardButton(text="Ресурсы"),
            KeyboardButton(text="Новости"),
            KeyboardButton(text="Советы")
        ],
        [
            KeyboardButton(text="Поддержка")
        ]
    ],
    resize_keyboard=True
)

