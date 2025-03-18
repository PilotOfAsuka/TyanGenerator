import base64
import logging
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import Command

from backend.gemineai import geminiAI
from tools.file_manager import delete_file

from config import tg_api

# Это каркас бота в телеграм

rus_prompt = "Добавь девушку (внешность придумай сам) (позу и действие придумай на основе изображеня как бы ты паместил ее), стоящую рядом с существующим человеком)"
eng_prompt = "Add a girlfriend (think up her appearance yourself) (think up her pose and action based on the image of how you would place her) standing next to an existing person)"

logging.basicConfig(level=logging.INFO)

bot = Bot(token=tg_api)
dp = Dispatcher()

# /start
@dp.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer(f"Привет! Я бот который добавит тянку если получится :)\n На ваше изображение.\nВозможны искажения и прочие недочеты.\nОснованно на gemini-2.0-flash-exp от Google!")


# Обработчик изображений
@dp.message(lambda message: message.photo)
async def handle_photo(message: Message):
    photo = message.photo[-1]  # Берем наибольшее по размеру изображение
    file = await bot.get_file(photo.file_id)
    file_path = file.file_path

    # Загружаем файл в память
    file_data = await bot.download_file(file_path)
    image_bytes = file_data.read()

    # Кодируем в base64
    base64_image = base64.b64encode(image_bytes).decode("utf-8")

    # Здесь мы получаем картинку и имя временного файла
    generated_image, name_of_generated_image = geminiAI(base64_image=base64_image, text_input=eng_prompt)

    # Отправляем сгенерированную фото пользователю
    await message.answer_photo(photo=generated_image)
    print(f"Картинка отправлена пользователю: {message.from_user.username}")

    # Удаляем временный файл
    delete_file(name_of_generated_image)

# Функция старта бота
async def start():
    await dp.start_polling(bot)

