from tools.my_func import load_json, save_in_json
from config import user_state_file

# Класс определяет, где находится юзер для обработки событий
class UserStates:
    def __init__(self):
        self.user_state = load_json(user_state_file)

    def set_user_state(self, state, user_id):
        """Функция установки 'user_state'"""
        self.user_state[user_id] = state
        save_in_json(self.user_state, user_state_file)
        pass

    # Инициализация начального списка состояний меню
    def init_self_states(self, user_id):
        self.user_state[user_id] = ""

    # Возвращает последнее стояние
    def get_user_state(self, user_id):
        return self.user_state.get(user_id)



user_states = UserStates()  # Инициализация класса
