import os
from dotenv import load_dotenv

# Загружаем переменные из .env
load_dotenv()

# Получаем значения
google_api = os.getenv("GOOGLE_API")
tg_api = os.getenv("TG_API")

users_data_file = "users_data.json"
