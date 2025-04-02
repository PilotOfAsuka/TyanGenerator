import json

description_eng = (
f"🌸 Waifu Snap Bot 🌸\n"
f"\n"
f"✨ Add a cute anime girl to your photos instantly! Just send a picture, and I'll do the rest. 🎀💖\n"
f"\n"
f"📸 How it works?\n"
f"1️⃣ Send a photo with a visible person 📷\n"
f"2️⃣ I'll add an adorable anime girl to your image! 🎨💫\n"
f"3️⃣ Receive your transformed picture in seconds! 🥰🌸\n"
f"\n"
f"📷 For the best results, send a clear, well-lit photo with one person visible. No heavy filters! ✨\n"
f"\n"
f"🎀 Have fun with unique edits, memes, or just for laughs! 💕\n"
f"\n"
f"By sending a photo, you confirm your consent to process the image. ✅\n"
f"\n"
f"Press 'Quick Generation' for instant results or 'Advanced Generation' for more options ⬇️✨\n"
)

description_ru = (
f"🌸 Waifu Snap Бот 🌸\n"
f"\n"
f"✨ Добавьте милую аниме-девочку на свои фото за секунды! Просто отправьте снимок, и я всё сделаю за вас. 🎀💖\n"
f"\n"
f"📸 Как это работает?\n"
f"1️⃣ Отправьте фото, где виден человек 📷\n"
f"2️⃣ Я добавлю очаровательную аниме-девушку на изображение! 🎨💫\n"
f"3️⃣ Получите готовый снимок всего за пару секунд! 🥰🌸\n"
f"\n"
f"📷 Для лучшего результата отправьте чёткое, хорошо освещённое фото с одним человеком. Без сильных фильтров! ✨\n"
f"\n"
f"🎀 Идеально для забавных правок, мемов и просто хорошего настроения! 💕\n"
f"\n"
f"Отправляя фото, вы подтверждаете согласие на его обработку. ✅\n"
f"\n"
f"Нажмите 'Быстрая генерация' для мгновенного результата или 'Продвинутая генерация' для тонкой настройки ⬇️✨\n"
)


def get_description(lang):
    if lang == "ru": return description_ru
    elif lang == "en": return description_eng
    else: return "Not have a description" #Илья Плохо знает англиский...

with open("misc/about.json", "r", encoding="utf-8") as f:
    about_texts = json.load(f)

def get_about_text(lang: str) -> str:
    return about_texts.get(lang, about_texts["en"])  # fallback на англ