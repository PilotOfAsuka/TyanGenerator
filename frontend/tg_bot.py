from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton  # Импортируем для создания кнопок

import base64
import logging
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import Command

from backend.gemineai import get_tyan_image

from config import tg_api

# Функция чтоб считывать описание бота с текстового документа. Сделал чтоб легче было разбираться где описание поминять
def load_description():
    with open("description.txt", "r", encoding="utf-8") as file:
        return file.read()
    
# Это каркас бота в телеграм

# "Добавь девушку (внешность придумай сам) (позу и действие придумай на основе изображеня как бы ты паместил ее), стоящую рядом с существующим человеком)"
eng_prompt = "Add a girlfriend (think up her appearance yourself) (think up her pose and action based on the image of how you would place her) standing next to an existing person)"

logging.basicConfig(level=logging.INFO)

bot = Bot(token=tg_api)
dp = Dispatcher()

# Создаем клавиатуру с кнопками
def create_keyboard():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="About", callback_data="about"),
            InlineKeyboardButton(text="Advanced Prompt settings", callback_data="advanced_prompt")
        ]
    ])
    return keyboard

# Обработчик команды /start
@dp.message(Command("start"))
async def cmd_start(message: Message):
    description = load_description()
    await message.answer(description, parse_mode="Markdown")
    await message.answer(f"Привет! Я бот который добавит тянку если получится :)\n На ваше изображение.\nВозможны искажения и прочие недочеты.\nОснованно на gemini-2.0-flash-exp от Google!")

# Обработчик нажатий на кнопки
@dp.callback_query(lambda query: True)
async def handle_button_click(query):
    if query.data == "about":
        await query.message.answer("Здесь будет описание бота, Я пока не приудмал. Может сам добавишь")
    elif query.data == "advanced_prompt":
        await query.message.answer("Здесь будут настройки промпта. Пока что это в разработке.")


# Обработчик изображений
@dp.message(lambda message: message.photo)
async def handle_photo(message: Message):
    photo = message.photo[-1]  # Берем наибольшее по размеру изображение
    file = await bot.get_file(photo.file_id)
    file_path = file.file_path

    # Загружаем файл в память
    file_data = await bot.download_file(file_path)
    image_bytes = file_data.read()

    # Кодируем в base64х
    base64_image_from_user = base64.b64encode(image_bytes).decode("utf-8")
    await message.answer(text="Начало генерации фото")
    # Здесь мы получаем картинку
    generated_image = get_tyan_image(base64_image=base64_image_from_user, text_input=eng_prompt)

    if generated_image:
        # Отправляем сгенерированную фото пользователю
        await message.answer(text="Сгенерированная фотография")
        await message.answer_photo(photo=generated_image) # Отправка фото пользователю
        print(f"Картинка отправлена пользователю: {message.from_user.username}")
    else:
        await message.answer(text="Произошла ошибка, попробуйте еще раз или используйте другое фото")


# Функция старта бота
async def start():
    await dp.start_polling(bot)

