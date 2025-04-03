
from frontend.keyboards.menu_gen import menuConstructor
from misc.lang_core import lang
from tools.user_state_handler import users_data

prompt = "Add a realistically styled {girl_type} girlfriend standing next to the existing person in the image. Generate her appearance, clothing, and pose naturally to match the scene's lighting and perspective. Ensure her positioning, facial expression, and body language suggest a natural and affectionate connection, as if she belongs in the original photo."

# список возможных вариантов (можно добавить мультиязычность тут)
valid_options = {
    key: category
    for category, keys in {
        "Japanese": ["азиатка", "asian"],
        "Bikini": ["бикини", "bikini"],
        "Latina": ["латинка", "latina"],
        "Goth": ["готика", "goth"],
        "MILF": ["милфа", "milf"],
        "Curvy": ["пышка", "curvy"],
        "Blonde": ["блондинка", "blonde"],
        "Brunette": ["брюнетка", "brunette"],
        "Redhead": ["рыжая", "redhead"],
        "Tattooed": ["тату", "tattooed"],
        "Pierced": ["пирсинг", "pierced"]
    }.items()
    for key in keys
}


async def handle_advanced_prompt(message):
    users_data.set_user_state(message=message, state="in_advanced_prompt_generation")  # Установка состояния
    await message.answer(
        text=lang.get(key="choose_appearance", message=message),
        reply_markup=menuConstructor.get_menu_with_lang(menu_name="girl_type", message=message)
    )

async def handle_advanced_prompt_selection(message):
    text = message.text.lower()
    if text in valid_options:
        girl_type = valid_options[text]
        final_prompt = prompt.format(girl_type=girl_type)
        users_data.set_user_state(message=message, state="start_advanced_generation")
        users_data.set_user_prompt(message=message, prompt=final_prompt)
        await message.answer(text=lang.get(key="selection_confirm", message=message).format(girl_type=girl_type))
    else:
        await message.answer(text=lang.get(key="invalid_selection", message=message),
                             reply_markup=menuConstructor.get_menu_with_lang(menu_name="girl_type", message=message))

