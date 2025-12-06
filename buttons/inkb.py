from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

product_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Добавить в корзину", callback_data="add_to_cart")
        ]
    ]
)

game_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Dog", callback_data="wrong"),
            InlineKeyboardButton(text="Cat", callback_data="wrong"),
            InlineKeyboardButton(text="Whale", callback_data="right")
        ]
    ]
)
