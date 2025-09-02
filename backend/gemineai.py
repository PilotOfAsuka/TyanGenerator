from google import genai
from google.genai import types
from io import BytesIO
from aiogram.types import BufferedInputFile
from google.genai.errors import ServerError
from config import google_api
import logging


client = genai.Client(api_key=google_api)  # Экземпляр клиента для работы с Гуглом
logging.basicConfig(level=logging.INFO)

model_2_5 = "gemini-2.5-flash-image-preview"
model_2_0_old = "gemini-2.0-flash-exp-image-generation"
model_2_0 = "gemini-2.0-flash-preview-image-generation"

def edit_image_with_prompt(base64_image, prompt_text_input):
    image = types.Part.from_bytes(data=base64_image, mime_type="image/jpeg")  # считываем картинку из ТГ
    try:
        # Формируем запрос для гугла
        response = client.models.generate_content(
            model=model_2_5,
            contents=[prompt_text_input, image],
            config=types.GenerateContentConfig(
                response_modalities=['Text', 'Image']
            )
        )
        # Проверка ответа от гугла (Кривая на коленках)

        if response is None:
            logging.info(msg=f"Ответ от сервера был пусто {response}")
        else:
            finish_reason = f"{response.candidates[0].finish_reason}"

            if finish_reason == "FinishReason.STOP":
                for part in response.candidates[0].content.parts:
                    if part.inline_data is not None:
                        # Декодируем байты в изображение
                        image = BytesIO(part.inline_data.data)
                        logging.info(msg=f"Картинка сгенерирована")
                        image.seek(0)  # Обязательно перемещаем указатель в начало

                        # Готовим изображение для отправки в Telegram
                        image_tg = BufferedInputFile(image.getvalue(), filename="generated.jpg")
                        return image_tg  # Возвращаем объект BufferedInputFile

            elif finish_reason == "FinishReason.IMAGE_SAFETY":
                print("Гугл вернул ошибку о безопасности фото")
    except ServerError as e:
        print(f"[!] Gemini server error: {e}")
        return None
