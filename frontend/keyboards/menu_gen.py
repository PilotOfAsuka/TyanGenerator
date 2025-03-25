from aiogram.types import (ReplyKeyboardMarkup,
                           KeyboardButton)
from frontend.keyboards.menu_lists import menu_buttons_list


# Класс конструктора меню
class MenuConstructor:
    def __init__(self, menu_list):
        self.menus = {}
        self.menu_list = menu_list

    def create_menu(self):
        # Функция для создания ReplyKeyboardMarkup из списка кнопок
        for menu_name in self.menu_list:
            buttons = [[KeyboardButton(text=button)] for button in self.menu_list[menu_name]]
            menu = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=buttons, one_time_keyboard=True)
            self.menus[menu_name] = menu

    # Возвращает меню по имени
    def get_menu(self, menu_name: str):
        return self.menus.get(menu_name)

    # Возвращает текст кнопки, по имени меню и ее индекса в списке
    def get_button_text(self, menu_name, index):
        return self.menu_list[menu_name][index]


menuConstructor = MenuConstructor(menu_list=menu_buttons_list) # Инициализация меню конструктора
menuConstructor.create_menu() # Создание клавиатур из menu_list




