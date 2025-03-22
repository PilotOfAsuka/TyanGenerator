from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton

from frontend.photo_handler import handle_photo_generation

# Шаг 1 — Внешность
async def handle_advanced_prompt(message: Message):


    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Азиатка")],
            [KeyboardButton(text="Европейка")],
            [KeyboardButton(text="Африканка")],
            [KeyboardButton(text="Латинка")]
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )
    await message.answer("Выберите внешность девушки:", reply_markup=keyboard)


# Шаг 2 — Поза
async def handle_appearance_choice(message: Message):
    user_id = message.from_user.id
    appearance = message.text



    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Сидит")],
            [KeyboardButton(text="Стоит")],
            [KeyboardButton(text="Смотрит в Сторону")],
            [KeyboardButton(text="Целует в Щечку")]
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )
    await message.answer("Теперь выберите позу:", reply_markup=keyboard)


# Шаг 3 — Генерация текста
async def handle_pose_choice(message: Message):
    user_id = message.from_user.id
    pose = message.text



    appearance = data.get("appearance", "girl")
    pose = data.get("pose", "standing")

    # Маппинг на английский (упрощённый)
    appearance_map = {
        "Азиатка": "Japanese",
        "Европейка": "European",
        "Африканка": "African",
        "Латинка": "Latina"
    }

    pose_map = {
        "Сидит": "sitting next to",
        "Стоит": "standing beside",
        "Смотрит в Сторону": "looking away while next to",
        "Целует в Щечку": "kissing the cheek of"
    }

    prompt = f"Add a realistically styled {appearance_map.get(appearance, 'girl')} girlfriend {pose_map.get(pose, 'next to')} the existing person in the image. Generate her appearance, clothing, and pose naturally to match the scene's lighting and perspective. Ensure her positioning, facial expression, and body language suggest a natural and affectionate connection, as if she belongs in the original photo."

    await message.answer("Промпт сгенерирован:")
    await message.answer(prompt)




    # когда готов твой кастомный промпт:
    await handle_photo_generation(message, prompt)
