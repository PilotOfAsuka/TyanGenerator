from backend.prompts import add_boyfriend_prompt, add_girlfriend_prompt

from tools.user_state_handler import users_data
from misc.descriptions import get_description, get_about_text
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
    await is_press_button(message=message, menu_name="main_menu", button_index=0, set_user_state="ready_to_generation", set_user_prompt=add_girlfriend_prompt, answer_text=lang.get(message=message, key="send_photo"), reply_markup=menuConstructor.get_menu_with_lang(message=message, menu_name="back_button"))
    await is_press_button(message=message, menu_name="main_menu", button_index=1, set_user_state="ready_to_generation", set_user_prompt=add_boyfriend_prompt,  answer_text=lang.get(message=message, key="send_photo"), reply_markup=menuConstructor.get_menu_with_lang(message=message, menu_name="back_button"))
    await is_press_button(message=message, menu_name="main_menu", button_index=2, set_user_state="get_advance_prompt", answer_text="Отправь текст промпта:", reply_markup=menuConstructor.get_menu_with_lang(message=message, menu_name="back_button"))
    await is_press_button(message=message, menu_name="main_menu", button_index=3, set_user_state="set_lang", answer_text="Выберите язык / Choose your language:", reply_markup=menuConstructor.get_menu("language"))
    await is_press_button(message=message, menu_name="main_menu", button_index=4, answer_text=get_about_text(users_data.get_user_language(message=message)))

async def is_press_button(message, menu_name: str, button_index: int, set_user_state=None, set_user_prompt=None, answer_text=None, reply_markup=None):
    button_text = menuConstructor.get_button_text(menu_name=menu_name, index=button_index, message=message).lower()
    if message.text.lower() == button_text:
        if set_user_state:
            users_data.set_user_state(message=message, state=set_user_state)
        if set_user_prompt:
            users_data.set_user_prompt(message=message, prompt=set_user_prompt)
        if answer_text:
            await message.answer(text=answer_text,
                             reply_markup=reply_markup)
