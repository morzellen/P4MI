import random
import tkinter as tk
from tkinter import messagebox
from itertools import permutations
import csv

# Данные для тестирования
roman_numerals = ['I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX', 'X']
icons = ['☺', '☻', '♥', '♦', '♣', '♠', '♪', '♫', '☼', '♧']

# Переменные для хранения результатов
correct_answers = 0
rounds = 0
max_rounds = 5
displayed_array = []

# Генерация массива символов без дублирования
def generate_symbol_array():
    # Объединяем римские цифры и иконки, затем выбираем 4 уникальных символа
    array = random.sample(roman_numerals + icons, 4)
    return array

# Показ массива пользователю
def show_symbol_array():
    global displayed_array
    displayed_array = generate_symbol_array()
    label_symbols.config(text=" ".join(displayed_array), font=("Helvetica", 12))
    root.after(3000, hide_symbols)  # Скрытие массива через 3 секунды

# Скрытие массива и показ вариантов
def hide_symbols():
    label_symbols.config(text="")
    generate_options()

# Генерация всех возможных перестановок
def generate_options():
    permutations_list = list(permutations(displayed_array))
    random.shuffle(permutations_list)

    # Оставляем только 24 варианта, если перестановок больше
    options = permutations_list[:24]
    if displayed_array not in options:
        options[0] = displayed_array
    random.shuffle(options)

    for i, btn in enumerate(buttons):
        btn.config(text=" ".join(options[i]), command=lambda opt=options[i]: check_answer(opt))

# Проверка ответа
def check_answer(selected_array):
    global correct_answers, rounds
    if list(selected_array) == displayed_array:
        correct_answers += 1
    
    rounds += 1
    if rounds < max_rounds:
        show_symbol_array()
    else:
        save_results()  # Сохранение результатов в файл
        show_results()

# Сохранение результатов в CSV файл
def save_results():
    with open('test_results_small_size.csv', mode='a', newline='', encoding='UTF-8') as file:
        writer = csv.writer(file)
        writer.writerow([correct_answers])

# Отображение результатов в виде таблицы
def show_results():
    result_text = f"Правильных ответов: {correct_answers}"
    messagebox.showinfo("Результаты", result_text)
    root.quit()

# Создание окна приложения
root = tk.Tk()
root.title("Тест на запоминание символов маленького размера")

# Полноэкранный режим
root.attributes('-fullscreen', True)

label_question = tk.Label(root, text="Запоминайте массив символов", font=("Helvetica", 20))
label_question.pack(pady=20)

label_symbols = tk.Label(root, text="")
label_symbols.pack(pady=20)

# Создание двух фреймов для столбцов кнопок
frame_left = tk.Frame(root)
frame_right = tk.Frame(root)
frame_left.pack(side='left', padx=20, pady=20)
frame_right.pack(side='right', padx=20, pady=20)

# Создание кнопок и их размещение в двух столбцах
buttons = []
for i in range(24):
    btn = tk.Button(root, text="", font=("Helvetica", 20), width=20)
    buttons.append(btn)
    if i < 12:
        btn.pack(in_=frame_left, pady=5)  # Первый столбец
    else:
        btn.pack(in_=frame_right, pady=5)  # Второй столбец

# Старт тестирования
show_symbol_array()

root.mainloop()
