import random

from google import genai
from google.genai import types
from PIL import Image
from io import BytesIO
from aiogram.types import FSInputFile

from config import google_api


client = genai.Client(api_key=google_api)  # Экземпляр клиента для работы с Гуглом


def geminiAI(base64_image, text_input):
    image = types.Part.from_bytes(data=base64_image, mime_type="image/jpeg")  # считываем картинку из ТГ

    # Формируем запрос для гугла
    response = client.models.generate_content(
        model="gemini-2.0-flash-exp-image-generation",
        contents=[text_input, image],
        config=types.GenerateContentConfig(
            response_modalities=['Text', 'Image']
        )
    )
    # Проверка ответа от гугла (Кривая на коленках)
    if response is None:
        print(f"Ответ от сервера пустой")
    else:

        for part in response.candidates[0].content.parts:
            if part.inline_data is not None:
                image = Image.open(BytesIO(part.inline_data.data))  # получаем картинку с байт кода от ответа гугла

                name = f'image_{random.randint(0, 9999)}.png'  # Временное имя для файла

                print(f"Картинка сгенерирована {name}")

                image.save(name)

                print(f'Картинка сохранена {name}')

                image_tg = FSInputFile(name)  # Формируем картинку для отправки в телеграм

                return image_tg, name  # Возвращаем картинку и название временного файла
