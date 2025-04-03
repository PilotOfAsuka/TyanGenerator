from tools.my_func import load_json, save_in_json, get_id_from_message
from config import users_data_file

# Класс для работы с информацией пользователей by PilotOfAsuka alpha 0.1
class UsersData:
    def __init__(self, json_name):
        self.json_name = json_name
        self.users_data = load_json(self.json_name)

    # Инициализация начального списка информаций пользователей, используется при команде /start
    def init_self_states(self, message):
        user_id = get_id_from_message(message)

        self.users_data.setdefault(user_id, {
            "state": None,
            "language": None,
            "prompt": None,
        })

        save_in_json(self.users_data, self.json_name)

    # Устанавливает состояние "state" пользователя
    def set_user_state(self, message, state):
        self.users_data[get_id_from_message(message)]["state"] = state
        save_in_json(self.users_data, self.json_name)

    # Возвращает "state" из users_data
    def get_user_state(self, message):
        return self.users_data[get_id_from_message(message)]["state"]

    # Возвращает Тру или Фолс если state совпадает с текущим состоянием
    def compare_self_state(self, message, state):
        # Эта функция нужна для того чтобы убеждатся что пользователь действительно
        # Находиться на том этапе который нам нужен
        return True if self.get_user_state(message=message) == state else False

    # Возвращает "language" из users_data
    def get_user_language(self, message):
        return self.users_data[get_id_from_message(message)]["language"]

    # Устанавливает язык пользователю
    def set_user_language(self, message, language):
        self.users_data[get_id_from_message(message)]["language"] = language
        save_in_json(self.users_data, self.json_name)

    # Возвращает "prompt" из users_data
    def get_user_prompt(self, message):
        return self.users_data[get_id_from_message(message)]["prompt"]

    # Установка значения промпта для пользователя
    def set_user_prompt(self, message, prompt):
        self.users_data[get_id_from_message(message)]["prompt"] = prompt

    # Очистка кастомного промпта пользователя
    def clear_custom_prompt(self, message):
        self.users_data[get_id_from_message(message)]["prompt"] = ""
        save_in_json(self.users_data, self.json_name)

    # Возврашает количество юзеров
    def get_unique_users_count(self):
        return len(self.users_data)


users_data = UsersData(json_name=users_data_file)
