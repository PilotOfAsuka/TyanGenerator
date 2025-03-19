from aiogram import types
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# Класс для состояний
class AdvancedPromptStates:
    waiting_for_ethnicity = "waiting_for_ethnicity"
    waiting_for_hair_color = "waiting_for_hair_color"
    waiting_for_hair_length = "waiting_for_hair_length"

async def start_advanced_prompt_dialog(query: types.CallbackQuery, state: FSMContext):
    # Переводим пользователя в состояние выбора внешности
    await state.set_state(AdvancedPromptStates.waiting_for_ethnicity)
    
    # Сохраняем пустую строку для user_prompt в состоянии
    await state.update_data(user_prompt="")

    # Создаем клавиатуру с выбором внешности
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Asian", callback_data="ethnicity_asian")],
        [InlineKeyboardButton(text="African", callback_data="ethnicity_black")],
        [InlineKeyboardButton(text="European", callback_data="ethnicity_european")],
        [InlineKeyboardButton(text="Latino", callback_data="ethnicity_latina")],
    ])
    
    # Задаем вопрос
    await query.message.answer("Select an appearance from the suggested buttons:", reply_markup=keyboard)

async def handle_ethnicity_choice(query: types.CallbackQuery, state: FSMContext):
    # Получаем текущие данные
    data = await state.get_data()
    
    # Обновляем user_prompt и сохраняем выбор пользователя
    user_prompt = data.get("user_prompt", "") + query.data + " "
    await state.update_data(user_prompt=user_prompt, ethnicity=query.data)

    # Переводим пользователя в состояние выбора цвета волос
    await state.set_state(AdvancedPromptStates.waiting_for_hair_color)

    # Создаем клавиатуру с выбором цвета волос
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Блондинка", callback_data="hair_color_blonde")],
        [InlineKeyboardButton(text="Брюнетка", callback_data="hair_color_brunette")],
        [InlineKeyboardButton(text="Рыжая", callback_data="hair_color_red")],
        [InlineKeyboardButton(text="Черная", callback_data="hair_color_black")],
    ])

    # Задаем вопрос
    await query.message.answer("Отлично! Теперь выбери цвет волос:", reply_markup=keyboard)
    await query.answer()

async def handle_hair_color_choice(query: types.CallbackQuery, state: FSMContext):
    # Сохраняем выбор пользователя
    data = await state.get_data()
    user_prompt = data.get("user_prompt", "") + query.data + " "
    await state.update_data(user_prompt=user_prompt, hair_color=query.data)

    # Переводим пользователя в состояние выбора длины волос
    await state.set_state(AdvancedPromptStates.waiting_for_hair_length)

    # Создаем клавиатуру с выбором длины волос
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Короткие", callback_data="hair_length_short")],
        [InlineKeyboardButton(text="Средние", callback_data="hair_length_medium")],
        [InlineKeyboardButton(text="Длинные", callback_data="hair_length_long")],
    ])

    # Задаем вопрос
    await query.message.answer("Супер! Теперь выбери длину волос:", reply_markup=keyboard)
    await query.answer()

async def handle_hair_length_choice(query: types.CallbackQuery, state: FSMContext):
    # Сохраняем выбор пользователя
    data = await state.get_data()
    user_prompt = data.get("user_prompt", "") + query.data + " "
    await state.update_data(user_prompt=user_prompt, hair_length=query.data)

    # Получаем все сохраненные данные
    user_data = await state.get_data()

    # Формируем итоговый промпт с защитой от ошибок
    final_prompt = (
        f"Девушка: {user_data.get('ethnicity', 'Не выбрано')}, "
        f"цвет волос: {user_data.get('hair_color', 'Не выбрано')}, "
        f"длина волос: {user_data.get('hair_length', 'Не выбрано')}"
    )

    # Отправляем итоговый промпт пользователю
    await query.message.answer(f"Твой выбор:\n{final_prompt}")

    # Сбрасываем состояние
    await state.clear()
    await query.answer()  # ✅ Добавлено для закрытия кнопки
