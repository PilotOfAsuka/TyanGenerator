import os
def delete_file(file_path):
    # Удаляем файл
    try:
        os.remove(file_path)
        print(f"Файл {file_path} был удалён.")
    except FileNotFoundError:
        print(f"Файл {file_path} не найден.")
    except PermissionError:
        print(f"У вас нет прав для удаления файла {file_path}.")