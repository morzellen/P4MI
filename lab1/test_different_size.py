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

# Генерация массива символов разного размера без дублирования
def generate_symbol_array():
    unique_symbols = random.sample(roman_numerals + icons, 4)  # Уникальные символы
    array = [(symbol, random.choice([12, 30])) for symbol in unique_symbols]  # Присвоение случайного размера
    return array


# Показ массива пользователю
def show_symbol_array():
    global displayed_array
    displayed_array = generate_symbol_array()

    # Очищаем текстовое поле перед показом нового массива
    label_symbols.delete(1.0, tk.END)

    for symbol, size in displayed_array:
        label = tk.Label(root, text=symbol, font=("Helvetica", size))
        label_symbols.window_create("end", window=label)

    root.after(3000, hide_symbols)  # Скрытие массива через 3 секунды

# Скрытие массива и показ вариантов
def hide_symbols():
    label_symbols.delete(1.0, tk.END)
    generate_options()

# Генерация всех возможных перестановок
def generate_options():
    # Составляем перестановки символов вместе с их размерами
    permutations_list = list(permutations(displayed_array))
    random.shuffle(permutations_list)

    # Оставляем только 24 варианта, если перестановок больше
    options = permutations_list[:24]
    if displayed_array not in options:
        options[0] = displayed_array
    random.shuffle(options)

    for i, btn in enumerate(buttons):
        option_text = " ".join([f"{symbol}" for symbol, size in options[i]])
        btn.config(text=option_text, command=lambda opt=options[i]: check_answer(opt))

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
    with open('test_results_different_size.csv', mode='a', newline='', encoding='UTF-8') as file:
        writer = csv.writer(file)
        writer.writerow([correct_answers])

# Отображение результатов
def show_results():
    result_text = f"Правильных ответов: {correct_answers}"
    messagebox.showinfo("Результаты", result_text)
    root.quit()

# Создание окна приложения
root = tk.Tk()
root.title("Тест на запоминание символов разного размера")

# Полноэкранный режим
root.attributes('-fullscreen', True)

label_question = tk.Label(root, text="Запоминайте массив символов разного размера", font=("Helvetica", 20))
label_question.pack(pady=20)

label_symbols = tk.Text(root, height=2, width=50)
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
