import json

description_eng = (
f"🌸 DreamTogetherBot 🌸\n"
f"\n"
f"✨ Want to add a cute girl or boy to your photos? Just send a picture, and I'll do my magic! 🎀💖\n"
f"\n"
f"📸 How it works?\n"
f"1️⃣ Send me a photo of a person 📷\n"
f"2️⃣ I'll add an adorable girl (or boy) to the image! 🎨💫\n"
f"3️⃣ Get your couple photo in seconds! 🥰🌸\n"
f"\n"
f"⚡ Advanced mode: Use your own custom prompt! Write what you want — add yourself, a partner, or even a fun fantasy character. 📝✨\n"
f"\n"
f"📷 For best results, send a clear photo with one person visible. Bright lighting and no filters work best! ✨\n"
f"\n"
f"🎀 Perfect for fun edits, memes, roleplay, or just for laughs! 💕\n"
f"\n"
f"By sending a photo, you confirm your consent to process the image. ✅\n"
f"\n"
f"For a quick start press 'Quick generation girl/boy' or choose 'Advanced generation' for full customization ⬇️✨\n"
)



description_ru = (
f"🌸 DreamTogetherBot 🌸\n"
f"\n"
f"✨ Хотите добавить милую девушку или парня на свои фотографии? Просто отправьте фото, и я сделаю своё волшебство! 🎀💖\n"
f"\n"
f"📸 Как это работает?\n"
f"1️⃣ Отправьте фотографию человека 📷\n"
f"2️⃣ Я добавлю на изображение очаровательную девушку или парня! 🎨💫\n"
f"3️⃣ Получите парное фото за считанные секунды! 🥰🌸\n"
f"\n"
f"⚡ В расширенном режиме можно использовать свой собственный промпт! Пишите, кого хотите видеть: себя, партнёра или даже фантазийного персонажа. 📝✨\n"
f"\n"
f"📷 Чтобы получить лучший результат, отправьте чёткое фото с одним человеком. Яркое освещение — идеально! ✨\n"
f"\n"
f"🎀 Идеально для забавных фотоправок, мемов, ролевых игр или просто веселья! 💕\n"
f"\n"
f"Отправляя фото, вы подтверждаете согласие на его обработку. ✅\n"
f"\n"
f"Для быстрого старта нажмите 'Быстрая генерация девушки/парня' или выберите 'Продвинутая генерация' для полной настройки ⬇️✨\n"
)




def get_description(lang):
    if lang == "ru": return description_ru
    elif lang == "en": return description_eng
    else: return "Not have a description" #Илья Плохо знает англиский...

with open("misc/about.json", "r", encoding="utf-8") as f:
    about_texts = json.load(f)

def get_about_text(lang: str) -> str:
    return about_texts.get(lang, about_texts["en"])  # fallback на англ