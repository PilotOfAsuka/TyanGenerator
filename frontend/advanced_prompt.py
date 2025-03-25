from aiogram.types import Message
from frontend.keyboards.menu_gen import menuConstructor
from tools.user_state_handler import users_data  
from frontend.photo_handler import handle_photo_generation

prompt = "Add a realistically styled {girl_type} standing next to the existing person in the image. Generate her appearance, clothing, and pose naturally to match the scene's lighting and perspective. Ensure her positioning, facial expression, and body language suggest a natural and affectionate connection, as if she belongs in the original photo."

# список возможных вариантов (можно добавить мультиязычность тут)

valid_options = {
    "азиатка": "Japanese",
    "бикини": "Bikini",
    "латинка": "Latina",
    "bbw": "BBW",
    "asian": "Japanese",
    "bikini": "Bikini",
    "latina": "Latina"
}

async def handle_advanced_prompt(message: Message):
    users_data.set_user_state(message=message, state="advanced_prompt")  # ✅ Установка состояния
    await message.answer(
        text="Выберите Внешность Девочки \n(Осторожней с выбором BBW...)\nЯ вас предупреждаю...",
        reply_markup=menuConstructor.get_menu("girl_type_en")
    )

async def handle_advanced_prompt_selection(message: Message):
    text = message.text.lower()
    if text in valid_options:
        girl_type = valid_options[text]
        final_prompt = prompt.format(girl_type=girl_type)
        await message.answer(f"✅ Вы выбрали: {girl_type}\nМожете теперь отправить фото.")

       
        
    else:
        await message.answer("❌ Пожалуйста, выберите один из предложенных вариантов.")

