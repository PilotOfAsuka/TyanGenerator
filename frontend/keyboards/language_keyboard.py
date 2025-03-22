from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

language_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Русский"), KeyboardButton(text="English")]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)
