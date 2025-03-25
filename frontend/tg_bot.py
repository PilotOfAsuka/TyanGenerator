import logging
from aiogram.types import Message
from aiogram.filters import Command
from frontend.photo_handler import handle_photo_generation  # переместил выше
from misc.core import bot, dp  # core должен быть в корне проекта

from tools.user_state_handler import users_data


from frontend.text_handler_functions import set_language_dialogue, if_in_generation, in_main_state
from frontend.keyboards.menu_gen import menuConstructor

from misc.descriptions import get_description

# Промпт по умолчанию
eng_prompt = "Add a realistically styled girlfriend standing next to the existing person in the image. Generate her appearance, clothing, and pose naturally to match the scene's lighting and perspective. Ensure her positioning, facial expression, and body language suggest a natural and affectionate connection, as if she belongs in the original photo."

# Настраиваем логирование
logging.basicConfig(level=logging.INFO)



# Команда /start — просто показывает описание
@dp.message(Command("start"))
async def cmd_start(message: Message):

    users_data.init_self_states(message=message) # Инициализируем информацию о пользователе при старте
    users_data.set_user_state(message=message, state="main") # Устанавливаем состаяние main базовое состояние

    # Проверяем установку языка
    if users_data.get_user_language(message=message) is None:
        users_data.set_user_state(message=message, state="set_lang") # Устанавливаем состояние "set_lang"
        await message.answer("Выберите язык / Choose your language:", reply_markup=menuConstructor.get_menu("language"))
    else:
        await message.answer(get_description(lang=users_data.get_user_language(message=message)), parse_mode="HTML", reply_markup=menuConstructor.get_menu("main_menu"))


# Команда /language — Для выбора языка
@dp.message(Command("language"))
async def cmd_language(message: Message):
    if users_data.compare_self_state(message=message, state="main"):
        users_data.set_user_state(message=message, state="set_lang")  # Устанавливаем состояние "set_lang"
        await message.answer("Выберите язык / Choose your language:", reply_markup=menuConstructor.get_menu("language"))


# отправка промпта и фото в photo_handler.py
@dp.message(lambda message: message.photo)
async def handle_photo(message: Message):
    if users_data.compare_self_state(message=message, state="start_generation"):
        advance_prompt = users_data.get_user_prompt(message=message) # Здесь будет формироваться адванц промпт
        await handle_photo_generation(message, eng_prompt)


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

    else:
        logging.info(msg=f"Пользователь {message.from_user.username}, потерялся :)")



# Запуск бота
async def start():
    await dp.start_polling(bot)
