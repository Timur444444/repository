from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

question1_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Меркурий", callback_data="right1"),
            InlineKeyboardButton(text="Венера", callback_data="wrong1"),
            InlineKeyboardButton(text="Марс", callback_data="wrong1")
        ]
    ]
)
question2_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="1914", callback_data="wrong2"),
            InlineKeyboardButton(text="1941", callback_data="wrong2"),
            InlineKeyboardButton(text="1939", callback_data="right2")
        ]
    ]
)
question3_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Гепард", callback_data="right3"),
            InlineKeyboardButton(text="Лев", callback_data="wrong3"),
            InlineKeyboardButton(text="Лошадь", callback_data="wrong3")
        ]
    ]
)
question4_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Гуанчжоу", callback_data="wrong4"),
            InlineKeyboardButton(text="Пекин", callback_data="right4"),
            InlineKeyboardButton(text="Шанхай", callback_data="wrong4")
        ]
    ]
)
question5_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Арбуз", callback_data="wrong5"),
            InlineKeyboardButton(text="Голубика", callback_data="right5"),
            InlineKeyboardButton(text="Клубника", callback_data="wrong5")
        ]
    ]
)