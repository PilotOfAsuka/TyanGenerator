from tools.user_state_handler import users_data
from misc.descriptions import get_description
import logging
from frontend.keyboards.menu_gen import menuConstructor
from frontend.advanced_prompt import handle_advanced_prompt


# Здесь отдельные функции обработки текста

logging.basicConfig(level=logging.INFO)

async def if_in_generation(message):
    await message.answer(text="Дождитесь конца генерации...\nЕсли генерация занимает больше минуты (Что не должно быть) напишите /start") # users_data.set_user_state(message=message, state="main")

async def set_language_dialogue(message):
    if message.text.lower() == "русский":
        users_data.set_user_language(message=message, language="ru")
        await message.answer(get_description(lang=users_data.get_user_language(message=message)), parse_mode="HTML",
                             reply_markup=menuConstructor.get_menu("main_menu"))
        users_data.set_user_state(message=message, state="main")  # Устанавливаем состояние main базовое состояние
    elif message.text.lower() == "english":
        users_data.set_user_language(message=message, language="en")
        await message.answer(get_description(lang=users_data.get_user_language(message=message)), parse_mode="HTML",
                             reply_markup=menuConstructor.get_menu("main_menu"))
        users_data.set_user_state(message=message, state="main")  # Устанавливаем состояние main базовое состояние
    else:
        logging.info(msg=f"Ошибка установки языка пользователю {message.from_user.username}, message: {message.text}")

async def in_main_state(message):
    if message.text.lower() == menuConstructor.get_button_text(menu_name="main_menu", index=0).lower():
        users_data.set_user_state(message=message, state="start_generation")
        await message.answer(text="Можете теперь отправить фото.")
    elif message.text.lower() == menuConstructor.get_button_text(menu_name="main_menu", index=1).lower():
        # Тут будет переход в состояние генерации Адванц промпт
        await handle_advanced_prompt(message)

    elif message.text.lower() == menuConstructor.get_button_text(menu_name="main_menu", index=2).lower():
        users_data.set_user_state(message=message, state="set_lang")
        await message.answer("Выберите язык / Choose your language:", reply_markup=menuConstructor.get_menu("language"))