import pandas as pd
import matplotlib.pyplot as plt

# Чтение данных из файлов
data_small = pd.read_csv('dist\\test_results_small_size.csv', header=None)
data_large = pd.read_csv('dist\\test_results_large_size.csv', header=None)
data_different = pd.read_csv('dist\\test_results_different_size.csv', header=None)

# Переименование колонок для удобства
data_small.columns = ['Правильные ответы']
data_large.columns = ['Правильные ответы']
data_different.columns = ['Правильные ответы']

# Подсчёт суммы правильных ответов
sum_small = data_small['Правильные ответы'].sum()
sum_large = data_large['Правильные ответы'].sum()
sum_different = data_different['Правильные ответы'].sum()

# Создание данных для отображения
labels = ['Маленькие символы', 'Большие символы', 'Разные символы']
sums = [sum_small, sum_large, sum_different]

# Построение столбцов
plt.bar(labels, sums, color=['blue', 'green', 'red'])

plt.title('Сравнение сумм правильных ответов')
plt.ylabel('Сумма правильных ответов')

# Отображение столбцов
plt.show()
