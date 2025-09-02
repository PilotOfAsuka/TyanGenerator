import logging
from aiogram.types import Message
from aiogram.filters import Command
from aiogram import F
from frontend.photo_handler import handle_photo_for_generation  # переместил выше
from misc.core import bot, dp
from tools.user_state_handler import users_data


from frontend.text_handler_functions import set_language_dialogue, if_in_generation, in_main_state, back_to_main
from frontend.keyboards.menu_gen import menuConstructor

from misc.descriptions import get_description, get_about_text
from misc.lang_core import lang


# Промпт по умолчанию
eng_prompt_old = "Add a realistically styled girlfriend standing next to the existing person in the image. Generate her appearance, clothing, and pose naturally to match the scene's lighting and perspective. Ensure her positioning, facial expression, and body language suggest a natural and affectionate connection, as if she belongs in the original photo."
eng_prompt = "Preserve the original person in the photo exactly as they are. Do not change their face, body, hairstyle, or clothing. Only add a realistically styled girlfriend standing naturally next to them. She should match the scene’s lighting, perspective, and background.Her body language and facial expression should suggest a warm and affectionate connection,as if she belongs in the original photo."

# Настраиваем логирование
logging.basicConfig(level=logging.INFO)

albums = []

# Команда /start — просто показывает описание
@dp.message(Command("start"))
async def cmd_start(message: Message):

    users_data.init_self_states(message=message) # Инициализируем информацию о пользователе при старте
    users_data.set_user_state(message=message, state="main") # Устанавливаем состаяние main базовое состояние

    # Проверяем установку языка
    if users_data.get_user_language(message=message) is None:
        await cmd_language(message)
    else:
        await message.answer(get_description(lang=users_data.get_user_language(message=message)), parse_mode="HTML",
                             reply_markup=menuConstructor.get_menu_with_lang(menu_name="main_menu", message=message))


# Команда /language — Для выбора языка
@dp.message(Command("language"))
async def cmd_language(message: Message):
    if users_data.compare_self_state(message=message, state="main"):
        users_data.set_user_state(message=message, state="set_lang")  # Устанавливаем состояние "set_lang"
        await message.answer("Выберите язык / Choose your language:", reply_markup=menuConstructor.get_menu("language"))

# Команда /about — Для about menu
@dp.message(Command("about"))
async def cmd_about(message: Message):
    about_message = get_about_text(users_data.get_user_language(message=message))
    await message.answer(about_message)


# отправка промпта и фото в photo_handler.py
@dp.message(F.photo)
async def handle_photo(message: Message):
    album = message.media_group_id
    if users_data.compare_self_state(message=message, state="ready_to_generation"):
        if not album:
            await handle_photo_for_generation(message, users_data.get_user_prompt(message=message))
        else:
            # Тут идет обработка когда отправлено много фото, НО он обрабатывает все (надо просто придумать как сделать иначе)
            await message.answer(lang.get(key="many_photo_err", message=message))



# Обработка текстовых сообщений от пользователя
@dp.message(lambda message: message.text)
async def handle_text_from_user(message: Message):
    # Проверяем что пользователь находится в состоянии
    if users_data.compare_self_state(message=message, state="main"):
        await in_main_state(message=message)
    elif users_data.compare_self_state(message=message, state="set_lang"):
        await set_language_dialogue(message=message)
    # Проверяем что пользователь находится в состоянии генерации
    elif users_data.compare_self_state(message=message, state="ingeneration"):
        await if_in_generation(message=message)
    elif users_data.compare_self_state(message=message, state="ready_to_generation"):
        await back_to_main(message=message)
    elif users_data.compare_self_state(message=message, state="get_advance_prompt"):
        await back_to_main(message=message)
        users_data.set_user_prompt(message=message, prompt=message.text)
        await message.answer(lang.get(message=message, key="send_photo"), reply_markup=menuConstructor.get_menu_with_lang(message=message, menu_name="back_button"))
        users_data.set_user_state(message=message, state="ready_to_generation")

    else:
        logging.info(msg=f"Пользователь {message.from_user.username}, потерялся :)")
        await message.answer(text=lang.get(key="all_error", message=message))

# Запуск бота
async def start():
    await dp.start_polling(bot)
