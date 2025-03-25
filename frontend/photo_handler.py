import base64
import logging
from backend.gemineai import get_tyan_image
from aiogram.types import Message
from tools.my_func import get_id_from_message
from misc.core import bot
from frontend.keyboards.menu_gen import menuConstructor

from tools.user_state_handler import users_data



async def handle_photo_generation(message: Message, prompt: str):
    user_id = get_id_from_message(message)
    username = message.from_user.username or "NoUsername"
    logging.info(f"[{user_id}] Получено изображение от пользователя @{username}")

    photo = message.photo[-1]
    file = await bot.get_file(photo.file_id)
    file_data = await bot.download_file(file.file_path)
    image_bytes = file_data.read()

    base64_image = base64.b64encode(image_bytes).decode("utf-8")

    editable_msg = await message.answer(text="Генерация изображения...")

    users_data.set_user_state(message=message, state="ingeneration")

    generated_image = get_tyan_image(base64_image=base64_image, text_input=prompt)

    if generated_image:
        logging.info(f"[{user_id}] Успешно сгенерировано изображение для @{username}")
        users_data.set_user_state(message=message, state="main")
        await editable_msg.delete()
        await message.answer_photo(photo=generated_image, reply_markup=menuConstructor.get_menu("main_menu"), caption="Ваше изображение сгенерированo\nЧтобы начать заново, нажмите Start Generation или Advanced Prompt Settings.")
    else:
        logging.error(f"[{user_id}] Ошибка генерации изображения для @{username}")
        users_data.set_user_state(message=message, state="main")
        await editable_msg.delete()
        await message.answer(text="Генерация была прервана. Чтобы продолжить работу с ботом, выберите Start Generation или Advanced Prompt Settings и начните заново.", reply_markup=menuConstructor.get_menu("main_menu"))
