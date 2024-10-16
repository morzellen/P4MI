import os
import sys
import ctypes
import shlex

# Функция для вывода содержимого каталога с разделением на папки и файлы
def list_directory(path='.'):
    if not os.path.isabs(path):
        abs_path = os.path.abspath(path)
    else:
        abs_path = path
    
    try:
        items = os.listdir(abs_path)
        dirs = []
        files = []
        
        for item in items:
            full_path = os.path.join(abs_path, item)
            if os.path.isdir(full_path):
                dirs.append(item)
            else:
                files.append(item)
        
        for dir_name in sorted(dirs):
            print(f"[DIR] {dir_name}")
        
        for file_name in sorted(files):
            print(f"[FILE] {file_name}")
    
    except FileNotFoundError:
        print(f"Каталог '{path}' не найден.")
    except PermissionError:
        print(f"Нет доступа к каталогу '{path}'.")

# Функция для установки атрибутов
def set_attributes(paths, hidden=None, readonly=None):
    for path in paths:
        if hidden is not None:
            set_hidden(path, hidden)
        if readonly is not None:
            set_readonly(path, readonly)

def set_hidden(path, hide):
    if os.name == 'nt':
        FILE_ATTRIBUTE_HIDDEN = 0x02
        attrs = ctypes.windll.kernel32.GetFileAttributesW(path)
        if hide:
            ctypes.windll.kernel32.SetFileAttributesW(path, attrs | FILE_ATTRIBUTE_HIDDEN)
            print(f"'{path}' скрыт.")
        else:
            ctypes.windll.kernel32.SetFileAttributesW(path, attrs & ~FILE_ATTRIBUTE_HIDDEN)
            print(f"'{path}' больше не скрыт.")
    else:
        print("Скрытие файлов доступно только на Windows.")

def set_readonly(path, readonly):
    if os.name == 'nt':
        FILE_ATTRIBUTE_READONLY = 0x01
        attrs = ctypes.windll.kernel32.GetFileAttributesW(path)
        if readonly:
            ctypes.windll.kernel32.SetFileAttributesW(path, attrs | FILE_ATTRIBUTE_READONLY)
            print(f"'{path}' теперь только для чтения.")
        else:
            ctypes.windll.kernel32.SetFileAttributesW(path, attrs & ~FILE_ATTRIBUTE_READONLY)
            print(f"'{path}' больше не только для чтения.")
    else:
        print("Атрибут 'только для чтения' доступен только на Windows.")

# Функция для смены текущего каталога
def change_directory(path):
    try:
        os.chdir(path)
        print(f"Текущий каталог изменен на '{path}'.")
    except FileNotFoundError:
        print(f"Каталог '{path}' не найден.")
    except PermissionError:
        print(f"Нет доступа к каталогу '{path}'.")

# Парсинг списка файлов из строки с учётом пробелов
def parse_file_list(file_list_str):
    if file_list_str.startswith('[') and file_list_str.endswith(']'):
        file_list_str = file_list_str[1:-1]  # Убираем квадратные скобки
    files = [f.strip() for f in file_list_str.split(',')]  # Разбиваем строку и убираем лишние пробелы
    return files

# Функция для обработки команд
def handle_command(command):
    if command[0] == "listdir":
        path = command[1] if len(command) > 1 else '.'
        list_directory(path)
    elif command[0] == "setattr":
        if len(command) < 4:
            print("Неверный формат команды. Пример: setattr [file1, file2] hidden True")
        else:
            file_list = parse_file_list(command[1])
            attr = command[2]
            value = command[3].lower() == 'true'
            
            set_attributes(file_list, hidden=value if attr == "hidden" else None,
                           readonly=value if attr == "readonly" else None)
    elif command[0] == "chdir":
        if len(command) < 2:
            print("Неверный формат команды. Пример: chdir /path/to/directory")
        else:
            change_directory(command[1])
    elif command[0] == "exit":
        print("Выход из программы.")
        sys.exit(0)
    else:
        print(f"Неизвестная команда '{command[0]}'")

# Функция для ввода новых команд
def run_command():
    while True:
        command = input("Введите команду: ").strip().split()
        if not command:
            continue
        handle_command(command)

# Основная программа
if __name__ == "__main__":
    # Проверяем, были ли переданы аргументы
    if len(sys.argv) > 1:
        initial_command = sys.argv[1:]
        handle_command(initial_command)  # Выполняем команду, переданную в аргументах
        
    # Переходим в режим ввода команд
    run_command()
