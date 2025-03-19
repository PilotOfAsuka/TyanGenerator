import base64
import logging
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import Command
from tools.user_state_handler import user_states
from tools.my_func import get_id_from_message
from backend.gemineai import get_tyan_image

from config import tg_api

# Это каркас бота в телеграм

rus_prompt = "Добавь девушку (внешность придумай сам) (позу и действие придумай на основе изображеня как бы ты паместил ее), стоящую рядом с существующим человеком)"
eng_prompt = "Add a girlfriend (think up her appearance yourself) (think up her pose and action based on the image of how you would place her) standing next to an existing person)"

logging.basicConfig(level=logging.INFO)

bot = Bot(token=tg_api)
dp = Dispatcher()

@dp.message(Command("start_generation"))
async def cmd_generation(message: Message):
    # здесь будет начало генерации
    user_states.set_user_state(state="start_generation", user_id=get_id_from_message(message))
    await message.answer(text="Отправьте фотографию на которую хотите дорисовать тян.")
    pass

# /start
@dp.message(Command("start"))
async def cmd_start(message: Message):
    user_states.init_self_states(user_id=get_id_from_message(message))
    user_states.set_user_state(state="main", user_id=get_id_from_message(message))
    await message.answer(f"Привет! Я бот который добавит тянку если получится :)\n На ваше изображение.\nВозможны искажения и прочие недочеты.\nОснованно на gemini-2.0-flash-exp от Google!\n")

# Обработка текста
@dp.message(lambda message: message.text)
async def handle_text(message: Message):
    # Обработка текста по состоянию юзера
    if user_states.get_user_state(user_id=get_id_from_message(message)) == "generation":
        await message.answer(text="Происходит генерация, подождите...")
    elif user_states.get_user_state(user_id=get_id_from_message(message)) == "main":
        await message.answer(text="Используйте команду /start_generation для старта")
        pass


# Обработчик изображений
@dp.message(lambda message: message.photo)
async def handle_photo(message: Message):
    if user_states.get_user_state(user_id=get_id_from_message(message)) == "start_generation":
        photo = message.photo[-1]  # Берем наибольшее по размеру изображение
        file = await bot.get_file(photo.file_id)
        file_path = file.file_path

        # Загружаем файл в память
        file_data = await bot.download_file(file_path)
        image_bytes = file_data.read()

        # Кодируем в base64х
        base64_image_from_user = base64.b64encode(image_bytes).decode("utf-8")

        await message.answer(text="Начало генерации фото")
        user_states.set_user_state(state="generation", user_id=get_id_from_message(message))
        # Здесь мы получаем картинку
        generated_image = get_tyan_image(base64_image=base64_image_from_user, text_input=eng_prompt)

        if generated_image:
            # Отправляем сгенерированную фото пользователю
            await message.answer(text="Сгенерированная фотография")
            await message.answer_photo(photo=generated_image) # Отправка фото пользователю
            print(f"Картинка отправлена пользователю: {message.from_user.username}")
            user_states.set_user_state(state="main", user_id=get_id_from_message(message))
        else:
            await message.answer(text="Произошла ошибка, попробуйте еще раз или используйте другое фото")
            user_states.set_user_state(state="main", user_id=get_id_from_message(message))
    else:
        await message.answer(text="Используйте команду /start_generation для старта")


# Функция старта бота
async def start():
    await dp.start_polling(bot)

