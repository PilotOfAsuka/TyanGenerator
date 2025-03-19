import json



# Функция для разделения аргументов из строки /команда аргумент1 .... аргументN
def extract_arguments(command_string):
    # Разделяем строку по пробелу, чтобы отделить команду от аргументов
    parts = command_string.split(' ', 1)

    # Проверяем, есть ли аргументы после команды
    if len(parts) > 1:
        # Разделяем аргументы по запятой и удаляем лишние пробелы
        arguments = [arg.strip() for arg in parts[1].split(',')]
        return arguments
    else:
        return []  # Если аргументов нет, возвращаем пустой список

# Загрузка данных из файла
def load_json(name):
    """Функция загрузки JSON в переменную"""
    try:
        with open(name, 'r') as file_user:
            file = json.load(file_user)
            print(f"{name} - loading successful")
            return file
    except FileNotFoundError:
        # Если файл не найден, начинаем с пустого словаря
        file = {}
        print(f"{name} not found, we make a new :)")
        return file


def save_in_json(dictionary, file_dir):
    """Принимает на вход словарь (dictionary) значений и сохраняет в файл JSON"""
    with open(file_dir, 'w') as file:
        json.dump(dictionary, file)


def get_id_from_message(msg):
    return str(msg.from_user.id)