import json

description_eng = (
f"🌸 Waifu Snap Bot 🌸\n"
f"\n"
f"✨ Want to add a cute girl to your photos? Just send a picture, and I'll do my magic! 🎀💖\n"
f"\n"
f"📸 How it works?\n"
f"1️⃣ Send me a photo of a person 📷\n"
f"2️⃣ I'll add an adorable girl to the image! 🎨💫\n"
f"3️⃣ Get your girlfriend picture in seconds! 🥰🌸\n"
f"📷 For best results, send a clear photo with one person visible. Bright lighting and no filters work best! ✨\n"
f"\n"
f"🎀 Perfect for fun edits, memes, or just for laughs! 💕\n"
f"\n"
f"For quick start Press 'Quick generation' or press 'Advanced generation' for Advanced Settings ⬇️✨\n"
)

description_ru =(
f"🌸 Waifu Snap Бот 🌸\n"
f"\n"
f"✨ Хотите добавить милую девушку на свои фотографии? Просто отправьте фотографию, и я сделаю свое волшебство! 🎀💖\n"
f"\n"
f"📸 Как это работает?\n"
f"1️⃣ Отправьте мне фотографию человека 📷\n"
f"2️⃣ Я добавлю к изображению очаровательную девочку! 🎨💫\n"
f"3️⃣ Получите фотографию своей девушки за считанные секунды! 🥰🌸\n"
f"\n"
f"📷 Чтобы получить лучший результат, отправьте чёткое фото с одним человеком. Яркое освещение — идеально! ✨\n"
f"🎀 Идеально подходит для забавных правок, мемов или просто смеха! 💕\n"
f"\n"
f"Для быстрого старта нажмите 'Быстрая генерация' или нажмите 'Продвинутая генерация' для Расширенных настроек ⬇️✨\n"
)

def get_description(lang):
    if lang == "ru": return description_ru
    elif lang == "en": return description_eng
    else: return "Not have a description" #Илья Плохо знает англиский...

with open("misc/about.json", "r", encoding="utf-8") as f:
    about_texts = json.load(f)

def get_about_text(lang: str) -> str:
    return about_texts.get(lang, about_texts["en"])  # fallback на англ