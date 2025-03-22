from tools.user_state_handler import users_data
from frontend.descriptions import get_description
import logging

# Здесь отдельные функции обработки текста

logging.basicConfig(level=logging.INFO)

async def if_in_generation(message):
    await message.answer(text="Дождитесь конца генерации...")

async def set_language_dialogue(message):
    if message.text.lower() == "русский":
        users_data.set_user_language(message=message, language="ru")
        await message.answer(get_description(lang=users_data.get_user_language(message=message)), parse_mode="HTML")
        users_data.set_user_state(message=message, state="main")  # Устанавливаем состояние main базовое состояние
    elif message.text.lower() == "english":
        users_data.set_user_language(message=message, language="en")
        await message.answer(get_description(lang=users_data.get_user_language(message=message)), parse_mode="HTML")
        users_data.set_user_state(message=message, state="main")  # Устанавливаем состояние main базовое состояние
    else:
        logging.info(msg=f"Ошибка установки языка пользователю {message.from_user.username}, message: {message.text}")