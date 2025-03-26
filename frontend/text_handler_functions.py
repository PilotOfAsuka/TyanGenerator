from tools.user_state_handler import users_data
from misc.descriptions import get_description
import logging
from frontend.keyboards.menu_gen import menuConstructor
from frontend.advanced_prompt import handle_advanced_prompt
from misc.lang_core import lang

async def set_lang_and_answer(message, lang=None):
    users_data.set_user_language(message=message, language=lang)
    await message.answer(get_description(lang=users_data.get_user_language(message=message)), parse_mode="HTML",
                         reply_markup=menuConstructor.get_menu_with_lang(menu_name="main_menu", lang=users_data.get_user_language(message=message)))
    users_data.set_user_state(message=message, state="main")  # Устанавливаем состояние main базовое состояние


logging.basicConfig(level=logging.INFO)

async def if_in_generation(message):
    await message.answer(text=lang.get(key="wait_generation", lang=users_data.get_user_language(message=message))) # users_data.set_user_state(message=message, state="main")

async def set_language_dialogue(message):
    if message.text.lower() == "русский":
        await set_lang_and_answer(message=message, lang="ru")
    elif message.text.lower() == "english":
        await set_lang_and_answer(message=message, lang="en")
    else:
        logging.info(msg=f"Ошибка установки языка пользователю {message.from_user.username}, message: {message.text}")

async def in_main_state(message):
    if message.text.lower() in {
        menuConstructor.get_button_text(menu_name="main_menu_ru", index=0).lower(),
        menuConstructor.get_button_text(menu_name="main_menu_en", index=0).lower()
    }:
        users_data.set_user_state(message=message, state="start_generation")
        await message.answer(text=lang.get(key="send_photo", lang=users_data.get_user_language(message=message)))
    elif message.text.lower() in {
        menuConstructor.get_button_text(menu_name="main_menu_ru", index=1).lower(),
        menuConstructor.get_button_text(menu_name="main_menu_en", index=1).lower()
    }:# Тут будет переход в состояние генерации Адванц промпт
        await handle_advanced_prompt(message)

    elif message.text.lower() in {
        menuConstructor.get_button_text(menu_name="main_menu_ru", index=2).lower(),
        menuConstructor.get_button_text(menu_name="main_menu_en", index=2).lower()
    }:
        users_data.set_user_state(message=message, state="set_lang")
        await message.answer("Выберите язык / Choose your language:", reply_markup=menuConstructor.get_menu("language"))