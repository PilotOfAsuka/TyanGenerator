from backend.prompts import add_boyfriend_prompt, add_girlfriend_prompt

from tools.user_state_handler import users_data
from misc.descriptions import get_description
import logging
from frontend.keyboards.menu_gen import menuConstructor
from misc.lang_core import lang

async def set_lang_and_answer(message, lang=None):
    users_data.set_user_language(message=message, language=lang)
    await message.answer(get_description(lang=users_data.get_user_language(message=message)), parse_mode="HTML",
                         reply_markup=menuConstructor.get_menu_with_lang(menu_name="main_menu", message=message))
    users_data.set_user_state(message=message, state="main")  # Устанавливаем состояние main базовое состояние


logging.basicConfig(level=logging.INFO)

async def back_to_main(message):
    if message.text.lower() in menuConstructor.get_button_text(menu_name="back_button", index=0, message=message).lower():
        users_data.set_user_state(message=message, state="main")  # Устанавливаем состаяние main базовое состояние
        await message.answer(get_description(lang=users_data.get_user_language(message=message)), parse_mode="HTML",
                             reply_markup=menuConstructor.get_menu_with_lang(menu_name="main_menu", message=message))

async def if_in_generation(message):
    await message.answer(text=lang.get(key="wait_generation", message=message))

async def set_language_dialogue(message):
    if message.text.lower() == "русский":
        await set_lang_and_answer(message=message, lang="ru")
    elif message.text.lower() == "english":
        await set_lang_and_answer(message=message, lang="en")
    else:
        logging.info(msg=f"Ошибка установки языка пользователю {message.from_user.username}, message: {message.text}")

async def in_main_state(message):
    if message.text.lower() in menuConstructor.get_button_text(menu_name="main_menu", index=0, message=message).lower():
        users_data.set_user_state(message=message, state="start_generation")
        users_data.set_user_prompt(message=message,prompt=add_girlfriend_prompt)
        await message.answer(text=lang.get(key="send_photo", message=message),  reply_markup=menuConstructor.get_menu_with_lang(menu_name="back_button", message=message))
    if message.text.lower() in menuConstructor.get_button_text(menu_name="main_menu", index=1, message=message).lower():
        users_data.set_user_state(message=message, state="start_generation")
        users_data.set_user_prompt(message=message, prompt=add_boyfriend_prompt)
        await message.answer(text=lang.get(key="send_photo", message=message),  reply_markup=menuConstructor.get_menu_with_lang(menu_name="back_button", message=message))

    elif message.text.lower() in menuConstructor.get_button_text(menu_name="main_menu", index=3, message=message).lower():
        users_data.set_user_state(message=message, state="set_lang")
        await message.answer("Выберите язык / Choose your language:", reply_markup=menuConstructor.get_menu("language"))