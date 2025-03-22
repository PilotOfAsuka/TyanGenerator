import logging
from aiogram.types import Message
from aiogram.filters import Command
from frontend.advanced_prompt import handle_advanced_prompt
from frontend.photo_handler import handle_photo_generation  # переместил выше
from frontend.core import bot, dp  # core должен быть в корне проекта

from tools.user_state_handler import users_data

from frontend.text_handler import set_language_dialogue, if_in_generation
from frontend.keyboards.language_keyboard import language_keyboard

from frontend.descriptions import get_description

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
        await message.answer("Выберите язык / Choose your language:", reply_markup=language_keyboard)
    else:
        await message.answer(get_description(lang=users_data.get_user_language(message=message)), parse_mode="HTML")


# Команда /language — Для выбора языка
@dp.message(Command("language"))
async def cmd_language(message: Message):
    if users_data.compare_self_state(message=message, state="main"):
        users_data.set_user_state(message=message, state="set_lang")  # Устанавливаем состояние "set_lang"
        await message.answer("Выберите язык / Choose your language:", reply_markup=language_keyboard)



# Команда /advancedprompt — Для расширенного выбора
@dp.message(Command("advancedprompt"))
async def cmd_advanced_prompt(message: Message):
    await handle_advanced_prompt(message)

# Команда /start_generation
@dp.message(Command("start_generation"))
async def start_generation(message: Message):
    if users_data.compare_self_state(message=message, state="main"):
        users_data.set_user_state(message=message, state="start_generation")
        await message.answer(text="Можете теперь отправить фото.")


# отправка промпта и фото в photo_handler.py
@dp.message(lambda message: message.photo)
async def handle_photo(message: Message):
    if users_data.compare_self_state(message=message, state="start_generation"):
        advance_prompt = users_data.get_user_prompt(message=message)
        await handle_photo_generation(message, eng_prompt)


# Обработка текстовых сообщений от пользователя
@dp.message(lambda message: message.text)
async def handle_text_from_user(message: Message):
    # Проверяем что пользователь находится в состоянии установки языка для обработки входящих текстов от кнопок
    if users_data.compare_self_state(message=message, state="set_lang"):
        await set_language_dialogue(message=message)
    # Проверяем что пользователь находится в состоянии генерации
    elif users_data.compare_self_state(message=message, state="ingeneration"):
        await if_in_generation(message=message)

    else:
        logging.info(msg=f"Пользователь {message.from_user.username}, потерялся :)")


# Запуск бота
async def start():
    await dp.start_polling(bot)
